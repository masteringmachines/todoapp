#!/usr/bin/env python3
"""
Daily Elements Todo App - Main Entry Point
A unique todo app that adapts to your daily rhythm, energy levels, and time of day.
"""

import sys
import click
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

from src.database import Database
from src.ui import TodoUI
from src.time_context import TimeContext, EnergyLevel, TimeOfDay
from src.focus_mode import FocusMode


class TodoApp:
    """Main application controller."""
    
    def __init__(self):
        """Initialize the app."""
        self.db = Database()
        self.ui = TodoUI()
        self.focus_mode = FocusMode()
        self.running = True
    
    def run_interactive(self):
        """Run interactive TUI mode."""
        while self.running:
            try:
                self.ui.clear()
                self.ui.show_header()
                
                # Get stats for header
                stats = self.db.get_stats(days=7)
                active_tasks = self.db.get_tasks(completed=False)
                today_tasks = self.db.get_tasks(completed=False, due_today=True)
                completed_today = len([t for t in self.db.get_tasks(completed=True) 
                                      if t.get('completed_at', '').startswith(
                                          str(Path(__file__).parent))])
                
                # Show menu
                choice = self.ui.show_main_menu(
                    streak=stats['streak'],
                    completed=len(today_tasks),
                    total=len(active_tasks)
                )
                
                # Handle choice
                if choice == "1":
                    self.view_tasks()
                elif choice == "2":
                    self.add_task()
                elif choice == "3":
                    self.complete_task()
                elif choice == "4":
                    self.start_focus_mode()
                elif choice == "5":
                    self.set_energy_level()
                elif choice == "6":
                    self.view_statistics()
                elif choice == "7":
                    self.delete_task()
                elif choice == "8":
                    self.quit_app()
                
            except KeyboardInterrupt:
                self.quit_app()
            except Exception as e:
                self.ui.show_error(f"An error occurred: {e}")
                self.ui.pause()
    
    def view_tasks(self):
        """View and filter tasks."""
        self.ui.clear()
        self.ui.show_header("VIEW TASKS")
        
        # Get tasks
        tasks = self.db.get_tasks(completed=False)
        
        # Show recommendations
        if tasks:
            self.ui.show_recommendations(tasks, self.ui.current_energy)
        
        # Show all tasks
        self.ui.show_tasks(tasks, "All Active Tasks")
        
        self.ui.pause()
    
    def add_task(self):
        """Add a new task."""
        self.ui.clear()
        self.ui.show_header("ADD NEW TASK")
        
        task_data = self.ui.add_task_form()
        
        if task_data:
            task_id = self.db.add_task(**task_data)
            self.ui.show_success(f"Task added successfully! (ID: {task_id})")
        else:
            self.ui.show_info("Task creation cancelled.")
        
        self.ui.pause()
    
    def complete_task(self):
        """Complete a task."""
        self.ui.clear()
        self.ui.show_header("COMPLETE TASK")
        
        # Show active tasks
        tasks = self.db.get_tasks(completed=False)
        self.ui.show_tasks(tasks, "Active Tasks")
        
        if not tasks:
            self.ui.pause()
            return
        
        try:
            task_id, mood = self.ui.complete_task_form()
            
            # Verify task exists
            task = self.db.get_task(task_id)
            if not task:
                self.ui.show_error(f"Task {task_id} not found.")
            elif task['completed']:
                self.ui.show_error(f"Task {task_id} is already completed.")
            else:
                self.db.complete_task(task_id, mood)
                mood_emoji = TimeContext.get_mood_emoji(mood) if mood else "✅"
                self.ui.show_success(f"{mood_emoji} Task completed! Great work!")
        except (ValueError, KeyError) as e:
            self.ui.show_error("Invalid task ID.")
        
        self.ui.pause()
    
    def start_focus_mode(self):
        """Start a Pomodoro focus session."""
        self.ui.clear()
        self.ui.show_header("FOCUS MODE")
        
        # Show active tasks to choose from
        tasks = self.db.get_tasks(completed=False)
        
        if not tasks:
            self.ui.show_info("No active tasks. Add a task first!")
            self.ui.pause()
            return
        
        self.ui.show_tasks(tasks, "Choose a task to focus on")
        
        try:
            from rich.prompt import Prompt
            task_id = int(Prompt.ask("Enter task ID (or 0 for no specific task)", default="0"))
            
            task = None
            task_title = "General Focus Session"
            
            if task_id > 0:
                task = self.db.get_task(task_id)
                if task:
                    task_title = task['title']
                else:
                    self.ui.show_error("Task not found. Starting general session.")
            
            # Start focus session
            self.ui.show_focus_mode(task_title, duration=self.focus_mode.work_duration)
            
            # Log the session
            self.db.add_focus_session(task_id if task else None, 
                                     self.focus_mode.work_duration, 
                                     completed=True)
            self.focus_mode.complete_session()
            
            # Show break suggestion
            break_type = self.focus_mode.get_next_break_type()
            break_duration = self.focus_mode.get_break_duration()
            
            self.ui.show_info(
                f"Take a {break_type} break ({break_duration} minutes). "
                f"Sessions completed: {self.focus_mode.sessions_completed}"
            )
            
        except ValueError:
            self.ui.show_error("Invalid input.")
        
        self.ui.pause()
    
    def set_energy_level(self):
        """Set current energy level."""
        self.ui.clear()
        self.ui.show_header("SET ENERGY LEVEL")
        
        self.ui.set_energy_level()
        
        # Show updated recommendations
        tasks = self.db.get_tasks(completed=False)
        if tasks:
            self.ui.show_recommendations(tasks, self.ui.current_energy)
        
        self.ui.pause()
    
    def view_statistics(self):
        """View statistics and progress."""
        self.ui.clear()
        self.ui.show_header("STATISTICS")
        
        stats = self.db.get_stats(days=7)
        self.ui.show_stats(stats)
        
        self.ui.pause()
    
    def delete_task(self):
        """Delete a task."""
        self.ui.clear()
        self.ui.show_header("DELETE TASK")
        
        # Show all tasks
        tasks = self.db.get_tasks(completed=False)
        self.ui.show_tasks(tasks, "Active Tasks")
        
        if not tasks:
            self.ui.pause()
            return
        
        try:
            from rich.prompt import Prompt
            task_id = int(Prompt.ask("Enter task ID to delete"))
            
            task = self.db.get_task(task_id)
            if not task:
                self.ui.show_error(f"Task {task_id} not found.")
            else:
                if self.ui.confirm(f"Delete task '{task['title']}'?"):
                    self.db.delete_task(task_id)
                    self.ui.show_success("Task deleted successfully!")
                else:
                    self.ui.show_info("Deletion cancelled.")
        except ValueError:
            self.ui.show_error("Invalid task ID.")
        
        self.ui.pause()
    
    def quit_app(self):
        """Quit the application."""
        self.ui.clear()
        self.ui.console.print("\n[bold cyan]Thanks for using Daily Todo App! 🌟[/bold cyan]")
        self.ui.console.print("[dim]Stay productive and take care of yourself![/dim]\n")
        self.running = False
        self.db.close()
        sys.exit(0)


