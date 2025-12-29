# Git Pull Fix - Not a Git Repository

## Problem

You're getting `fatal: not a git repository` because you're not in the project directory.

## Solution

Navigate to the project directory first:

```bash
# Navigate to project directory
cd ~/d2RO_trail/Aviatrax

# Now pull changes
git pull --no-rebase origin main
```

## Complete Steps

```bash
# 1. Navigate to project
cd ~/d2RO_trail/Aviatrax

# 2. Check if it's a git repository
ls -la .git

# 3. Check current status
git status

# 4. Pull changes
git pull --no-rebase origin main

# 5. If there are conflicts, resolve them
# Then rebuild Docker containers
docker compose build --no-cache frontend
docker compose up -d frontend
```

## If Git Repository Doesn't Exist

If the directory is not a git repository, you have two options:

### Option 1: Initialize Git Repository

```bash
cd ~/d2RO_trail/Aviatrax
git init
git remote add origin <your-repository-url>
git pull origin main
```

### Option 2: Clone Fresh

```bash
cd ~/d2RO_trail
rm -rf Aviatrax  # Backup first if needed!
git clone <your-repository-url> Aviatrax
cd Aviatrax
```

## Quick Fix

```bash
# Just navigate to the correct directory
cd ~/d2RO_trail/Aviatrax && git pull --no-rebase origin main
```

