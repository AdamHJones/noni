# Setting Up Git Repository

Complete guide to set up your Git repository on GitHub.

## Prerequisites

- GitHub account at https://github.com/AdamHJones
- Git installed on your Mac
- Terminal access

---

## Step 1: Check Git Installation

```bash
# Check if git is installed
git --version

# If not installed:
xcode-select --install
```

---

## Step 2: Configure Git (One-Time Setup)

```bash
# Set your name
git config --global user.name "Adam Jones"

# Set your email (use your GitHub email)
git config --global user.email "your-email@example.com"

# Verify settings
git config --list
```

---

## Step 3: Initialize Repository

```bash
# Navigate to your project
cd /users/adamjones/noni

# Initialize git
git init

# Check status
git status
```

---

## Step 4: Create .gitignore (Already Done!)

Your `.gitignore` file is already set up to exclude:
- API keys (.env files)
- Dependencies (node_modules, venv)
- Build artifacts
- Sensitive credentials

**IMPORTANT:** Never commit `.env` files!

---

## Step 5: Create Repository on GitHub

1. **Go to** https://github.com/AdamHJones
2. **Click** "New repository" (green button)
3. **Repository name:** `care-companion` (or `noni`)
4. **Description:** "AI-native care companion app for elderly with Alzheimer's/dementia"
5. **Visibility:** Private (recommended for now)
6. **DO NOT** initialize with README (we have one)
7. **Click** "Create repository"

---

## Step 6: Connect Local to GitHub

```bash
# Add all files
git add .

# Create first commit
git commit -m "Initial commit: Complete Care Companion MVP with vision and geolocation"

# Add GitHub as remote (replace USERNAME with AdamHJones)
git remote add origin https://github.com/AdamHJones/care-companion.git

# Rename branch to main (if needed)
git branch -M main

# Push to GitHub
git push -u origin main
```

---

## Step 7: Verify on GitHub

Visit: https://github.com/AdamHJones/care-companion

You should see all your files!

---

## Daily Git Workflow

### Making Changes

```bash
# Check what changed
git status

# See specific changes
git diff

# Add specific files
git add path/to/file

# Or add all changes
git add .

# Commit with message
git commit -m "Add camera feature for medication scanning"

# Push to GitHub
git push
```

### Viewing History

```bash
# See commit history
git log --oneline

# See changes in last commit
git show
```

### Branching (Optional but Recommended)

```bash
# Create feature branch
git checkout -b feature/calendar-integration

# Work on feature...
git add .
git commit -m "Add Google Calendar integration"

# Push feature branch
git push -u origin feature/calendar-integration

# Switch back to main
git checkout main

# Merge feature (when ready)
git merge feature/calendar-integration
```

---

## Common Commands Reference

```bash
# Status
git status                  # See what changed
git log --oneline          # See history
git diff                   # See changes

# Adding & Committing
git add .                  # Add all files
git add filename           # Add specific file
git commit -m "message"    # Commit with message

# Pushing & Pulling
git push                   # Push to GitHub
git pull                   # Pull from GitHub

# Branching
git branch                 # List branches
git checkout -b name       # Create new branch
git checkout main          # Switch to main
git merge branch-name      # Merge branch

# Undoing
git restore filename       # Discard changes
git reset HEAD~1           # Undo last commit (keep changes)
git reset --hard HEAD~1    # Undo last commit (delete changes)
```

---

## Best Practices

### Commit Messages

**Good:**
- "Add vision service for medication scanning"
- "Fix geolocation permission issue on iOS"
- "Update documentation for camera features"
- "Refactor AI service for better error handling"

**Bad:**
- "update"
- "fix stuff"
- "asdf"
- "changes"

### When to Commit

**Commit when:**
- ✅ You finish a feature
- ✅ You fix a bug
- ✅ You complete a refactor
- ✅ At the end of each work session

**Don't commit:**
- ❌ Broken code (unless on feature branch)
- ❌ API keys or secrets
- ❌ Personal test data
- ❌ Half-finished work (use branches)

### Commit Frequency

- Small commits (1 feature/fix at a time)
- Commit often (several times per day)
- Push regularly (at least daily)

