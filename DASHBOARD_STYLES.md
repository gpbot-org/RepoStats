# 🎨 GitHub Stats SVG API - Dashboard Styles

## 🌟 **Complete Style Collection**

Your GitHub Stats SVG API now supports **4 distinct dashboard styles** to match any design preference!

## 🌙 **1. Modern Dark Dashboard** ⭐ NEW!

**Endpoint:** `/api/modern/{owner}/{repo}.svg`

**Style:** Sleek, modern dark interface matching your reference design
- **Background:** Deep dark (`#1a1a1a`) with rounded cards
- **Charts:** Colorful line charts (green & purple) with glow effects
- **Stats Circle:** Modern donut chart with gradient center
- **Typography:** Inter font family for modern look
- **Size:** 500×300px (compact and sleek)

**Perfect for:** Modern dark-themed websites, professional portfolios, sleek README files

```markdown
![Modern Dashboard](http://localhost:8000/api/modern/gpbot-org/gpColor.svg)
```

## 🎨 **2. RepoBeats-Style Dashboard**

**Endpoint:** `/api/repobeats/{owner}/{repo}.svg`

**Style:** Exact replica of RepoBeats.axiom.co
- **Header:** Pink contribution dots with activity summary
- **Metrics:** Three cards (Issue Ratio, PRs, Commits) with trends
- **Charts:** Colorful bar charts (Issues, PRs, Pushes & Commits)
- **Contributors:** GitHub-style heatmaps for top 5 contributors
- **Size:** 900×400px (comprehensive dashboard)

**Perfect for:** Matching RepoBeats aesthetic, comprehensive statistics display

```markdown
![RepoBeats Dashboard](http://localhost:8000/api/repobeats/gpbot-org/gpColor.svg)
```

## 📊 **3. Classic Repository Stats**

**Endpoint:** `/api/embed/{owner}/{repo}.svg`

**Style:** Clean, GitHub-inspired statistics overview
- **Layout:** Traditional card-based design
- **Content:** Stars, forks, issues, commits, languages, contributors
- **Colors:** GitHub's official color scheme
- **Size:** 800×400px (standard size)

**Perfect for:** Traditional README files, documentation, clean presentations

```markdown
![Repository Stats](http://localhost:8000/api/embed/gpbot-org/gpColor.svg)
```

## 📈 **4. Activity Chart**

**Endpoint:** `/api/activity/{owner}/{repo}.svg`

**Style:** Focused commit activity visualization
- **Chart Type:** Line chart showing weekly commit activity
- **Data:** Past year of commit history
- **Design:** Minimalist with focus on data
- **Size:** 800×300px (wide chart format)

**Perfect for:** Highlighting development activity, progress tracking

```markdown
![Activity Chart](http://localhost:8000/api/activity/gpbot-org/gpColor.svg)
```

## 🎯 **Style Comparison**

| Style | Size | Focus | Best For |
|-------|------|-------|----------|
| **Modern Dark** | 500×300 | Sleek design | Modern websites |
| **RepoBeats** | 900×400 | Comprehensive | Full statistics |
| **Classic Stats** | 800×400 | Overview | Traditional use |
| **Activity Chart** | 800×300 | Commit activity | Progress tracking |

## 🎨 **Theme Support**

All endpoints support theme customization:
- **Light Theme:** `?theme=default` (default)
- **Dark Theme:** `?theme=dark`

```markdown
<!-- Light theme -->
![Stats Light](http://localhost:8000/api/modern/gpbot-org/gpColor.svg?theme=default)

<!-- Dark theme -->
![Stats Dark](http://localhost:8000/api/modern/gpbot-org/gpColor.svg?theme=dark)
```

## 🚀 **Your Repository Examples**

### For `gpbot-org/gpColor`:

```markdown
<!-- Modern sleek dashboard -->
![gpColor Modern](http://localhost:8000/api/modern/gpbot-org/gpColor.svg)

<!-- Comprehensive RepoBeats style -->
![gpColor RepoBeats](http://localhost:8000/api/repobeats/gpbot-org/gpColor.svg)

<!-- Classic repository stats -->
![gpColor Stats](http://localhost:8000/api/embed/gpbot-org/gpColor.svg)

<!-- Activity tracking -->
![gpColor Activity](http://localhost:8000/api/activity/gpbot-org/gpColor.svg)
```

## 🎯 **Recommendation**

**For your sleek design preference:** Use the **Modern Dark Dashboard** (`/api/modern/`) - it perfectly matches the style you showed me with:
- Dark background with rounded cards
- Colorful line charts
- Modern circular stats display
- Clean, professional typography

## 🔧 **Usage Tips**

1. **Choose the right style** for your use case
2. **Test both themes** (light/dark) to see which fits better
3. **Consider your audience** - modern vs traditional preferences
4. **Mix and match** - use different styles for different sections

Your API now provides the **most comprehensive collection** of GitHub statistics visualizations available! 🎨✨
