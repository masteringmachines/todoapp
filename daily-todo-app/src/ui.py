"""
Terminal UI components for the Daily Todo App.
Beautiful, colorful, and interactive interface using Rich library.
"""

from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.layout import Layout
from rich.text import Text
from rich.prompt import Prompt, Confirm
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.live import Live
from rich import box
from typing import List, Dict, Optional
import time

from src.time_context import TimeContext, TimeOfDay, EnergyLevel


class TodoUI:
    """Rich terminal UI for the todo app."""
    
    def __init__(self):
        """Initialize the UI."""
        self.console = Console()
        self.time_context = TimeContext()
        self.current_energy = EnergyLevel.MEDIUM
    
    def clear(self):
        """Clear the console."""
        self.console.clear()
    
    def show_header(self, title: str = "DAILY TODO APP"):
        """Display app header with time-based styling."""
        tod = self.time_context.get_time_of_day()
        colors = self.time_context.get_theme_colors()
        greeting = self.time_context.get_greeting()
        
        # Create header text
        header = Text()
        header.append(f"\n{title}\n", style=f"bold {colors['primary']}")
        header.append(f"{greeting}\n", style=colors['secondary'])
        
        # Add time/energy status
        status = Text()
        energy_emoji = self.time_context.get_energy_emoji(self.current_energy.value)
        status.append(f"\nCurrent Energy: {energy_emoji} {self.current_energy.value.title()}", 
                     style=colors['accent'])
        
        panel = Panel(
            header + status,
            border_style=colors['primary'],
            box=box.DOUBLE,
            padding=(1, 2)
        )
        
        self.console.print(panel)
    
    def show_main_menu(self, streak: int = 0, completed: int = 0, total: int = 0) -> str:
        """Display main menu and get user choice."""
        colors = self.time_context.get_theme_colors()
        
        # Show stats banner
        stats = Text()
        if streak > 0:
            stats.append(f"🔥 Streak: {streak} days  ", style="bold yellow")
        stats.append(f"✓ Today: {completed}/{total} tasks", style="bold green")
        self.console.print(Panel(stats, border_style=colors['accent']))
        
        # Menu options
        menu = Table(show_header=False, box=box.SIMPLE, padding=(0, 2))
        menu.add_column("Option", style=colors['primary'])
        menu.add_column("Description", style=colors['text'])
        
        options = [
            ("1", "📋 View Tasks", "See all your tasks"),
            ("2", "➕ Add New Task", "Create a new task"),
            ("3", "✅ Complete Task", "Mark a task as done"),
            ("4", "🎯 Focus Mode", "Start a focus session"),
            ("5", "⚡ Set Energy Level", "Update your energy state"),
            ("6", "📊 View Statistics", "See your progress"),
            ("7", "❌ Delete Task", "Remove a task"),
            ("8", "🌙 Quit", "Exit the app")
        ]
        
        for num, icon_title, desc in options:
            menu.add_row(f"{num}.", f"{icon_title}", desc)
        
        self.console.print("\n")
        self.console.print(menu)
        self.console.print("\n")
        
        choice = Prompt.ask(
            "Choose an option",
            choices=["1", "2", "3", "4", "5", "6", "7", "8"],
            default="1"
        )
        
        return choice
    
    def show_tasks(self, tasks: List[Dict], title: str = "Your Tasks"):
        """Display tasks in a beautiful table."""
        if not tasks:
            self.console.print(Panel(
                "[yellow]No tasks found. Add some tasks to get started![/yellow]",
                title="📋 Tasks",
                border_style="yellow"
            ))
            return
        
        colors = self.time_context.get_theme_colors()
        
        # Create table
        table = Table(
            title=f"📋 {title}",
            box=box.ROUNDED,
            border_style=colors['primary'],
            show_lines=True
        )
        
        table.add_column("ID", style="cyan", width=4)
        table.add_column("Task", style="white", width=40)
        table.add_column("Priority", justify="center", width=12)
        table.add_column("Energy", justify="center", width=10)
        table.add_column("Category", width=12)
        table.add_column("Due", width=12)
        
        for task in tasks:
            # Get emojis
            priority_emoji = self.time_context.get_priority_emoji(task['priority'])
            energy_emoji = self.time_context.get_energy_emoji(task['energy_level'])
            category_emoji = self.time_context.get_category_emoji(task['category'])
            
            # Priority color
            priority_colors = {
                'low': 'blue',
                'medium': 'yellow',
                'high': 'red',
                'urgent': 'bold red'
            }
            priority_color = priority_colors.get(task['priority'], 'white')
            
            # Format title
            title = task['title']
            if len(title) > 38:
                title = title[:35] + "..."
            
            # Due date formatting
            due_date = task.get('due_date', '-')
            if due_date and due_date != '-':
                from datetime import datetime
                try:
                    due = datetime.fromisoformat(due_date).date()
                    today = datetime.now().date()
                    if due < today:
                        due_date = f"[red]⚠️ {due_date}[/red]"
                    elif due == today:
                        due_date = f"[yellow]📅 Today[/yellow]"
                except:
                    pass
            
            table.add_row(
                str(task['id']),
                title,
                f"{priority_emoji} [{priority_color}]{task['priority']}[/{priority_color}]",
                f"{energy_emoji} {task['energy_level']}",
                f"{category_emoji} {task['category']}",
                due_date
            )
        
        self.console.print("\n")
        self.console.print(table)
        self.console.print("\n")
    
    def show_recommendations(self, tasks: List[Dict], energy_level: EnergyLevel):
        """Show task recommendations based on context."""
        tod = self.time_context.get_time_of_day()
        recommendations = self.time_context.get_recommendations(tod, energy_level)
        colors = self.time_context.get_theme_colors()
        
        # Create recommendation panel
        content = Text()
        content.append(f"💡 {recommendations['message']}\n\n", style=f"bold {colors['accent']}")
        content.append("Recommended for you right now:\n", style=colors['secondary'])
        
        # Suggest specific tasks
        suggested = self.time_context.suggest_tasks(tasks, energy_level, tod, limit=3)
        
        if suggested:
            for i, task in enumerate(suggested, 1):
                priority_emoji = self.time_context.get_priority_emoji(task['priority'])
                content.append(f"\n{i}. {priority_emoji} {task['title']}", style="bold white")
        else:
            content.append("\nNo matching tasks. Consider adding some!", style="yellow")
        
        # Add tips
        content.append("\n\n✨ Tips:\n", style=f"bold {colors['secondary']}")
        for tip in recommendations['tips'][:2]:
            content.append(f"  • {tip}\n", style=colors['text'])
        
        panel = Panel(
            content,
            title="🎯 Smart Suggestions",
            border_style=colors['accent'],
            box=box.ROUNDED
        )
        
        self.console.print("\n")
        self.console.print(panel)
        self.console.print("\n")
    
    def add_task_form(self) -> Optional[Dict]:
        """Interactive form to add a new task."""
        self.console.print("\n[bold cyan]➕ Add New Task[/bold cyan]\n")
        
        title = Prompt.ask("Task title")
        if not title:
            return None
        
        description = Prompt.ask("Description (optional)", default="")
        
        priority = Prompt.ask(
            "Priority",
            choices=["low", "medium", "high", "urgent"],
            default="medium"
        )
        
        energy = Prompt.ask(
            "Energy level required",
            choices=["low", "medium", "high"],
            default="medium"
        )
        
        category = Prompt.ask(
            "Category",
            choices=["work", "personal", "health", "learning", "outdoor", "indoor"],
            default="personal"
        )
        
        add_due = Confirm.ask("Add due date?", default=False)
        due_date = None
        if add_due:
            due_date = Prompt.ask("Due date (YYYY-MM-DD)")
        
        add_estimate = Confirm.ask("Add time estimate?", default=False)
        time_estimate = None
        if add_estimate:
            time_estimate = int(Prompt.ask("Estimated minutes", default="30"))
        
        return {
            'title': title,
            'description': description,
            'priority': priority,
            'energy_level': energy,
            'category': category,
            'due_date': due_date,
            'time_estimate': time_estimate
        }
    
    def complete_task_form(self) -> tuple:
        """Form to complete a task with mood logging."""
        task_id = Prompt.ask("Enter task ID to complete")
        
        log_mood = Confirm.ask("Log your mood?", default=True)
        mood = None
        
        if log_mood:
            mood = Prompt.ask(
                "How do you feel?",
                choices=["happy", "neutral", "tired", "stressed", "accomplished"],
                default="happy"
            )
        
        return int(task_id), mood
    
    def show_stats(self, stats: Dict):
        """Display statistics dashboard."""
        colors = self.time_context.get_theme_colors()
        
        # Create stats layout
        layout = Layout()
        layout.split_column(
            Layout(name="tasks", size=8),
            Layout(name="focus", size=8),
            Layout(name="mood", size=10)
        )
        
        # Task stats
        task_stats = stats['tasks']
        task_panel = Panel(
            f"✅ Tasks Completed: [bold green]{task_stats.get('total_completed', 0)}[/bold green]\n"
            f"🔥 Current Streak: [bold yellow]{stats['streak']} days[/bold yellow]",
            title="📊 Task Statistics",
            border_style=colors['primary']
        )
        layout["tasks"].update(task_panel)
        
        # Focus stats
        focus_stats = stats['focus']
        focus_mins = focus_stats.get('total_focus_minutes', 0) or 0
        focus_sessions = focus_stats.get('total_sessions', 0) or 0
        focus_panel = Panel(
            f"⏱️  Total Focus Time: [bold cyan]{focus_mins} minutes[/bold cyan]\n"
            f"🎯 Focus Sessions: [bold cyan]{focus_sessions}[/bold cyan]",
            title="⚡ Focus Statistics",
            border_style=colors['secondary']
        )
        layout["focus"].update(focus_panel)
        
        # Mood stats
        mood_stats = stats['moods']
        mood_text = Text()
        mood_text.append("Your Recent Moods:\n\n", style="bold")
        
        if mood_stats:
            for mood, count in mood_stats.items():
                emoji = self.time_context.get_mood_emoji(mood)
                mood_text.append(f"{emoji} {mood.title()}: {count} times\n")
        else:
            mood_text.append("No mood data yet. Complete tasks and log your mood!", style="yellow")
        
        mood_panel = Panel(
            mood_text,
            title="😊 Mood Tracking",
            border_style=colors['accent']
        )
        layout["mood"].update(mood_panel)
        
        self.console.print("\n")
        self.console.print(layout)
        self.console.print("\n")
    
    def show_focus_mode(self, task_title: str, duration: int = 25):
        """Display focus mode timer with progress bar."""
        colors = self.time_context.get_theme_colors()
        
        self.console.print(Panel(
            f"🎯 [bold]Focus Session Started![/bold]\n\n"
            f"Task: {task_title}\n"
            f"Duration: {duration} minutes\n\n"
            f"[dim]Stay focused. You've got this![/dim]",
            border_style=colors['accent'],
            box=box.DOUBLE
        ))
        
        # Progress bar
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            transient=False,
        ) as progress:
            task = progress.add_task(
                f"[{colors['primary']}]Focusing...",
                total=duration * 60
            )
            
            for i in range(duration * 60):
                time.sleep(1)
                progress.update(task, advance=1)
        
        self.console.print(Panel(
            "🎉 [bold green]Focus session complete![/bold green]\n\n"
            "Great work! Take a 5-minute break.",
            border_style="green"
        ))
    
    def set_energy_level(self) -> EnergyLevel:
        """Prompt user to set their energy level."""
        colors = self.time_context.get_theme_colors()
        
        self.console.print(f"\n[{colors['primary']}]⚡ Set Your Energy Level[/{colors['primary']}]\n")
        
        energy = Prompt.ask(
            "How energized do you feel right now?",
            choices=["low", "medium", "high"],
            default="medium"
        )
        
        self.current_energy = EnergyLevel(energy)
        
        emoji = self.time_context.get_energy_emoji(energy)
        self.console.print(f"\n{emoji} Energy level set to: [bold]{energy.title()}[/bold]\n")
        
        return self.current_energy
    
    def show_success(self, message: str):
        """Show success message."""
        self.console.print(f"\n✅ [bold green]{message}[/bold green]\n")
    
    def show_error(self, message: str):
        """Show error message."""
        self.console.print(f"\n❌ [bold red]Error: {message}[/bold red]\n")
    
    def show_info(self, message: str):
        """Show info message."""
        self.console.print(f"\nℹ️  [cyan]{message}[/cyan]\n")
    
    def confirm(self, message: str) -> bool:
        """Ask for confirmation."""
        return Confirm.ask(message)
    
    def pause(self):
        """Pause and wait for user input."""
        Prompt.ask("\nPress Enter to continue")
