#!/usr/bin/env python3
"""
Todo - Simple CLI todo list.
Usage: python todo.py [--add TASK] [--list] [--done N] [--clear]
Stores tasks in ~/.todo.json
"""

import sys
import os
import json

TODO_FILE = os.path.expanduser('~/.todo.json')

def load():
    if os.path.exists(TODO_FILE):
        with open(TODO_FILE) as f:
            return json.load(f)
    return []

def save(tasks):
    with open(TODO_FILE, 'w') as f:
        json.dump(tasks, f, indent=2)

def list_tasks(tasks):
    if not tasks:
        print("No tasks.")
        return
    for i, task in enumerate(tasks, 1):
        status = '✓' if task.get('done') else '○'
        print(f"{status} {i}. {task['text']}")

if __name__ == '__main__':
    tasks = load()
    
    if '--add' in sys.argv:
        idx = sys.argv.index('--add')
        text = ' '.join(sys.argv[idx + 1:])
        tasks.append({'text': text, 'done': False})
        save(tasks)
        print(f"Added: {text}")
    elif '--done' in sys.argv:
        idx = sys.argv.index('--done')
        n = int(sys.argv[idx + 1]) - 1
        if 0 <= n < len(tasks):
            tasks[n]['done'] = True
            save(tasks)
            print(f"Done: {tasks[n]['text']}")
    elif '--list' in sys.argv:
        list_tasks(tasks)
    elif '--clear' in sys.argv:
        tasks = [t for t in tasks if not t.get('done')]
        save(tasks)
        print("Cleared done tasks.")
    else:
        list_tasks(tasks)