# CLI Commands
@click.group(invoke_without_command=True)
@click.pass_context
def cli(ctx):
    """Daily Elements Todo App - Adapts to your daily rhythm."""
    if ctx.invoked_subcommand is None:
        # Run interactive mode
        app = TodoApp()
        app.run_interactive()


@cli.command()
@click.argument('title')
@click.option('--description', '-d', default='', help='Task description')
@click.option('--priority', '-p', type=click.Choice(['low', 'medium', 'high', 'urgent']), 
              default='medium', help='Task priority')
@click.option('--energy', '-e', type=click.Choice(['low', 'medium', 'high']), 
              default='medium', help='Energy level required')
@click.option('--category', '-c', type=click.Choice(['work', 'personal', 'health', 'learning', 'outdoor', 'indoor']),
              default='personal', help='Task category')
@click.option('--due', help='Due date (YYYY-MM-DD)')
@click.option('--estimate', type=int, help='Time estimate in minutes')
def add(title, description, priority, energy, category, due, estimate):
    """Add a new task."""
    db = Database()
    task_id = db.add_task(
        title=title,
        description=description,
        priority=priority,
        energy_level=energy,
        category=category,
        due_date=due,
        time_estimate=estimate
    )
    click.echo(f"✅ Task added successfully! (ID: {task_id})")
    db.close()


