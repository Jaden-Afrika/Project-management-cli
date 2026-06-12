# Push to GitHub - Step by Step

## Prerequisites
- GitHub account (create at https://github.com/signup if needed)
- Git installed locally
- This project directory with initialized repo

## Step 1: Create Repository on GitHub

1. Go to https://github.com/new
2. Fill in:
   - **Repository name:** `project-management-cli`
   - **Description:** CLI tool for managing users, projects, and tasks
   - **Public/Private:** Choose "Public"
3. **Do NOT** initialize with README, .gitignore, or license (we already have these)
4. Click **Create repository**

You'll see a page with setup instructions. We'll use those.

## Step 2: Push Existing Repository

Copy and run these commands in your terminal:

```bash
cd /home/student/Python

# Set up the remote (replace YOUR_USERNAME with your actual GitHub username)
git remote add origin https://github.com/YOUR_USERNAME/project-management-cli.git

# Rename branch to 'main' (optional but recommended for GitHub)
git branch -M main

# Push to GitHub
git push -u origin main
```

Example with actual username:
```bash
git remote add origin https://github.com/johndoe/project-management-cli.git
git branch -M main
git push -u origin main
```

## Step 3: Verify Repository

1. Go to https://github.com/YOUR_USERNAME/project-management-cli
2. You should see all files:
   - Source code (index.py, cli.py, models.py, data_manager.py)
   - Tests (tests.py)
   - Documentation (README.md)
   - Configuration (.gitignore, requirements.txt)

## Step 4: Share Repository

Your public repository URL:
```
https://github.com/YOUR_USERNAME/project-management-cli
```

Share this link with instructors/reviewers.

## Troubleshooting

### Error: "remote origin already exists"
```bash
git remote remove origin
git remote add origin https://github.com/YOUR_USERNAME/project-management-cli.git
```

### Error: "Authentication failed"
- Make sure you're using HTTPS URLs
- Use a GitHub Personal Access Token (PAT) for authentication
- Or set up SSH keys

### Repository appears empty
- Verify you pushed to the correct branch: `git push -u origin main`
- Refresh the GitHub page

## Verify Locally

Before pushing, verify everything is committed:
```bash
cd /home/student/Python
git status
git log --oneline
```

Both should show:
- No uncommitted changes
- 2 commits ready

You're all set! 🎉
