#!/usr/bin/env python3
"""
Cheatsheet Generator - Generate a cheatsheet for any CLI command.
Usage: python cheatsheet-gen.py <command>
"""

import sys
import subprocess

CHEATSHEETS = {
    'git': """
Git Cheatsheet
==============
git init              Create new repo
git clone <url>       Clone repo
git add <file>        Stage changes
git commit -m "msg"    Commit
git push              Push to remote
git pull              Pull from remote
git status            Show status
git log --oneline     Show commits
git branch            List branches
git checkout <b>      Switch branch
git merge <b>         Merge branch
git stash             Stash changes
git reset --hard      Reset to last commit
""",
    'docker': """
Docker Cheatsheet
=================
docker build .        Build image
docker run <img>      Run container
docker ps              List running
docker ps -a          List all
docker stop <id>       Stop container
docker rm <id>         Remove container
docker images          List images
docker rmi <img>       Remove image
docker exec -it <id> bash  Shell into container
docker logs <id>       View logs
docker-compose up      Run compose file
""",
    'kubectl': """
Kubernetes Cheatsheet
=====================
kubectl get pods       List pods
kubectl get svc        List services
kubectl get deploy     List deployments
kubectl apply -f <f>   Apply config
kubectl delete -f <f>  Delete resources
kubectl describe pod <name>  Pod details
kubectl logs <pod>     Pod logs
kubectl exec -it <pod> -- bash  Shell
kubectl scale deploy <name> --replicas N  Scale
""",
    'vim': """
Vim Cheatsheet
==============
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
:vsplit <file>        Split vertical
""",
}

def generate_cheatsheet(cmd):
    """Generate cheatsheet for command."""
    cmd_lower = cmd.lower()
    if cmd_lower in CHEATSHEETS:
        return CHEATSHEETS[cmd_lower]
    
    # Try man page
    try:
        result = subprocess.run(['man', cmd], capture_output=True, text=True, timeout=5)
        if result.returncode == 0:
            # Extract first ~100 lines
            lines = result.stdout.split('\n')[:100]
            return f"{cmd} Manual\n" + '=' * 40 + '\n' + '\n'.join(lines)
    except:
        pass
    
    return f"No cheatsheet available for: {cmd}"

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python cheatsheet-gen.py <command>")
        print("\nAvailable:", ', '.join(CHEATSHEETS.keys()))
        sys.exit(1)
    
    cmd = sys.argv[1]
    print(generate_cheatsheet(cmd))
