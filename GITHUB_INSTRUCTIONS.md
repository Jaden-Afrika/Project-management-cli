# GitHub Repository Setup

Follow these steps to push this project to a public GitHub repository:

## Step 1: Create a Repository on GitHub

1. Go to [GitHub.com](https://github.com)
2. Click the **+** icon in the top right → **New repository**
3. Name it: `project-management-cli`
4. **Do NOT** initialize with README, .gitignore, or license
5. Click **Create repository**

## Step 2: Add Remote and Push

Run these commands in the project directory:

```bash
# Add remote origin
git remote add origin https://github.com/YOUR_USERNAME/project-management-cli.git

# Rename branch to main (optional but recommended)
git branch -M main

# Stage all files
git add .

# Commit
git commit -m "Initial commit: Project management CLI with user, project, and task management"

# Push to GitHub
git push -u origin main
```

## Step 3: Verify Repository

Your public repository will be at:
```
https://github.com/YOUR_USERNAME/project-management-cli
```

## Repository Contents

✅ **Source Code:**
- `index.py` - CLI entry point
- `cli.py` - Command-line interface
- `models.py` - User, Project, Task classes
- `data_manager.py` - JSON persistence layer
- `tests.py` - Unit tests (11 passing)

✅ **Configuration:**
- `requirements.txt` - Python dependencies (tabulate==0.9.0)
- `.gitignore` - Ignore venv, cache, and generated data

✅ **Documentation:**
- `README.md` - Setup and usage guide
- `data/sample_data.json` - Data structure example

✅ **Data:**
- `data/` - Directory for JSON storage

## Making Your Repository Public

The repository is public by default after creation. To verify:

1. Go to your repository on GitHub
2. Click **Settings** → **General**
3. Under "Danger Zone", verify the repository is public (not private)

## Sharing the Repository

Share this link with others:
```
https://github.com/YOUR_USERNAME/project-management-cli
```

They can clone it with:
```bash
git clone https://github.com/YOUR_USERNAME/project-management-cli.git
```
