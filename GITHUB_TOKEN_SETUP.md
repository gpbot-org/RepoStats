# 🔑 GitHub Token Setup Guide

## Why You Need a GitHub Token

**Without Token:**
- ❌ 60 requests per hour per IP address
- ❌ Rate limits hit quickly during testing
- ❌ Limited functionality

**With Token:**
- ✅ 5,000 requests per hour
- ✅ Smooth operation and testing
- ✅ Full API functionality

## 📝 How to Get a GitHub Personal Access Token

### Step 1: Go to GitHub Settings
1. Visit: https://github.com/settings/tokens
2. Or: GitHub → Settings → Developer settings → Personal access tokens → Tokens (classic)

### Step 2: Generate New Token
1. Click **"Generate new token"** → **"Generate new token (classic)"**
2. Give it a descriptive name: `GitHub Stats SVG API`
3. Set expiration (recommend 90 days or No expiration for development)

### Step 3: Select Scopes
For this API, you only need **public repository access**:
- ✅ **`public_repo`** - Access public repositories
- ✅ **`read:user`** - Read user profile (optional, for contributor data)

**Note:** You don't need private repo access unless you want to generate stats for private repositories.

### Step 4: Generate and Copy Token
1. Click **"Generate token"**
2. **⚠️ IMPORTANT:** Copy the token immediately - you won't see it again!
3. It will look like: `ghp_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx`

## 🔧 Add Token to Your API

### Method 1: Environment File
1. Edit the `.env` file in your project:
```bash
# GitHub Personal Access Token
GITHUB_TOKEN=ghp_your_actual_token_here

# Redis configuration (optional)
REDIS_URL=redis://localhost:6379/0
```

### Method 2: Environment Variable
```bash
export GITHUB_TOKEN=ghp_your_actual_token_here
```

## 🚀 Restart the API

After adding the token:
```bash
# Stop the current server (Ctrl+C)
# Then restart:
./start.sh
# Or manually:
source venv/bin/activate && python main.py
```

## ✅ Test Your Repository

Once the token is added, test your repository:

```bash
# Test basic stats
curl "http://localhost:8000/api/embed/gpbot-org/gpColor.svg"

# Test RepoBeats-style dashboard
curl "http://localhost:8000/api/repobeats/gpbot-org/gpColor.svg"

# Test dark theme
curl "http://localhost:8000/api/repobeats/gpbot-org/gpColor.svg?theme=dark"
```

## 🎨 Expected Results for gpbot-org/gpColor

With a valid token, you should get:

### Repository Stats (`/api/embed/gpbot-org/gpColor.svg`)
- Repository name and description
- Stars, forks, and watchers count
- Programming language distribution
- Top contributors
- Issue statistics

### RepoBeats-Style Dashboard (`/api/repobeats/gpbot-org/gpColor.svg`)
- Comprehensive 900x500px dashboard
- Colorful contribution activity header
- Issues, PRs, and commits charts
- Contributors heatmap section
- Professional GitHub-style design

### Usage in README
```markdown
![gpColor Stats](http://your-domain.com/api/embed/gpbot-org/gpColor.svg)
![gpColor Dashboard](http://your-domain.com/api/repobeats/gpbot-org/gpColor.svg)
```

## 🔒 Security Notes

- ✅ Keep your token secure and private
- ✅ Don't commit tokens to version control
- ✅ Use environment variables or .env files
- ✅ Regenerate tokens periodically
- ✅ Only grant minimum required permissions

## 🆘 Troubleshooting

### Still Getting Rate Limit Errors?
1. Verify token is correctly set in `.env`
2. Restart the API server
3. Check token hasn't expired
4. Ensure token has `public_repo` scope

### Token Not Working?
1. Verify the token format (starts with `ghp_`)
2. Check token permissions/scopes
3. Try generating a new token
4. Ensure no extra spaces in `.env` file

### Repository Not Found?
1. Check repository name spelling: `gpbot-org/gpColor`
2. Ensure repository is public
3. Verify organization/username is correct

Once you add the token, the API will work smoothly with your `gpbot-org/gpColor` repository! 🎉
