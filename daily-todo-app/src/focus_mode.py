"""
Focus mode implementation with Pomodoro technique.
"""

import time
from datetime import datetime, timedelta
from typing import Optional


class FocusMode:
    """Pomodoro-style focus sessions."""
    
    def __init__(self, work_duration: int = 25, short_break: int = 5, 
                 long_break: int = 15, sessions_before_long_break: int = 4):
        """
        Initialize focus mode settings.
        
        Args:
            work_duration: Work session length in minutes (default: 25)
            short_break: Short break length in minutes (default: 5)
            long_break: Long break length in minutes (default: 15)
            sessions_before_long_break: Number of sessions before long break (default: 4)
        """
        self.work_duration = work_duration
        self.short_break = short_break
        self.long_break = long_break
        self.sessions_before_long_break = sessions_before_long_break
        self.sessions_completed = 0
    
    def start_work_session(self, task_id: Optional[int] = None) -> dict:
        """
        Start a work session.
        
        Args:
            task_id: Optional task ID to associate with this session
            
        Returns:
            Session info dict
        """
        start_time = datetime.now()
        end_time = start_time + timedelta(minutes=self.work_duration)
        
        return {
            'type': 'work',
            'task_id': task_id,
            'duration': self.work_duration,
            'start_time': start_time,
            'end_time': end_time,
            'session_number': self.sessions_completed + 1
        }
    
    def complete_session(self):
        """Mark a session as completed."""
        self.sessions_completed += 1
    
    def get_break_duration(self) -> int:
        """
        Get the appropriate break duration.
        
        Returns:
            Break duration in minutes
        """
        if self.sessions_completed % self.sessions_before_long_break == 0:
            return self.long_break
        return self.short_break
    
    def should_take_long_break(self) -> bool:
        """Check if it's time for a long break."""
        return self.sessions_completed > 0 and \
               self.sessions_completed % self.sessions_before_long_break == 0
    
    def get_next_break_type(self) -> str:
        """Get the type of next break."""
        if self.should_take_long_break():
            return "long"
        return "short"
    
    def reset_sessions(self):
        """Reset session counter."""
        self.sessions_completed = 0
    
    def get_session_stats(self) -> dict:
        """Get statistics about completed sessions."""
        total_work_time = self.sessions_completed * self.work_duration
        long_breaks_taken = self.sessions_completed // self.sessions_before_long_break
        short_breaks_taken = self.sessions_completed - long_breaks_taken
        
        total_break_time = (
            long_breaks_taken * self.long_break +
            short_breaks_taken * self.short_break
        )
        
        return {
            'sessions_completed': self.sessions_completed,
            'total_work_minutes': total_work_time,
            'total_break_minutes': total_break_time,
            'long_breaks': long_breaks_taken,
            'short_breaks': short_breaks_taken,
            'next_break_type': self.get_next_break_type()
        }


class FocusTimer:
    """Timer utility for focus sessions."""
    
    @staticmethod
    def countdown(minutes: int, callback=None):
        """
        Run a countdown timer.
        
        Args:
            minutes: Duration in minutes
            callback: Optional callback function called each second
        """
        total_seconds = minutes * 60
        
        for remaining in range(total_seconds, -1, -1):
            mins, secs = divmod(remaining, 60)
            
            if callback:
                callback(mins, secs, remaining, total_seconds)
            
            time.sleep(1)
    
    @staticmethod
    def format_time(minutes: int, seconds: int) -> str:
        """Format time as MM:SS."""
        return f"{minutes:02d}:{seconds:02d}"
    
    @staticmethod
    def get_progress_bar(current: int, total: int, width: int = 50) -> str:
        """
        Generate a text progress bar.
        
        Args:
            current: Current progress
            total: Total amount
            width: Width of progress bar
            
        Returns:
            Progress bar string
        """
        progress = int((current / total) * width)
        bar = "█" * progress + "░" * (width - progress)
        percentage = int((current / total) * 100)
        return f"[{bar}] {percentage}%"
