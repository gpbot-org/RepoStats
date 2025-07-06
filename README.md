# GitHub Stats SVG API

A Python API that generates dynamic SVG charts for GitHub repository statistics, similar to RepoBeats. Create beautiful, real-time visualizations of your repository's activity, contributors, and statistics.

## Features

- 🌙 **Modern Dark Dashboard**: Sleek, modern interface with colorful line charts and circular stats
- 🎨 **RepoBeats-Style Dashboard**: Comprehensive colorful dashboard with charts and heatmaps
- 📊 **Repository Statistics**: Stars, forks, issues, commits, and more
- 👥 **Contributor Analytics**: Individual contributor statistics and activity heatmaps
- 📈 **Activity Charts**: Commit activity visualization over time
- 🎨 **Multiple Themes**: Light and dark themes with customizable colors
- 🚀 **Fast & Cached**: Redis caching for optimal performance
- 🔄 **Real-time Data**: Syncs with GitHub API for up-to-date information
- 📱 **SVG Output**: Scalable vector graphics perfect for README files

## Quick Start

### 1. Installation

```bash
# Clone the repository
git clone <your-repo-url>
cd github-stats-svg-api

# Install dependencies
pip install -r requirements.txt

# Copy environment file
cp .env.example .env
```

### 2. Configuration

Edit `.env` file:
```bash
# Optional: GitHub Personal Access Token for higher rate limits
GITHUB_TOKEN=your_github_token_here

# Optional: Redis for caching (falls back to memory cache)
REDIS_URL=redis://localhost:6379/0
```

### 3. Run the API

```bash
python main.py
```

The API will be available at `http://localhost:8000`

## Usage

### 🌙 Modern Dark Dashboard

Generate a sleek, modern dashboard with dark theme and colorful charts:

```
GET /api/modern/{owner}/{repo}.svg
```

**Example:**
```html
<img src="http://localhost:8000/api/modern/gpbot-org/gpColor.svg" />
```

### 🎨 RepoBeats-Style Dashboard

Generate a comprehensive, colorful dashboard similar to RepoBeats:

```
GET /api/repobeats/{owner}/{repo}.svg
```

**Example:**
```html
<img src="http://localhost:8000/api/repobeats/microsoft/vscode.svg" />
```

### 📊 Repository Statistics

Generate an SVG with comprehensive repository statistics:

```
GET /api/embed/{owner}/{repo}.svg
```

**Example:**
```html
<img src="http://localhost:8000/api/embed/microsoft/vscode.svg" />
```

### 📈 Activity Chart

Generate a commit activity chart over time:

```
GET /api/activity/{owner}/{repo}.svg
```

**Example:**
```html
<img src="http://localhost:8000/api/activity/microsoft/vscode.svg" />
```

**Parameters (all endpoints):**
- `theme`: `default` or `dark` (optional)

### Contributor Statistics

Generate an SVG for individual contributor statistics:

```
GET /api/contributor/{owner}/{repo}/{username}.svg
```

**Example:**
```html
<img src="http://localhost:8000/api/contributor/microsoft/vscode/bpasero.svg" />
```

## API Endpoints

| Endpoint | Description | Parameters |
|----------|-------------|------------|
| `GET /` | API information | - |
| `GET /api/modern/{owner}/{repo}.svg` | 🌙 Modern dark dashboard with sleek design | `theme` (optional) |
| `GET /api/repobeats/{owner}/{repo}.svg` | 🎨 RepoBeats-style comprehensive dashboard | `theme` (optional) |
| `GET /api/embed/{owner}/{repo}.svg` | 📊 Repository stats SVG | `theme` (optional) |
| `GET /api/contributor/{owner}/{repo}/{username}.svg` | 👥 Contributor stats SVG | `theme` (optional) |
| `GET /api/activity/{owner}/{repo}.svg` | 📈 Commit activity chart SVG | `theme` (optional) |

## 🎨 Dashboard Styles

### 🌙 Modern Dark Dashboard (`/api/modern/`)
- **Style**: Sleek, modern interface with dark background
- **Features**: Colorful line charts, circular stats, rounded cards
- **Size**: 500×300px (compact)
- **Best for**: Modern websites, professional portfolios

