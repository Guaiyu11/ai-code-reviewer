#!/usr/bin/env python3
"""
Cheat - Show quick reference for commands.
Usage: python cheat.py <command>
"""

import sys

CHEATS = {
    'git': """
git init              Create repo
git clone <url>       Clone repo
git add .            Stage all
git commit -m "msg"  Commit
git push              Push
git pull             Pull
git status            Status
git log --oneline     History
git branch            Branches
git checkout <b>     Switch branch
git merge <b>         Merge branch
git stash             Stash changes
""",
    'docker': """
docker build .         Build image
docker run <img>       Run container
docker ps              Running containers
docker ps -a           All containers
docker stop <id>       Stop container
docker rm <id>         Remove container
docker images          List images
docker exec -it <id> bash  Shell into container
docker logs <id>       View logs
""",
    'ssh': """
ssh user@host           Connect
ssh -i key host        With key
ssh -p 2222 user@host  Custom port
ssh -L 8080:localhost:80 user@host  Tunnel
""",
    'vim': """
i                     Insert mode
Esc                   Normal mode
:w                    Save
:q                    Quit
:wq                   Save and quit
dd                    Delete line
yy                    Copy line
p                     Paste
u                     Undo
Ctrl+r                Redo
/search               Search
:%s/old/new/g         Replace all
""",
    'curl': """
curl <url>             GET request
curl -X POST -d "data" <url>  POST
curl -H "Header: value" <url>  Headers
curl -o file <url>     Download to file
curl -I <url>          HEAD request
""",
    'tar': """
tar -cvf file.tar dir/   Create
tar -xvf file.tar        Extract
tar -czvf file.tar.gz dir/  Create gzip
tar -xzvf file.tar.gz    Extract gzip
tar -tvf file.tar         List contents
""",
}

def show_cheat(cmd):
    """Show cheat sheet."""
    cmd_lower = cmd.lower()
    if cmd_lower in CHEATS:
        print(CHEATS[cmd_lower])
    else:
        print(f"No cheat sheet for: {cmd}")
        print(f"Available: {', '.join(CHEATS.keys())}")

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python cheat.py <command>")
        print(f"\nAvailable: {', '.join(CHEATS.keys())}")
        sys.exit(1)
    
    show_cheat(sys.argv[1])
