"""
Time-based context and intelligence for the Daily Todo App.
Provides recommendations based on time of day, energy levels, and other factors.
"""

from datetime import datetime, time
from typing import List, Dict, Tuple
from enum import Enum


class TimeOfDay(Enum):
    """Time periods throughout the day."""
    MORNING = "morning"
    AFTERNOON = "afternoon"
    EVENING = "evening"
    NIGHT = "night"


class EnergyLevel(Enum):
    """Energy level states."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class Priority(Enum):
    """Task priority levels."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    URGENT = "urgent"


class TimeContext:
    """Provides time-based intelligence and recommendations."""
    
    @staticmethod
    def get_time_of_day() -> TimeOfDay:
        """Determine current time of day period."""
        now = datetime.now().time()
        
        if time(6, 0) <= now < time(12, 0):
            return TimeOfDay.MORNING
        elif time(12, 0) <= now < time(18, 0):
            return TimeOfDay.AFTERNOON
        elif time(18, 0) <= now < time(22, 0):
            return TimeOfDay.EVENING
        else:
            return TimeOfDay.NIGHT
    
    @staticmethod
    def get_greeting() -> str:
        """Get a time-appropriate greeting."""
        tod = TimeContext.get_time_of_day()
        
        greetings = {
            TimeOfDay.MORNING: "Good Morning! 🌅",
            TimeOfDay.AFTERNOON: "Good Afternoon! ☀️",
            TimeOfDay.EVENING: "Good Evening! 🌆",
            TimeOfDay.NIGHT: "Good Night! 🌙"
        }
        
        return greetings[tod]
    
    @staticmethod
    def get_theme_colors() -> Dict[str, str]:
        """Get color scheme based on time of day."""
        tod = TimeContext.get_time_of_day()
        
        themes = {
            TimeOfDay.MORNING: {
                'primary': 'bright_yellow',
                'secondary': 'cyan',
                'accent': 'bright_green',
                'text': 'white'
            },
            TimeOfDay.AFTERNOON: {
                'primary': 'bright_blue',
                'secondary': 'blue',
                'accent': 'cyan',
                'text': 'white'
            },
            TimeOfDay.EVENING: {
                'primary': 'bright_magenta',
                'secondary': 'magenta',
                'accent': 'yellow',
                'text': 'white'
            },
            TimeOfDay.NIGHT: {
                'primary': 'blue',
                'secondary': 'bright_black',
                'accent': 'cyan',
                'text': 'bright_white'
            }
        }
        
        return themes[tod]
    
    @staticmethod
    def get_recommendations(time_of_day: TimeOfDay, energy_level: EnergyLevel) -> Dict:
        """Get task recommendations based on time and energy."""
        recommendations = {
            (TimeOfDay.MORNING, EnergyLevel.HIGH): {
                'message': "Perfect time for strategic planning and important decisions!",
                'suggested_categories': ['work', 'learning', 'planning'],
                'suggested_priorities': ['high', 'urgent'],
                'tips': [
                    "Tackle your most important task first",
                    "Set your intentions for the day",
                    "Review your goals"
                ]
            },
            (TimeOfDay.MORNING, EnergyLevel.MEDIUM): {
                'message': "Good morning energy! Start with a warm-up task.",
                'suggested_categories': ['work', 'personal', 'health'],
                'suggested_priorities': ['medium', 'high'],
                'tips': [
                    "Begin with a quick win",
                    "Review your task list",
                    "Organize your workspace"
                ]
            },
            (TimeOfDay.MORNING, EnergyLevel.LOW): {
                'message': "Take it easy this morning. Light tasks to start.",
                'suggested_categories': ['personal', 'health'],
                'suggested_priorities': ['low', 'medium'],
                'tips': [
                    "Do some light stretching",
                    "Have a healthy breakfast",
                    "Start with simple tasks"
                ]
            },
            (TimeOfDay.AFTERNOON, EnergyLevel.HIGH): {
                'message': "Peak productivity time! Tackle your hardest tasks.",
                'suggested_categories': ['work', 'learning', 'outdoor'],
                'suggested_priorities': ['high', 'urgent'],
                'tips': [
                    "Enter deep work mode",
                    "Minimize distractions",
                    "Use focus sessions"
                ]
            },
            (TimeOfDay.AFTERNOON, EnergyLevel.MEDIUM): {
                'message': "Solid working hours. Mix challenging and routine tasks.",
                'suggested_categories': ['work', 'personal', 'learning'],
                'suggested_priorities': ['medium', 'high'],
                'tips': [
                    "Alternate between task types",
                    "Take short breaks",
                    "Stay hydrated"
                ]
            },
            (TimeOfDay.AFTERNOON, EnergyLevel.LOW): {
                'message': "Afternoon slump? Try lighter tasks or take a break.",
                'suggested_categories': ['personal', 'indoor'],
                'suggested_priorities': ['low', 'medium'],
                'tips': [
                    "Take a short walk",
                    "Do some easy admin work",
                    "Have a healthy snack"
                ]
            },
            (TimeOfDay.EVENING, EnergyLevel.HIGH): {
                'message': "Still energized! Great time for creative work.",
                'suggested_categories': ['learning', 'personal', 'work'],
                'suggested_priorities': ['medium', 'high'],
                'tips': [
                    "Work on passion projects",
                    "Learn something new",
                    "Connect with others"
                ]
            },
            (TimeOfDay.EVENING, EnergyLevel.MEDIUM): {
                'message': "Winding down. Focus on wrapping up and planning.",
                'suggested_categories': ['personal', 'work', 'planning'],
                'suggested_priorities': ['low', 'medium'],
                'tips': [
                    "Review today's accomplishments",
                    "Plan tomorrow",
                    "Tidy your workspace"
                ]
            },
            (TimeOfDay.EVENING, EnergyLevel.LOW): {
                'message': "Time to relax. Light tasks and self-care.",
                'suggested_categories': ['personal', 'health'],
                'suggested_priorities': ['low'],
                'tips': [
                    "Do a calming activity",
                    "Prepare for tomorrow",
                    "Get ready for bed"
                ]
            },
            (TimeOfDay.NIGHT, EnergyLevel.HIGH): {
                'message': "Late energy burst? Quick tasks only, then rest.",
                'suggested_categories': ['personal', 'learning'],
                'suggested_priorities': ['low', 'medium'],
                'tips': [
                    "Journal your thoughts",
                    "Light reading",
                    "Avoid screens soon"
                ]
            },
            (TimeOfDay.NIGHT, EnergyLevel.MEDIUM): {
                'message': "Getting late. Minimal tasks, prepare for rest.",
                'suggested_categories': ['personal'],
                'suggested_priorities': ['low'],
                'tips': [
                    "Wind down routine",
                    "Set intentions for tomorrow",
                    "Practice gratitude"
                ]
            },
            (TimeOfDay.NIGHT, EnergyLevel.LOW): {
                'message': "Time for rest. Focus on sleep preparation.",
                'suggested_categories': ['health', 'personal'],
                'suggested_priorities': ['low'],
                'tips': [
                    "Prepare for bed",
                    "Avoid screens",
                    "Create a calming environment"
                ]
            }
        }
        
        return recommendations.get(
            (time_of_day, energy_level),
            {
                'message': "Let's make today productive!",
                'suggested_categories': ['work', 'personal'],
                'suggested_priorities': ['medium'],
                'tips': ["Stay focused", "Take breaks", "Stay hydrated"]
            }
        )
    
    @staticmethod
    def suggest_tasks(tasks: List[Dict], energy_level: EnergyLevel, 
                     time_of_day: TimeOfDay, limit: int = 5) -> List[Dict]:
        """Suggest most appropriate tasks based on current context."""
        recommendations = TimeContext.get_recommendations(time_of_day, energy_level)
        suggested_categories = recommendations['suggested_categories']
        suggested_priorities = recommendations['suggested_priorities']
        
        # Score tasks based on context match
        scored_tasks = []
        for task in tasks:
            score = 0
            
            # Match energy level
            if task.get('energy_level') == energy_level.value:
                score += 3
            
            # Match category
            if task.get('category') in suggested_categories:
                score += 2
            
            # Match priority
            if task.get('priority') in suggested_priorities:
                score += 1
            
            # Boost urgent tasks
            if task.get('priority') == 'urgent':
                score += 2
            
            # Boost tasks due today
            if task.get('due_date') == datetime.now().date().isoformat():
                score += 3
            
            scored_tasks.append((score, task))
        
        # Sort by score and return top N
        scored_tasks.sort(key=lambda x: x[0], reverse=True)
        return [task for score, task in scored_tasks[:limit]]
    
    @staticmethod
    def get_energy_emoji(energy_level: str) -> str:
        """Get emoji for energy level."""
        emojis = {
            'low': '🔋',
            'medium': '⚡',
            'high': '🔥'
        }
        return emojis.get(energy_level, '⚡')
    
    @staticmethod
    def get_priority_emoji(priority: str) -> str:
        """Get emoji for priority level."""
        emojis = {
            'low': '🔵',
            'medium': '🟡',
            'high': '🔴',
            'urgent': '🚨'
        }
        return emojis.get(priority, '🟡')
    
    @staticmethod
    def get_category_emoji(category: str) -> str:
        """Get emoji for category."""
        emojis = {
            'work': '💼',
            'personal': '🏠',
            'health': '💪',
            'learning': '📚',
            'outdoor': '🌳',
            'indoor': '🏠',
            'planning': '📋'
        }
        return emojis.get(category, '📝')
    
    @staticmethod
    def get_mood_emoji(mood: str) -> str:
        """Get emoji for mood."""
        emojis = {
            'happy': '😊',
            'neutral': '😐',
            'tired': '😔',
            'stressed': '😤',
            'accomplished': '🎉'
        }
        return emojis.get(mood, '😊')
