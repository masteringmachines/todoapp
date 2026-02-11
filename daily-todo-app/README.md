# Daily Elements Todo App 🌅

A unique todo application that adapts to your daily rhythm, energy levels, weather, and time of day. Built with Python and a beautiful terminal UI.

![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

## ✨ Unique Features

### 🌞 Time-Based Intelligence
- **Morning Mode** (6am-12pm): Focus on planning and high-priority tasks
- **Afternoon Mode** (12pm-6pm): Peak productivity hours
- **Evening Mode** (6pm-10pm): Lighter tasks and reflection
- **Night Mode** (10pm-6am): Minimal tasks, rest focus

### ⚡ Energy Level Tracking
- Track your current energy (Low, Medium, High)
- Get task recommendations based on energy state
- Tasks tagged with energy requirements
- Smart task filtering by energy level

### 🌤️ Weather Context
- Indoor/Outdoor task suggestions based on weather
- Weather emoji indicators
- Automatic task filtering by weather conditions

### 🎯 Focus Mode
- Built-in Pomodoro timer
- 25-minute focus sessions
- Break reminders
- Session tracking

### 😊 Mood Tracking
- Log your mood when completing tasks
- Track emotional patterns
- Weekly mood summaries

### 🔥 Gamification
- Daily completion streaks
- Task completion stats
- Progress tracking
- Achievement system

### 🎨 Beautiful Terminal UI
- Color-coded priorities
- Rich panels and tables
- Live updates
- Smooth animations
- Interactive menus

## 📦 Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/daily-todo-app.git
cd daily-todo-app

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

## 🚀 Quick Start

```bash
# Run the app
python main.py

# Or use the CLI directly
python main.py add "Write project report" --priority high --energy high
python main.py list --filter today
python main.py complete 1
```

## 📖 Usage

### Interactive Mode
Simply run `python main.py` to enter the interactive TUI (Terminal User Interface).

**Navigation:**
- Use **number keys** to select menu options
- Use **arrow keys** to navigate lists
- Press **q** to quit
- Press **h** for help

### CLI Mode

**Add a task:**
```bash
python main.py add "Task description" --priority high --energy medium --category outdoor
```

**List tasks:**
```bash
python main.py list                    # All active tasks
python main.py list --filter today     # Today's tasks
python main.py list --filter week      # This week's tasks
python main.py list --energy high      # High energy tasks
```

**Complete a task:**
```bash
python main.py complete 1 --mood happy
```

**Delete a task:**
```bash
python main.py delete 1
```

**View statistics:**
```bash
python main.py stats
```

**Start focus mode:**
```bash
python main.py focus
```

### Task Properties

- **Priority**: low, medium, high, urgent
- **Energy Level**: low, medium, high
- **Category**: work, personal, health, learning, outdoor, indoor
- **Due Date**: YYYY-MM-DD format
- **Time Estimate**: minutes

## 🎯 Features Guide

### Time of Day Modes

The app automatically adapts based on current time:

**🌅 Morning (6am-12pm)**
- Suggests planning and high-priority tasks
- Best for: Strategic work, important decisions
- UI Theme: Bright, energetic colors

**☀️ Afternoon (12pm-6pm)**
- Peak productivity period
- Best for: Deep work, challenging tasks
- UI Theme: Professional, focused colors

**🌆 Evening (6pm-10pm)**
- Lighter tasks and wrap-up
- Best for: Admin tasks, planning tomorrow
- UI Theme: Warm, calming colors

**🌙 Night (10pm-6am)**
- Rest and minimal tasks
- Best for: Light reading, journaling
- UI Theme: Dark, relaxing colors

### Energy Level System

Tasks are tagged with energy requirements:

- **🔴 High Energy**: Complex problem-solving, creative work
- **🟡 Medium Energy**: Regular work tasks, meetings
- **🟢 Low Energy**: Admin work, email, light tasks

The app suggests tasks matching your current energy level.

### Weather Integration

Tasks can be categorized by weather suitability:

- **☀️ Outdoor Tasks**: Errands, exercise, photography
- **🏠 Indoor Tasks**: Computer work, reading, cleaning
- **☁️ Any Weather**: Phone calls, planning, writing

### Focus Mode (Pomodoro)

1. Start a 25-minute focus session
2. Work on selected task
3. Take a 5-minute break
4. Repeat 4 times, then take a 15-minute break

Benefits:
- Improved concentration
- Better time management
- Reduced burnout
- Track focused work time

### Mood Tracking

When completing tasks, log your mood:
- 😊 Happy
- 😐 Neutral
- 😔 Tired
- 😤 Stressed
- 🎉 Accomplished

View mood patterns in weekly summaries.

## 📊 Example Workflow

```bash
# Morning routine
python main.py
# > Set energy level: High
# > View morning tasks
# > Start focus session on priority task

# Afternoon
# > Add new tasks from meetings
# > Complete tasks as you go
# > Log mood with each completion

# Evening
# > Review day's progress
# > Plan tomorrow's tasks
# > Check streak and stats
```

## 🎨 UI Screenshots

```
╔══════════════════════════════════════════════════════════════╗
║                  DAILY TODO APP 🌅                          ║
║                    Good Morning!                             ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║  Current Energy: ⚡ High                                     ║
║  Today's Streak: 🔥 7 days                                   ║
║  Tasks Completed: ✓ 12/15                                   ║
║                                                              ║
╠══════════════════════════════════════════════════════════════╣
║                        MENU                                  ║
║                                                              ║
║  1. 📋 View Tasks                                            ║
║  2. ➕ Add New Task                                          ║
║  3. ✅ Complete Task                                         ║
║  4. 🎯 Focus Mode                                            ║
║  5. ⚡ Set Energy Level                                      ║
║  6. 📊 View Statistics                                       ║
║  7. ❌ Delete Task                                           ║
║  8. 🌙 Quit                                                  ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
```

## 🛠️ Configuration

Create a `config.json` file to customize:

```json
{
  "theme": "auto",
  "default_energy": "medium",
  "focus_duration": 25,
  "break_duration": 5,
  "weather_location": "auto"
}
```

## 📁 Project Structure

```
daily-todo-app/
├── src/
│   ├── __init__.py
│   ├── database.py      # SQLite database management
│   ├── models.py        # Task and data models
│   ├── ui.py            # Terminal UI components
│   ├── time_context.py  # Time-based intelligence
│   ├── focus_mode.py    # Pomodoro timer
│   └── stats.py         # Statistics and tracking
├── tests/
│   └── test_tasks.py
├── data/
│   └── tasks.db         # SQLite database (auto-created)
├── main.py              # Entry point
├── requirements.txt
├── README.md
└── LICENSE
```

## 🧪 Testing

```bash
pytest tests/ -v
```

## 🤝 Contributing

Contributions are welcome! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for details.

## 📝 License

MIT License - See [LICENSE](LICENSE) file

## 🙏 Acknowledgments

- Built with [Rich](https://github.com/Textualize/rich) for beautiful terminal output
- Inspired by GTD (Getting Things Done) methodology
- Weather data from OpenWeatherMap API

## 🔮 Future Features

- [ ] Cloud sync
- [ ] Mobile companion app
- [ ] Task templates
- [ ] Habit tracking
- [ ] Team collaboration
- [ ] Calendar integration
- [ ] Voice input
- [ ] AI-powered task suggestions

## 💡 Tips

1. **Start your day by setting your energy level**
2. **Use focus mode for important tasks**
3. **Review your stats weekly for insights**
4. **Keep tasks specific and actionable**
5. **Use categories to organize by context**
6. **Log your mood to identify patterns**

---

Made with ❤️ and ☕ for productive people who value their time and energy.
