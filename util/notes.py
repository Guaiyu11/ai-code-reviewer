#!/usr/bin/env python3
"""
Notes - Simple CLI notes manager.
Usage: python notes.py [--add TEXT] [--list] [--search TERM] [--delete N]
Notes stored in ~/.notes.json
"""

import sys
import os
import json
from datetime import datetime

NOTES_FILE = os.path.expanduser('~/.notes.json')

def load_notes():
    if os.path.exists(NOTES_FILE):
        with open(NOTES_FILE, 'r') as f:
            return json.load(f)
    return []

def save_notes(notes):
    with open(NOTES_FILE, 'w') as f:
        json.dump(notes, f, indent=2)

def add_note(text):
    notes = load_notes()
    notes.append({
        'id': len(notes) + 1,
        'text': text,
        'date': datetime.now().strftime('%Y-%m-%d %H:%M')
    })
    save_notes(notes)
    print(f"Added note #{len(notes)}")

def list_notes():
    notes = load_notes()
    if not notes:
        print("No notes.")
        return
    for note in notes:
        print(f"[{note['id']}] {note['date']} - {note['text']}")

def search_notes(term):
    notes = load_notes()
    results = [n for n in notes if term.lower() in n['text'].lower()]
    if not results:
        print(f"No notes containing '{term}'")
        return
    for note in results:
        print(f"[{note['id']}] {note['date']} - {note['text']}")

def delete_note(n):
    notes = load_notes()
    notes = [note for note in notes if note['id'] != n]
    save_notes(notes)
    print(f"Deleted note #{n}")

if __name__ == '__main__':
    if '--add' in sys.argv:
        idx = sys.argv.index('--add')
        text = ' '.join(sys.argv[idx + 1:])
        add_note(text)
    elif '--list' in sys.argv:
        list_notes()
    elif '--search' in sys.argv:
        idx = sys.argv.index('--search')
        term = sys.argv[idx + 1]
        search_notes(term)
    elif '--delete' in sys.argv:
        idx = sys.argv.index('--delete')
        n = int(sys.argv[idx + 1])
        delete_note(n)
    else:
        print("Usage: python notes.py [--add TEXT] [--list] [--search TERM] [--delete N]")
