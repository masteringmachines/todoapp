"""
Database models and schema for the Daily Todo App.
"""

import sqlite3
from datetime import datetime, date
from typing import Optional, List, Dict
from pathlib import Path


class Database:
    """Manage SQLite database operations."""
    
    def __init__(self, db_path: str = "data/tasks.db"):
        """Initialize database connection."""
        self.db_path = db_path
        Path(db_path).parent.mkdir(parents=True, exist_ok=True)
        self.conn = None
        self.init_db()
    
    def init_db(self):
        """Initialize database schema."""
        self.conn = sqlite3.connect(self.db_path)
        self.conn.row_factory = sqlite3.Row
        
        # Create tasks table
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                description TEXT,
                priority TEXT DEFAULT 'medium',
                energy_level TEXT DEFAULT 'medium',
                category TEXT DEFAULT 'personal',
                due_date TEXT,
                time_estimate INTEGER,
                completed BOOLEAN DEFAULT 0,
                completed_at TEXT,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                mood TEXT
            )
        """)
        
        # Create focus sessions table
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS focus_sessions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                task_id INTEGER,
                duration INTEGER,
                started_at TEXT,
                completed BOOLEAN DEFAULT 0,
                FOREIGN KEY (task_id) REFERENCES tasks(id)
            )
        """)
        
        # Create daily stats table
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS daily_stats (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT UNIQUE,
                tasks_completed INTEGER DEFAULT 0,
                focus_minutes INTEGER DEFAULT 0,
                energy_level TEXT,
                mood_summary TEXT
            )
        """)
        
        self.conn.commit()
    
    def add_task(self, title: str, description: str = "", priority: str = "medium",
                 energy_level: str = "medium", category: str = "personal",
                 due_date: Optional[str] = None, time_estimate: Optional[int] = None) -> int:
        """Add a new task."""
        cursor = self.conn.execute("""
            INSERT INTO tasks (title, description, priority, energy_level, category, 
                             due_date, time_estimate)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (title, description, priority, energy_level, category, due_date, time_estimate))
        self.conn.commit()
        return cursor.lastrowid
    
    def get_tasks(self, completed: bool = False, category: Optional[str] = None,
                  energy_level: Optional[str] = None, due_today: bool = False) -> List[Dict]:
        """Get tasks with optional filters."""
        query = "SELECT * FROM tasks WHERE completed = ?"
        params = [1 if completed else 0]
        
        if category:
            query += " AND category = ?"
            params.append(category)
        
        if energy_level:
            query += " AND energy_level = ?"
            params.append(energy_level)
        
        if due_today:
            today = date.today().isoformat()
            query += " AND due_date = ?"
            params.append(today)
        
        query += " ORDER BY priority DESC, created_at DESC"
        
        cursor = self.conn.execute(query, params)
        return [dict(row) for row in cursor.fetchall()]
    
    def get_task(self, task_id: int) -> Optional[Dict]:
        """Get a specific task by ID."""
        cursor = self.conn.execute("SELECT * FROM tasks WHERE id = ?", (task_id,))
        row = cursor.fetchone()
        return dict(row) if row else None
    
    def complete_task(self, task_id: int, mood: Optional[str] = None):
        """Mark a task as completed."""
        now = datetime.now().isoformat()
        self.conn.execute("""
            UPDATE tasks 
            SET completed = 1, completed_at = ?, mood = ?
            WHERE id = ?
        """, (now, mood, task_id))
        self.conn.commit()
        
        # Update daily stats
        self._update_daily_stats()
    
    def delete_task(self, task_id: int):
        """Delete a task."""
        self.conn.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
        self.conn.commit()
    
    def update_task(self, task_id: int, **kwargs):
        """Update task fields."""
        allowed_fields = ['title', 'description', 'priority', 'energy_level', 
                         'category', 'due_date', 'time_estimate']
        
        updates = []
        values = []
        for key, value in kwargs.items():
            if key in allowed_fields:
                updates.append(f"{key} = ?")
                values.append(value)
        
        if updates:
            values.append(task_id)
            query = f"UPDATE tasks SET {', '.join(updates)} WHERE id = ?"
            self.conn.execute(query, values)
            self.conn.commit()
    
    def add_focus_session(self, task_id: int, duration: int, completed: bool = True):
        """Log a focus session."""
        now = datetime.now().isoformat()
        self.conn.execute("""
            INSERT INTO focus_sessions (task_id, duration, started_at, completed)
            VALUES (?, ?, ?, ?)
        """, (task_id, duration, now, 1 if completed else 0))
        self.conn.commit()
        
        # Update daily stats
        self._update_daily_stats()
    
    def get_focus_sessions(self, days: int = 7) -> List[Dict]:
        """Get recent focus sessions."""
        cursor = self.conn.execute("""
            SELECT f.*, t.title 
            FROM focus_sessions f
            LEFT JOIN tasks t ON f.task_id = t.id
            WHERE f.started_at >= date('now', '-' || ? || ' days')
            ORDER BY f.started_at DESC
        """, (days,))
        return [dict(row) for row in cursor.fetchall()]
    
    def get_stats(self, days: int = 7) -> Dict:
        """Get statistics for the past N days."""
        # Task completion stats
        cursor = self.conn.execute("""
            SELECT COUNT(*) as total_completed,
                   AVG(CASE WHEN priority = 'high' THEN 1 ELSE 0 END) as high_priority_pct
            FROM tasks
            WHERE completed = 1 
            AND completed_at >= date('now', '-' || ? || ' days')
        """, (days,))
        task_stats = dict(cursor.fetchone())
        
        # Focus time stats
        cursor = self.conn.execute("""
            SELECT SUM(duration) as total_focus_minutes,
                   COUNT(*) as total_sessions
            FROM focus_sessions
            WHERE started_at >= date('now', '-' || ? || ' days')
        """, (days,))
        focus_stats = dict(cursor.fetchone())
        
        # Mood distribution
        cursor = self.conn.execute("""
            SELECT mood, COUNT(*) as count
            FROM tasks
            WHERE completed = 1 
            AND completed_at >= date('now', '-' || ? || ' days')
            AND mood IS NOT NULL
            GROUP BY mood
        """, (days,))
        mood_stats = {row['mood']: row['count'] for row in cursor.fetchall()}
        
        # Current streak
        streak = self._calculate_streak()
        
        return {
            'tasks': task_stats,
            'focus': focus_stats,
            'moods': mood_stats,
            'streak': streak
        }
    
    def _calculate_streak(self) -> int:
        """Calculate current completion streak (consecutive days)."""
        cursor = self.conn.execute("""
            SELECT DISTINCT DATE(completed_at) as date
            FROM tasks
            WHERE completed = 1
            ORDER BY date DESC
            LIMIT 365
        """)
        
        dates = [row['date'] for row in cursor.fetchall()]
        if not dates:
            return 0
        
        # Check if today has completions
        today = date.today().isoformat()
        if not dates or dates[0] != today:
            # Check if yesterday has completions (streak might continue)
            yesterday = str(date.today().replace(day=date.today().day - 1))
            if not dates or dates[0] != yesterday:
                return 0
        
        # Count consecutive days
        streak = 1
        for i in range(len(dates) - 1):
            current = datetime.fromisoformat(dates[i]).date()
            next_date = datetime.fromisoformat(dates[i + 1]).date()
            diff = (current - next_date).days
            
            if diff == 1:
                streak += 1
            else:
                break
        
        return streak
    
    def _update_daily_stats(self):
        """Update today's statistics."""
        today = date.today().isoformat()
        
        # Get today's completed tasks count
        cursor = self.conn.execute("""
            SELECT COUNT(*) as count
            FROM tasks
            WHERE DATE(completed_at) = ?
        """, (today,))
        completed_count = cursor.fetchone()['count']
        
        # Get today's focus minutes
        cursor = self.conn.execute("""
            SELECT SUM(duration) as total
            FROM focus_sessions
            WHERE DATE(started_at) = ?
        """, (today,))
        focus_minutes = cursor.fetchone()['total'] or 0
        
        # Upsert daily stats
        self.conn.execute("""
            INSERT INTO daily_stats (date, tasks_completed, focus_minutes)
            VALUES (?, ?, ?)
            ON CONFLICT(date) DO UPDATE SET
                tasks_completed = ?,
                focus_minutes = ?
        """, (today, completed_count, focus_minutes, completed_count, focus_minutes))
        self.conn.commit()
    
    def close(self):
        """Close database connection."""
        if self.conn:
            self.conn.close()
