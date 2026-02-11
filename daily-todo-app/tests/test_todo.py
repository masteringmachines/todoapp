"""
Unit tests for the Daily Todo App.
"""

import pytest
import sys
from pathlib import Path
from datetime import datetime, date

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.database import Database
from src.time_context import TimeContext, TimeOfDay, EnergyLevel
from src.focus_mode import FocusMode


class TestDatabase:
    """Test database operations."""
    
    @pytest.fixture
    def db(self, tmp_path):
        """Create a test database."""
        db_path = tmp_path / "test.db"
        return Database(str(db_path))
    
    def test_add_task(self, db):
        """Test adding a task."""
        task_id = db.add_task(
            title="Test Task",
            description="Test Description",
            priority="high",
            energy_level="medium"
        )
        assert task_id > 0
        
        task = db.get_task(task_id)
        assert task['title'] == "Test Task"
        assert task['priority'] == "high"
    
    def test_get_tasks(self, db):
        """Test retrieving tasks."""
        db.add_task("Task 1", priority="high")
        db.add_task("Task 2", priority="low")
        
        tasks = db.get_tasks(completed=False)
        assert len(tasks) == 2
    
    def test_complete_task(self, db):
        """Test completing a task."""
        task_id = db.add_task("Test Task")
        db.complete_task(task_id, mood="happy")
        
        task = db.get_task(task_id)
        assert task['completed'] == 1
        assert task['mood'] == "happy"
    
    def test_delete_task(self, db):
        """Test deleting a task."""
        task_id = db.add_task("Test Task")
        db.delete_task(task_id)
        
        task = db.get_task(task_id)
        assert task is None
    
    def test_update_task(self, db):
        """Test updating a task."""
        task_id = db.add_task("Test Task", priority="low")
        db.update_task(task_id, priority="high", title="Updated Task")
        
        task = db.get_task(task_id)
        assert task['priority'] == "high"
        assert task['title'] == "Updated Task"
    
    def test_focus_session(self, db):
        """Test logging focus sessions."""
        task_id = db.add_task("Focus Task")
        db.add_focus_session(task_id, 25, completed=True)
        
        sessions = db.get_focus_sessions(days=1)
        assert len(sessions) == 1
        assert sessions[0]['duration'] == 25
    
    def test_stats(self, db):
        """Test statistics retrieval."""
        task_id = db.add_task("Task 1")
        db.complete_task(task_id, mood="happy")
        
        stats = db.get_stats(days=7)
        assert stats['tasks']['total_completed'] == 1
        assert 'happy' in stats['moods']


class TestTimeContext:
    """Test time-based intelligence."""
    
    def test_time_of_day_detection(self):
        """Test time of day detection."""
        tod = TimeContext.get_time_of_day()
        assert isinstance(tod, TimeOfDay)
    
    def test_greeting_generation(self):
        """Test greeting generation."""
        greeting = TimeContext.get_greeting()
        assert len(greeting) > 0
        assert any(word in greeting.lower() for word in ['morning', 'afternoon', 'evening', 'night'])
    
    def test_theme_colors(self):
        """Test theme color generation."""
        colors = TimeContext.get_theme_colors()
        assert 'primary' in colors
        assert 'secondary' in colors
        assert 'accent' in colors
    
    def test_recommendations(self):
        """Test recommendation generation."""
        rec = TimeContext.get_recommendations(TimeOfDay.MORNING, EnergyLevel.HIGH)
        assert 'message' in rec
        assert 'suggested_categories' in rec
        assert 'tips' in rec
    
    def test_emoji_generation(self):
        """Test emoji generation."""
        energy_emoji = TimeContext.get_energy_emoji('high')
        assert len(energy_emoji) > 0
        
        priority_emoji = TimeContext.get_priority_emoji('urgent')
        assert len(priority_emoji) > 0
        
        mood_emoji = TimeContext.get_mood_emoji('happy')
        assert len(mood_emoji) > 0
    
    def test_task_suggestions(self):
        """Test task suggestion algorithm."""
        tasks = [
            {
                'id': 1,
                'title': 'High energy work task',
                'energy_level': 'high',
                'category': 'work',
                'priority': 'high',
                'due_date': date.today().isoformat()
            },
            {
                'id': 2,
                'title': 'Low energy task',
                'energy_level': 'low',
                'category': 'personal',
                'priority': 'low',
                'due_date': None
            }
        ]
        
        suggestions = TimeContext.suggest_tasks(
            tasks,
            EnergyLevel.HIGH,
            TimeOfDay.AFTERNOON,
            limit=2
        )
        
        assert len(suggestions) <= 2
        # High energy task should be suggested first
        if suggestions:
            assert suggestions[0]['id'] == 1


class TestFocusMode:
    """Test focus mode functionality."""
    
    def test_initialization(self):
        """Test focus mode initialization."""
        focus = FocusMode()
        assert focus.work_duration == 25
        assert focus.short_break == 5
        assert focus.long_break == 15
    
    def test_work_session(self):
        """Test work session creation."""
        focus = FocusMode()
        session = focus.start_work_session(task_id=1)
        
        assert session['type'] == 'work'
        assert session['task_id'] == 1
        assert session['duration'] == 25
    
    def test_session_completion(self):
        """Test session completion tracking."""
        focus = FocusMode()
        assert focus.sessions_completed == 0
        
        focus.complete_session()
        assert focus.sessions_completed == 1
    
    def test_break_duration(self):
        """Test break duration calculation."""
        focus = FocusMode()
        
        # First session - short break
        focus.complete_session()
        assert focus.get_break_duration() == 5
        
        # After 4 sessions - long break
        focus.complete_session()
        focus.complete_session()
        focus.complete_session()
        assert focus.get_break_duration() == 15
    
    def test_session_stats(self):
        """Test session statistics."""
        focus = FocusMode()
        focus.complete_session()
        focus.complete_session()
        
        stats = focus.get_session_stats()
        assert stats['sessions_completed'] == 2
        assert stats['total_work_minutes'] == 50
    
    def test_reset(self):
        """Test session reset."""
        focus = FocusMode()
        focus.complete_session()
        focus.complete_session()
        
        focus.reset_sessions()
        assert focus.sessions_completed == 0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