@cli.command()
@click.option('--filter', type=click.Choice(['all', 'today', 'week']), default='all',
              help='Filter tasks')
@click.option('--energy', type=click.Choice(['low', 'medium', 'high']), help='Filter by energy level')
@click.option('--category', help='Filter by category')
def list(filter, energy, category):
    """List tasks."""
    db = Database()
    
    due_today = filter == 'today'
    tasks = db.get_tasks(completed=False, energy_level=energy, category=category, due_today=due_today)
    
    if not tasks:
        click.echo("No tasks found.")
    else:
        for task in tasks:
            priority_emoji = TimeContext.get_priority_emoji(task['priority'])
            energy_emoji = TimeContext.get_energy_emoji(task['energy_level'])
            click.echo(f"{task['id']:3d}. {priority_emoji} {energy_emoji} {task['title']}")
    
    db.close()


@cli.command()
@click.argument('task_id', type=int)
@click.option('--mood', type=click.Choice(['happy', 'neutral', 'tired', 'stressed', 'accomplished']),
              help='Log your mood')
def complete(task_id, mood):
    """Complete a task."""
    db = Database()
    task = db.get_task(task_id)
    
    if not task:
        click.echo(f"❌ Task {task_id} not found.")
    elif task['completed']:
        click.echo(f"❌ Task {task_id} is already completed.")
    else:
        db.complete_task(task_id, mood)
        mood_emoji = TimeContext.get_mood_emoji(mood) if mood else "✅"
        click.echo(f"{mood_emoji} Task completed! Great work!")
    
    db.close()


@cli.command()
@click.argument('task_id', type=int)
def delete(task_id):
    """Delete a task."""
    db = Database()
    task = db.get_task(task_id)
    
    if not task:
        click.echo(f"❌ Task {task_id} not found.")
    else:
        if click.confirm(f"Delete task '{task['title']}'?"):
            db.delete_task(task_id)
            click.echo("✅ Task deleted successfully!")
    
    db.close()


@cli.command()
@click.option('--days', default=7, help='Number of days to analyze')
def stats(days):
    """View statistics."""
    db = Database()
    stats = db.get_stats(days=days)
    
    click.echo(f"\n📊 Statistics (Last {days} days)\n")
    click.echo(f"✅ Tasks Completed: {stats['tasks']['total_completed']}")
    click.echo(f"🔥 Current Streak: {stats['streak']} days")
    click.echo(f"⏱️  Total Focus Time: {stats['focus']['total_focus_minutes'] or 0} minutes")
    click.echo(f"🎯 Focus Sessions: {stats['focus']['total_sessions'] or 0}")
    
    if stats['moods']:
        click.echo(f"\n😊 Mood Distribution:")
        for mood, count in stats['moods'].items():
            emoji = TimeContext.get_mood_emoji(mood)
            click.echo(f"   {emoji} {mood.title()}: {count}")
    
    click.echo()
    db.close()


@cli.command()
@click.option('--duration', default=25, help='Focus duration in minutes')
def focus(duration):
    """Start a focus session."""
    click.echo(f"🎯 Focus session started for {duration} minutes!")
    click.echo("Stay focused. Press Ctrl+C to cancel.\n")
    
    try:
        import time
        for i in range(duration * 60):
            mins, secs = divmod(duration * 60 - i, 60)
            click.echo(f"\rTime remaining: {mins:02d}:{secs:02d}", nl=False)
            time.sleep(1)
        
        click.echo("\n\n🎉 Focus session complete! Take a break.")
        
        # Log session
        db = Database()
        db.add_focus_session(None, duration, completed=True)
        db.close()
        
    except KeyboardInterrupt:
        click.echo("\n\n❌ Focus session cancelled.")


if __name__ == "__main__":
    cli()