### 🎨 RepoBeats-Style Dashboard (`/api/repobeats/`)
- **Style**: Comprehensive dashboard matching RepoBeats.axiom.co
- **Features**: Contribution dots, metric cards, bar charts, contributor heatmaps
- **Size**: 900×400px (comprehensive)
- **Best for**: Full statistics display, RepoBeats alternative

### 📊 Classic Repository Stats (`/api/embed/`)
- **Style**: Traditional GitHub-inspired overview
- **Features**: Stars, forks, issues, languages, contributors
- **Size**: 800×400px (standard)
- **Best for**: Traditional README files, clean presentations

### 📈 Activity Chart (`/api/activity/`)
- **Style**: Focused commit activity visualization
- **Features**: Line chart showing weekly commit history
- **Size**: 800×300px (wide chart)
- **Best for**: Development progress tracking

## Themes

### Default Theme
Light theme with GitHub-style colors.

### Dark Theme
Dark theme optimized for dark mode README files.

Add `?theme=dark` to any endpoint to use the dark theme.

## Examples

### 🌙 Modern Dark Dashboard
```markdown
![Modern Dashboard](http://localhost:8000/api/modern/gpbot-org/gpColor.svg)
```

### 🎨 RepoBeats-Style Dashboard
```markdown
![RepoBeats Dashboard](http://localhost:8000/api/repobeats/microsoft/vscode.svg)
```

### 📊 Repository Statistics
```markdown
![Repository Stats](http://localhost:8000/api/embed/microsoft/vscode.svg)
```

### 📈 Commit Activity Chart
```markdown
![Activity Chart](http://localhost:8000/api/activity/microsoft/vscode.svg)
```

### 👥 Individual Contributor
```markdown
![Contributor Stats](http://localhost:8000/api/contributor/microsoft/vscode/bpasero.svg)
```

### 🎨 Theme Variations
```markdown
<!-- Light theme (default) -->
![Light Theme](http://localhost:8000/api/modern/gpbot-org/gpColor.svg?theme=default)

<!-- Dark theme -->
![Dark Theme](http://localhost:8000/api/modern/gpbot-org/gpColor.svg?theme=dark)
```

### 🚀 Complete Example for Your Repository
```markdown
<!-- Choose your preferred style -->

<!-- Modern sleek dashboard -->
![gpColor Modern](http://localhost:8000/api/modern/gpbot-org/gpColor.svg)

<!-- Comprehensive RepoBeats style -->
![gpColor RepoBeats](http://localhost:8000/api/repobeats/gpbot-org/gpColor.svg)

<!-- Classic repository overview -->
![gpColor Stats](http://localhost:8000/api/embed/gpbot-org/gpColor.svg)

<!-- Activity tracking -->
![gpColor Activity](http://localhost:8000/api/activity/gpbot-org/gpColor.svg)
```

## Development

### Project Structure
```
├── main.py                 # FastAPI application
├── requirements.txt        # Python dependencies
├── src/
│   ├── __init__.py
│   ├── github_api.py      # GitHub API integration
│   ├── svg_generator.py   # SVG generation engine
│   └── cache_manager.py   # Caching system
└── README.md
```

### Running Tests
```bash
# Install test dependencies
pip install pytest pytest-asyncio

# Run tests
pytest
```

## Deployment

### Docker
```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 8000

CMD ["python", "main.py"]
```

### Environment Variables
- `GITHUB_TOKEN`: GitHub Personal Access Token (optional but recommended)
- `REDIS_URL`: Redis connection URL (optional, defaults to memory cache)
- `PORT`: Server port (default: 8000)

## Rate Limits

- **Without GitHub Token**: 60 requests per hour per IP
- **With GitHub Token**: 5,000 requests per hour
- **Caching**: 1-hour cache reduces API calls

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## License

MIT License - see LICENSE file for details.

## Acknowledgments

Inspired by [RepoBeats](https://repobeats.axiom.co/) and the GitHub community's need for beautiful repository statistics.
