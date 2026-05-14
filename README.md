# ✅ Daily Todo App

A clean, Python-powered daily task manager to help you organize, track, and complete your to-do list. Built with simplicity in mind — get things done without the clutter.

## ✨ Features

- **Create Tasks**: Add tasks with titles, optional descriptions, and due dates
- **Mark Complete**: Check off tasks as you finish them
- **Daily View**: See what's on your plate for today at a glance
- **Persistent Storage**: Your tasks are saved between sessions
- **Simple Interface**: Lightweight CLI or web UI — no overhead

## 🛠️ Tech Stack

- Python 3.10+
- SQLite (local task storage)
- (Optional) Flask / FastAPI for a web interface

## 📁 Project Structure

```
todoapp/
└── daily-todo-app/
    ├── main.py           # App entry point
    ├── models.py         # Task data models
    ├── storage.py        # SQLite persistence layer
    ├── cli.py            # Command-line interface
    └── requirements.txt
```

## 🚀 Getting Started

### Prerequisites

- Python 3.10+

### Installation

```bash
git clone https://github.com/masteringmachines/todoapp.git
cd todoapp/daily-todo-app
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### Run

```bash
python main.py
```

## 🖥️ Usage

```bash
# Add a new task
python main.py add "Buy groceries"

# List today's tasks
python main.py list

# Mark a task complete
python main.py done 1

# Remove a task
python main.py remove 1

# Show all tasks (including completed)
python main.py list --all
```

## 💡 Example

```
$ python main.py list

📋 Today's Tasks
─────────────────────────────
[ ] 1. Buy groceries
[ ] 2. Review pull requests
[✓] 3. Morning run

2 remaining / 1 completed
```

## 🤝 Contributing

Got ideas for features like priority levels, categories, or reminders? Open a PR or issue!

## 📝 License

MIT