---

## Protecting Sensitive Data

### What NEVER to Commit

- ❌ `.env` files
- ❌ API keys
- ❌ Passwords
- ❌ Access tokens
- ❌ `credentials.json`
- ❌ Database connection strings
- ❌ Personal information

### If You Accidentally Commit Secrets

```bash
# Remove file from git (keeps local file)
git rm --cached .env

# Commit the removal
git commit -m "Remove .env from git"

# Push
git push

# IMPORTANT: Rotate the exposed API keys immediately!
```

---

## Collaborating (If Working with Others)

### Pull Before You Work

```bash
git pull
# Always pull latest changes before starting work
```

### Push Regularly

```bash
git push
# Push your changes so others can see them
```

### Resolving Conflicts

If you get conflicts:

```bash
# Pull latest
git pull

# Git will mark conflicts in files
# Open files and resolve manually
# Look for <<<<<<< and >>>>>>>

# After resolving
git add .
git commit -m "Resolve merge conflicts"
git push
```

---

## GitHub Features to Use

### Issues

Track bugs and features:
```
https://github.com/AdamHJones/care-companion/issues
```

**Example Issue:**
```
Title: Add medication reminder notifications
Body: We need push notifications when medications are due.
- [ ] Set up notification service
- [ ] Create reminder logic
- [ ] Test on iPhone
```

### Projects

Organize work:
```
https://github.com/AdamHJones/care-companion/projects
```

Create boards:
- To Do
- In Progress
- Done

### Pull Requests

For code review (if working with others):
1. Create feature branch
2. Push branch
3. Open Pull Request on GitHub
4. Review & merge

---

## Backup Strategy

### Git is Your Backup

- Every commit is saved
- History is preserved
- Can revert to any point

### Additional Backups

```bash
# Clone to another location
git clone https://github.com/AdamHJones/care-companion.git ~/backups/noni-backup

# Or manually backup
cp -r /users/adamjones/noni ~/backups/noni-$(date +%Y%m%d)
```

---

## Useful Git Aliases

Add to `~/.gitconfig`:

```ini
[alias]
    st = status
    co = checkout
    br = branch
    ci = commit
    unstage = reset HEAD --
    last = log -1 HEAD
    visual = log --oneline --graph --all
```

Then use:
```bash
git st              # Instead of git status
git co main         # Instead of git checkout main
git visual          # Pretty history tree
```

---

## Troubleshooting

### "Permission denied"

```bash
# Generate SSH key
ssh-keygen -t ed25519 -C "your-email@example.com"

# Add to GitHub
# Copy: ~/.ssh/id_ed25519.pub
# Paste in: GitHub Settings → SSH Keys
```

### "Repository not found"

```bash
# Check remote URL
git remote -v

# Update if wrong
git remote set-url origin https://github.com/AdamHJones/care-companion.git
```

### "Merge conflicts"

```bash
# See conflicted files
git status

# Edit files, choose correct version
# Then:
git add .
git commit -m "Resolve conflicts"
```

### "Accidentally committed to wrong branch"

```bash
# Move commit to new branch
git branch feature-branch
git reset --hard HEAD~1
git checkout feature-branch
```

---

## Quick Start Checklist

- [ ] Git installed
- [ ] Git configured (name, email)
- [ ] Repository created on GitHub
- [ ] Local repo initialized
- [ ] .gitignore in place
- [ ] First commit made
- [ ] Pushed to GitHub
- [ ] Verified files on GitHub

---

## Your First Commands

```bash
cd /users/adamjones/noni
git init
git add .
git commit -m "Initial commit: Care Companion MVP"
git remote add origin https://github.com/AdamHJones/care-companion.git
git branch -M main
git push -u origin main
```

---

## Next Steps After Setup

1. **Create README badges** (optional):
   - Build status
   - License
   - Version

2. **Add LICENSE file**:
   - MIT License (most permissive)
   - Or keep private

3. **Set up GitHub Actions** (optional):
   - Auto-test on push
   - Auto-deploy to production

4. **Enable Discussions** (optional):
   - For questions/ideas
   - Community feedback

---

You're ready to use Git! 🚀

