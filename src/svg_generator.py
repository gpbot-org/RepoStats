from typing import Dict, List
import math
from datetime import datetime

class SVGGenerator:
    def __init__(self):
        self.themes = {
            "default": {
                "background": "#ffffff",
                "text_primary": "#24292e",
                "text_secondary": "#586069",
                "accent": "#0366d6",
                "success": "#28a745",
                "warning": "#ffd33d",
                "danger": "#d73a49",
                "border": "#e1e4e8",
                # Additional colors for charts
                "blue": "#58a6ff",
                "purple": "#a855f7",
                "pink": "#fb7185",
                "orange": "#f97316",
                "green": "#22c55e",
                "yellow": "#eab308",
                "red": "#ef4444",
                "indigo": "#6366f1"
            },
            "dark": {
                "background": "#0d1117",
                "text_primary": "#f0f6fc",
                "text_secondary": "#8b949e",
                "accent": "#58a6ff",
                "success": "#3fb950",
                "warning": "#d29922",
                "danger": "#f85149",
                "border": "#30363d",
                # Additional colors for charts
                "blue": "#58a6ff",
                "purple": "#a855f7",
                "pink": "#fb7185",
                "orange": "#f97316",
                "green": "#22c55e",
                "yellow": "#eab308",
                "red": "#ef4444",
                "indigo": "#6366f1"
            }
        }
    
    def get_theme_colors(self, theme: str) -> Dict[str, str]:
        """Get color scheme for the specified theme"""
        return self.themes.get(theme, self.themes["default"])

    def _safe_truncate_text(self, text, max_length: int) -> str:
        """Safely truncate text with null handling"""
        if not text or text is None:
            return ""
        text_str = str(text)
        if len(text_str) > max_length:
            return text_str[:max_length] + "..."
        return text_str
    
    def generate_repo_stats_svg(self, data: Dict, theme: str = "default") -> str:
        """Generate SVG for repository statistics"""
        colors = self.get_theme_colors(theme)

        # Safe data extraction with defaults
        repo = data.get("repository", {})
        stats = data.get("statistics", {})
        languages = data.get("languages", {})
        contributors = data.get("contributors", [])
        
        # SVG dimensions
        width = 800
        height = 400
        
        svg_parts = [
            f'<svg width="{width}" height="{height}" xmlns="http://www.w3.org/2000/svg">',
            f'<rect width="{width}" height="{height}" fill="{colors["background"]}" rx="6"/>',
            
            # Title
            f'<text x="20" y="30" font-family="Arial, sans-serif" font-size="18" font-weight="bold" fill="{colors["text_primary"]}">{repo.get("name", "Repository")}</text>',
            f'<text x="20" y="50" font-family="Arial, sans-serif" font-size="12" fill="{colors["text_secondary"]}">{self._safe_truncate_text(repo.get("description"), 80)}</text>',
            
            # Stats boxes
            self._generate_stat_box(80, 80, "Stars", repo.get("stars", 0), colors["accent"], colors),
            self._generate_stat_box(200, 80, "Forks", repo.get("forks", 0), colors["success"], colors),
            self._generate_stat_box(320, 80, "Issues", stats.get("open_issues", 0), colors["warning"], colors),
            self._generate_stat_box(440, 80, "Commits", stats.get("total_commits", 0), colors["accent"], colors),
            
            # Language chart
            self._generate_language_chart(20, 160, 350, languages, colors),
            
            # Contributors section
            self._generate_contributors_section(400, 160, contributors, colors),
            
            # Footer
            f'<text x="20" y="{height-10}" font-family="Arial, sans-serif" font-size="10" fill="{colors["text_secondary"]}">Generated at {datetime.now().strftime("%Y-%m-%d %H:%M UTC")}</text>',
            
            '</svg>'
        ]
        
        return '\n'.join(svg_parts)
    
    def _generate_stat_box(self, x: int, y: int, label: str, value: int, color: str, colors: Dict) -> str:
        """Generate a statistics box"""
        return f'''
        <g>
            <rect x="{x}" y="{y}" width="100" height="60" fill="{colors["background"]}" stroke="{colors["border"]}" rx="4"/>
            <text x="{x+50}" y="{y+20}" font-family="Arial, sans-serif" font-size="12" text-anchor="middle" fill="{colors["text_secondary"]}">{label}</text>
            <text x="{x+50}" y="{y+40}" font-family="Arial, sans-serif" font-size="16" font-weight="bold" text-anchor="middle" fill="{color}">{self._format_number(value)}</text>
        </g>'''
    
    def _format_number(self, num: int) -> str:
        """Format large numbers with K, M suffixes"""
        if num >= 1000000:
            return f"{num/1000000:.1f}M"
        elif num >= 1000:
            return f"{num/1000:.1f}K"
        return str(num)
    
    def _generate_language_chart(self, x: int, y: int, width: int, languages: Dict, colors: Dict) -> str:
        """Generate a horizontal bar chart for programming languages"""
        if not languages:
            return f'<text x="{x}" y="{y+20}" font-family="Arial, sans-serif" font-size="12" fill="{colors["text_secondary"]}">No language data available</text>'
        
        # Language colors (simplified)
        lang_colors = {
            "Python": "#3776ab",
            "JavaScript": "#f1e05a",
            "TypeScript": "#2b7489",
            "Java": "#b07219",
            "C++": "#f34b7d",
            "html": "#e34c26",
            "C": "#555555",
            "Go": "#00add8",
            "Rust": "#dea584",
            "PHP": "#4f5d95",
            "Ruby": "#701516",
            "Swift": "#ffac45",
            "Kotlin": "#f18e33"
        }
        
        chart_parts = [f'<text x="{x}" y="{y}" font-family="Arial, sans-serif" font-size="14" font-weight="bold" fill="{colors["text_primary"]}">Languages</text>']
        
        # Sort languages by percentage
        sorted_languages = sorted(languages.items(), key=lambda x: x[1], reverse=True)[:5]
        
        bar_height = 20
        bar_spacing = 25
        
        for i, (lang, percentage) in enumerate(sorted_languages):
            bar_y = y + 25 + (i * bar_spacing)
            bar_width = (percentage / 100) * (width - 100)
            lang_color = lang_colors.get(lang, colors["accent"])
            
            chart_parts.extend([
                f'<rect x="{x}" y="{bar_y}" width="{bar_width}" height="{bar_height}" fill="{lang_color}" rx="2"/>',
                f'<text x="{x + bar_width + 10}" y="{bar_y + 15}" font-family="Arial, sans-serif" font-size="11" fill="{colors["text_primary"]}">{lang} ({percentage:.1f}%)</text>'
            ])
        
        return '\n'.join(chart_parts)
    
    def _generate_contributors_section(self, x: int, y: int, contributors: List, colors: Dict) -> str:
        """Generate contributors section"""
        if not contributors:
            return f'<text x="{x}" y="{y+20}" font-family="Arial, sans-serif" font-size="12" fill="{colors["text_secondary"]}">No contributors data</text>'
        
        section_parts = [f'<text x="{x}" y="{y}" font-family="Arial, sans-serif" font-size="14" font-weight="bold" fill="{colors["text_primary"]}">Top Contributors</text>']
        
        for i, contributor in enumerate(contributors[:5]):
            contrib_y = y + 25 + (i * 30)
            avatar_size = 20
            
            # Contributor avatar (placeholder circle)
            section_parts.extend([
                f'<circle cx="{x + avatar_size//2}" cy="{contrib_y + avatar_size//2}" r="{avatar_size//2}" fill="{colors["accent"]}" opacity="0.3"/>',
                f'<text x="{x + avatar_size + 10}" y="{contrib_y + 8}" font-family="Arial, sans-serif" font-size="11" fill="{colors["text_primary"]}">{contributor.get("login", "Unknown")}</text>',
                f'<text x="{x + avatar_size + 10}" y="{contrib_y + 20}" font-family="Arial, sans-serif" font-size="10" fill="{colors["text_secondary"]}">{contributor.get("contributions", 0)} contributions</text>'
            ])
        
        return '\n'.join(section_parts)
    
    def generate_contributor_stats_svg(self, data: Dict, theme: str = "default") -> str:
        """Generate SVG for individual contributor statistics"""
        colors = self.get_theme_colors(theme)
        username = data["username"]
        total_commits = data["total_commits"]
        activity = data["activity"]
        
        # SVG dimensions
        width = 600
        height = 300
        
        svg_parts = [
            f'<svg width="{width}" height="{height}" xmlns="http://www.w3.org/2000/svg">',
            f'<rect width="{width}" height="{height}" fill="{colors["background"]}" rx="6"/>',
            
            # Title
            f'<text x="20" y="30" font-family="Arial, sans-serif" font-size="18" font-weight="bold" fill="{colors["text_primary"]}">{username}</text>',
            f'<text x="20" y="50" font-family="Arial, sans-serif" font-size="12" fill="{colors["text_secondary"]}">Contributor Stats for {data["repository"]}</text>',
            
            # Total commits
            f'<text x="20" y="80" font-family="Arial, sans-serif" font-size="14" fill="{colors["text_primary"]}">Total Commits: <tspan font-weight="bold" fill="{colors["accent"]}">{total_commits}</tspan></text>',
            
            # Activity heatmap (simplified)
            self._generate_activity_heatmap(20, 100, 560, activity, colors),
            
            # Footer
            f'<text x="20" y="{height-10}" font-family="Arial, sans-serif" font-size="10" fill="{colors["text_secondary"]}">Generated at {datetime.now().strftime("%Y-%m-%d %H:%M UTC")}</text>',
            
            '</svg>'
        ]
        
        return '\n'.join(svg_parts)
    
    def _generate_activity_heatmap(self, x: int, y: int, width: int, activity: Dict, colors: Dict) -> str:
        """Generate a simplified activity heatmap"""
        if not activity:
            return f'<text x="{x}" y="{y+20}" font-family="Arial, sans-serif" font-size="12" fill="{colors["text_secondary"]}">No activity data available</text>'

        heatmap_parts = [f'<text x="{x}" y="{y}" font-family="Arial, sans-serif" font-size="14" font-weight="bold" fill="{colors["text_primary"]}">Activity Heatmap</text>']

        # Create a simple grid representation
        cell_size = 12
        cells_per_row = width // (cell_size + 2)
        max_commits = max(activity.values()) if activity else 1

        sorted_weeks = sorted(activity.items())[-52:]  # Last 52 weeks

        for i, (week, commits) in enumerate(sorted_weeks):
            row = i // cells_per_row
            col = i % cells_per_row

            cell_x = x + (col * (cell_size + 2))
            cell_y = y + 25 + (row * (cell_size + 2))

            # Calculate opacity based on commit count
            opacity = min(commits / max_commits, 1.0) if max_commits > 0 else 0

            heatmap_parts.append(
                f'<rect x="{cell_x}" y="{cell_y}" width="{cell_size}" height="{cell_size}" '
                f'fill="{colors["accent"]}" opacity="{opacity}" rx="2" title="{week}: {commits} commits"/>'
            )

        return '\n'.join(heatmap_parts)

    def generate_commit_activity_svg(self, data: Dict, theme: str = "default") -> str:
        """Generate SVG for commit activity over time"""
        colors = self.get_theme_colors(theme)
        commit_activity = data.get("commit_activity", [])

        if not commit_activity:
            return self._generate_empty_chart("No commit activity data", theme)

        width = 800
        height = 300

        # Chart area
        chart_x = 60
        chart_y = 60
        chart_width = width - 100
        chart_height = height - 120

        svg_parts = [
            f'<svg width="{width}" height="{height}" xmlns="http://www.w3.org/2000/svg">',
            f'<rect width="{width}" height="{height}" fill="{colors["background"]}" rx="6"/>',

            # Title
            f'<text x="20" y="30" font-family="Arial, sans-serif" font-size="18" font-weight="bold" fill="{colors["text_primary"]}">Commit Activity</text>',
            f'<text x="20" y="50" font-family="Arial, sans-serif" font-size="12" fill="{colors["text_secondary"]}">Weekly commits over the past year</text>',

            # Chart background
            f'<rect x="{chart_x}" y="{chart_y}" width="{chart_width}" height="{chart_height}" fill="none" stroke="{colors["border"]}"/>',
        ]

        # Generate line chart
        max_commits = max(week.get('total', 0) for week in commit_activity) if commit_activity else 1
        points = []

        for i, week in enumerate(commit_activity):
            x_pos = chart_x + (i / len(commit_activity)) * chart_width
            y_pos = chart_y + chart_height - (week.get('total', 0) / max_commits) * chart_height
            points.append(f"{x_pos},{y_pos}")

        if points:
            svg_parts.append(f'<polyline points="{" ".join(points)}" fill="none" stroke="{colors["accent"]}" stroke-width="2"/>')

        # Y-axis labels
        for i in range(5):
            y_val = (max_commits / 4) * i
            y_pos = chart_y + chart_height - (i / 4) * chart_height
            svg_parts.append(f'<text x="{chart_x - 10}" y="{y_pos + 5}" font-family="Arial, sans-serif" font-size="10" text-anchor="end" fill="{colors["text_secondary"]}">{int(y_val)}</text>')

        svg_parts.extend([
            f'<text x="20" y="{height-10}" font-family="Arial, sans-serif" font-size="10" fill="{colors["text_secondary"]}">Generated at {datetime.now().strftime("%Y-%m-%d %H:%M UTC")}</text>',
            '</svg>'
        ])

        return '\n'.join(svg_parts)

    def _generate_empty_chart(self, message: str, theme: str = "default") -> str:
        """Generate an empty chart with a message"""
        colors = self.get_theme_colors(theme)
        width = 400
        height = 200

        return f'''<svg width="{width}" height="{height}" xmlns="http://www.w3.org/2000/svg">
            <rect width="{width}" height="{height}" fill="{colors["background"]}" rx="6"/>
            <text x="{width//2}" y="{height//2}" font-family="Arial, sans-serif" font-size="14" text-anchor="middle" fill="{colors["text_secondary"]}">{message}</text>
        </svg>'''

    def generate_repobeats_style_svg(self, data: Dict, theme: str = "default") -> str:
        """Generate exact RepoBeats-style comprehensive dashboard SVG"""
        colors = self.get_theme_colors(theme)

        # Safe data extraction with defaults
        repo = data.get("repository", {})
        stats = data.get("statistics", {})
        contributors = data.get("contributors", [])

        # SVG dimensions matching RepoBeats
        width = 900
        height = 400

        svg_parts = [
            f'<svg width="{width}" height="{height}" xmlns="http://www.w3.org/2000/svg">',
            # Background with subtle border
            f'<rect width="{width}" height="{height}" fill="{colors["background"]}" stroke="#e1e4e8" stroke-width="1" rx="6"/>',

            # Header with contributions summary
            self._generate_repobeats_header(15, 15, width-30, data, colors),

            # Main metrics row (3 cards)
            self._generate_repobeats_metrics(15, 70, width-30, data, colors),

            # Charts section (3 charts side by side)
            self._generate_repobeats_charts(15, 160, width-30, 180, data, colors),

            # Contributors section with GitHub-style heatmaps
            self._generate_repobeats_contributors(15, 350, width-30, contributors, colors),

            '</svg>'
        ]

        return '\n'.join(svg_parts)

    def _generate_contributions_header(self, x: int, y: int, width: int, data: Dict, colors: Dict) -> str:
        """Generate the contributions summary header"""
        stats = data["statistics"]
        total_commits = stats.get("total_commits", 0)

        # Generate activity dots (simplified representation)
        dots = []
        for i in range(52):  # 52 weeks
            dot_x = x + 300 + (i * 8)
            if dot_x > x + width - 10:
                break
            intensity = min(1.0, (i % 7) * 0.2 + 0.1)  # Simplified pattern
            dot_color = colors["success"] if intensity > 0.5 else colors["border"]
            dots.append(f'<rect x="{dot_x}" y="{y+5}" width="6" height="6" fill="{dot_color}" rx="1" opacity="{0.3 + intensity * 0.7}"/>')

        return f'''
        <g>
            <text x="{x}" y="{y+15}" font-family="Arial, sans-serif" font-size="14" font-weight="bold" fill="{colors["accent"]}">{total_commits} Contributions in the Last 30 Days</text>
            {''.join(dots)}
        </g>'''

    def _generate_metrics_row(self, x: int, y: int, width: int, data: Dict, colors: Dict) -> str:
        """Generate the main metrics row with colorful indicators"""
        repo = data["repository"]
        stats = data["statistics"]

        # Calculate metrics
        total_issues = stats.get("total_issues", 1)
        open_issues = stats.get("open_issues", 0)
        issue_ratio = open_issues / max(total_issues, 1)
        pr_opened = min(stats.get("open_issues", 0), 100)  # Simplified - would need separate PR data
        commits = stats.get("total_commits", 0)

        metric_width = width // 3

        return f'''
        <g>
            <!-- Issue Ratio -->
            <g>
                <text x="{x}" y="{y+15}" font-family="Arial, sans-serif" font-size="16" font-weight="bold" fill="{colors["text_primary"]}">{issue_ratio:.2f} Opened/Closed Issue Ratio</text>
                <text x="{x}" y="{y+35}" font-family="Arial, sans-serif" font-size="12" fill="{colors["text_secondary"]}">0 (-0.27%)</text>
                <text x="{x}" y="{y+50}" font-family="Arial, sans-serif" font-size="10" fill="{colors["danger"]}">↓ past month</text>
            </g>

            <!-- Pull Requests -->
            <g>
                <text x="{x + metric_width}" y="{y+15}" font-family="Arial, sans-serif" font-size="16" font-weight="bold" fill="{colors["text_primary"]}">{pr_opened} Pull Requests Opened</text>
                <text x="{x + metric_width}" y="{y+35}" font-family="Arial, sans-serif" font-size="12" fill="{colors["text_secondary"]}">-20 (-30.3%)</text>
                <text x="{x + metric_width}" y="{y+50}" font-family="Arial, sans-serif" font-size="10" fill="{colors["danger"]}">↓ past month</text>
            </g>

            <!-- Commits -->
            <g>
                <text x="{x + metric_width * 2}" y="{y+15}" font-family="Arial, sans-serif" font-size="16" font-weight="bold" fill="{colors["text_primary"]}">{commits} Commits</text>
                <text x="{x + metric_width * 2}" y="{y+35}" font-family="Arial, sans-serif" font-size="12" fill="{colors["text_secondary"]}">-35 (-35.35%)</text>
                <text x="{x + metric_width * 2}" y="{y+50}" font-family="Arial, sans-serif" font-size="10" fill="{colors["danger"]}">↓ past month</text>
            </g>
        </g>'''

    def _generate_charts_section(self, x: int, y: int, width: int, height: int, data: Dict, colors: Dict) -> str:
        """Generate the colorful charts section"""
        chart_width = width // 3 - 20
        chart_height = height - 40

        # Chart colors using theme palette
        issue_colors = [colors["blue"], colors["indigo"]]
        pr_colors = [colors["purple"], colors["pink"]]
        commit_colors = [colors["orange"], colors["red"]]

        charts = []

        # Issues chart
        charts.append(self._generate_bar_chart(
            x, y + 30, chart_width, chart_height - 30,
            "Issues", ["Opened", "Closed"],
            issue_colors,
            data, colors
        ))

        # Pull Requests chart
        charts.append(self._generate_bar_chart(
            x + chart_width + 20, y + 30, chart_width, chart_height - 30,
            "Pull Requests", ["Opened", "Closed"],
            pr_colors,
            data, colors
        ))

        # Pushes & Commits chart
        charts.append(self._generate_bar_chart(
            x + (chart_width + 20) * 2, y + 30, chart_width, chart_height - 30,
            "Pushes & Commits", ["Pushes", "Commits"],
            commit_colors,
            data, colors
        ))

        return '\n'.join(charts)

    def _generate_bar_chart(self, x: int, y: int, width: int, height: int, title: str,
                           labels: List[str], chart_colors: List[str], data: Dict, colors: Dict) -> str:
        """Generate a colorful bar chart"""
        stats = data["statistics"]

        # Sample data - in real implementation, this would come from actual data
        if "Issues" in title:
            values = [stats.get("open_issues", 0), stats.get("closed_issues", 0)]
        elif "Pull" in title:
            values = [stats.get("open_issues", 0) // 2, stats.get("closed_issues", 0) // 2]  # Simplified
        else:
            values = [stats.get("total_commits", 0) // 4, stats.get("total_commits", 0)]  # Simplified

        max_value = max(values) if values else 1

        chart_parts = [
            f'<text x="{x}" y="{y-10}" font-family="Arial, sans-serif" font-size="12" font-weight="bold" fill="{colors["text_primary"]}">{title}</text>'
        ]

        # Generate bars for each week (simplified to 12 weeks)
        bar_width = width // 12
        for week in range(12):
            for i, (label, color, value) in enumerate(zip(labels, chart_colors, values)):
                # Simulate weekly variation
                weekly_value = max(0, value * (0.5 + (week % 4) * 0.25) * (0.8 + i * 0.4))
                bar_height = (weekly_value / max_value) * height * 0.8 if max_value > 0 else 0

                bar_x = x + week * bar_width + i * (bar_width // len(labels))
                bar_y = y + height - bar_height
                bar_w = bar_width // len(labels) - 2

                chart_parts.append(
                    f'<rect x="{bar_x}" y="{bar_y}" width="{bar_w}" height="{bar_height}" '
                    f'fill="{color}" rx="1" opacity="0.8"/>'
                )

        # Add legend
        legend_y = y + height + 15
        for i, (label, color) in enumerate(zip(labels, chart_colors)):
            legend_x = x + i * 80
            chart_parts.extend([
                f'<circle cx="{legend_x}" cy="{legend_y}" r="4" fill="{color}"/>',
                f'<text x="{legend_x + 10}" y="{legend_y + 4}" font-family="Arial, sans-serif" font-size="10" fill="{colors["text_primary"]}">{label}</text>'
            ])

        return '\n'.join(chart_parts)

    def _generate_contributors_heatmap(self, x: int, y: int, width: int, contributors: List, colors: Dict) -> str:
        """Generate contributors section with GitHub-style heatmaps"""
        if not contributors:
            return f'<text x="{x}" y="{y+15}" font-family="Arial, sans-serif" font-size="12" fill="{colors["text_secondary"]}">No contributors data</text>'

        heatmap_parts = [
            f'<text x="{x}" y="{y}" font-family="Arial, sans-serif" font-size="14" font-weight="bold" fill="{colors["text_primary"]}">+ Top Contributors</text>'
        ]

        # Show top 5 contributors with mini heatmaps
        contributor_width = width // 5
        for i, contributor in enumerate(contributors[:5]):
            if i >= 5:
                break

            contrib_x = x + i * contributor_width
            contrib_y = y + 20

            username = contributor.get("login", f"User{i+1}")
            contributions = contributor.get("contributions", 0)

            # Contributor name
            heatmap_parts.append(
                f'<text x="{contrib_x}" y="{contrib_y}" font-family="Arial, sans-serif" font-size="11" font-weight="bold" fill="{colors["text_primary"]}">{username}</text>'
            )

            # Mini heatmap (7x7 grid representing weeks)
            cell_size = 3
            for week in range(7):
                for day in range(7):
                    cell_x = contrib_x + day * (cell_size + 1)
                    cell_y = contrib_y + 10 + week * (cell_size + 1)

                    # Simulate activity intensity
                    intensity = min(1.0, ((week + day + i) % 5) * 0.25)
                    opacity = 0.1 + intensity * 0.9

                    heatmap_parts.append(
                        f'<rect x="{cell_x}" y="{cell_y}" width="{cell_size}" height="{cell_size}" '
                        f'fill="{colors["success"]}" opacity="{opacity}" rx="0.5"/>'
                    )

        return '\n'.join(heatmap_parts)

    def _generate_repobeats_header(self, x: int, y: int, width: int, data: Dict, colors: Dict) -> str:
        """Generate exact RepoBeats-style header with contribution dots"""
        stats = data["statistics"]
        total_commits = stats.get("total_commits", 240)  # Default for demo

        # Pink/magenta color for contributions
        contrib_color = "#ff69b4" if colors["background"] == "#ffffff" else "#ff69b4"

        # Generate 52 contribution dots
        dots = []
        dot_size = 4
        dot_spacing = 6
        start_x = x + 400  # Position dots to the right

        for i in range(52):
            dot_x = start_x + (i * dot_spacing)
            if dot_x > x + width - dot_size:
                break

            # Simulate realistic contribution pattern
            intensity = 0.1 + (i % 7) * 0.15 + (i % 3) * 0.1
            if i % 7 == 0 or i % 7 == 6:  # Weekends - less activity
                intensity *= 0.3

            opacity = min(1.0, intensity)
            dot_color = contrib_color if opacity > 0.4 else "#ebedf0"

            dots.append(f'<rect x="{dot_x}" y="{y+5}" width="{dot_size}" height="{dot_size}" fill="{dot_color}" rx="1"/>')

        return f'''
        <g>
            <rect x="{x}" y="{y}" width="30" height="15" fill="{contrib_color}" rx="2"/>
            <text x="{x+40}" y="{y+12}" font-family="-apple-system,BlinkMacSystemFont,Segoe UI,Helvetica,Arial,sans-serif" font-size="14" font-weight="600" fill="{contrib_color}">{total_commits} Contributions in the Last 30 Days</text>
            {''.join(dots)}
        </g>'''

    def _generate_repobeats_metrics(self, x: int, y: int, width: int, data: Dict, colors: Dict) -> str:
        """Generate exact RepoBeats-style metrics cards"""
        stats = data["statistics"]

        # Calculate realistic metrics
        total_issues = stats.get("total_issues", 100)
        open_issues = stats.get("open_issues", 50)
        closed_issues = total_issues - open_issues
        issue_ratio = open_issues / max(total_issues, 1) if total_issues > 0 else 0.68

        pr_opened = min(stats.get("open_issues", 46), 100)
        commits = min(stats.get("total_commits", 64), 200)

        card_width = (width - 40) // 3

        return f'''
        <g>
            <!-- Issue Ratio Card -->
            <rect x="{x}" y="{y}" width="{card_width}" height="70" fill="{colors["background"]}" stroke="#e1e4e8" rx="6"/>
            <text x="{x+15}" y="{y+20}" font-family="-apple-system,BlinkMacSystemFont,Segoe UI,Helvetica,Arial,sans-serif" font-size="16" font-weight="600" fill="#0969da">{issue_ratio:.2f} Opened/Closed Issue Ratio</text>
            <text x="{x+15}" y="{y+40}" font-family="-apple-system,BlinkMacSystemFont,Segoe UI,Helvetica,Arial,sans-serif" font-size="14" fill="#656d76">0 (-0.27%)</text>
            <text x="{x+15}" y="{y+55}" font-family="-apple-system,BlinkMacSystemFont,Segoe UI,Helvetica,Arial,sans-serif" font-size="12" fill="#cf222e">v past month</text>

            <!-- Pull Requests Card -->
            <rect x="{x + card_width + 20}" y="{y}" width="{card_width}" height="70" fill="{colors["background"]}" stroke="#e1e4e8" rx="6"/>
            <text x="{x + card_width + 35}" y="{y+20}" font-family="-apple-system,BlinkMacSystemFont,Segoe UI,Helvetica,Arial,sans-serif" font-size="16" font-weight="600" fill="#8250df">{pr_opened} Pull Requests Opened</text>
            <text x="{x + card_width + 35}" y="{y+40}" font-family="-apple-system,BlinkMacSystemFont,Segoe UI,Helvetica,Arial,sans-serif" font-size="14" fill="#656d76">-20 (-30.3%)</text>
            <text x="{x + card_width + 35}" y="{y+55}" font-family="-apple-system,BlinkMacSystemFont,Segoe UI,Helvetica,Arial,sans-serif" font-size="12" fill="#cf222e">v past month</text>

            <!-- Commits Card -->
            <rect x="{x + (card_width + 20) * 2}" y="{y}" width="{card_width}" height="70" fill="{colors["background"]}" stroke="#e1e4e8" rx="6"/>
            <text x="{x + (card_width + 20) * 2 + 15}" y="{y+20}" font-family="-apple-system,BlinkMacSystemFont,Segoe UI,Helvetica,Arial,sans-serif" font-size="16" font-weight="600" fill="#d1242f">{commits} Commits</text>
            <text x="{x + (card_width + 20) * 2 + 15}" y="{y+40}" font-family="-apple-system,BlinkMacSystemFont,Segoe UI,Helvetica,Arial,sans-serif" font-size="14" fill="#656d76">-35 (-35.35%)</text>
            <text x="{x + (card_width + 20) * 2 + 15}" y="{y+55}" font-family="-apple-system,BlinkMacSystemFont,Segoe UI,Helvetica,Arial,sans-serif" font-size="12" fill="#cf222e">v past month</text>
        </g>'''

    def _generate_repobeats_charts(self, x: int, y: int, width: int, height: int, data: Dict, colors: Dict) -> str:
        """Generate exact RepoBeats-style charts section"""
        chart_width = (width - 40) // 3
        chart_height = height - 60

        # Exact RepoBeats colors
        issue_blue = "#0969da"
        issue_dark_blue = "#0550ae"
        pr_purple = "#8250df"
        pr_dark_purple = "#6639ba"
        commit_orange = "#fd7e14"
        commit_red = "#d1242f"

        charts = []

        # Issues Chart
        charts.append(self._generate_repobeats_chart(
            x, y, chart_width, chart_height,
            "Issues", "Opened", "Closed",
            issue_blue, issue_dark_blue, data
        ))

        # Pull Requests Chart
        charts.append(self._generate_repobeats_chart(
            x + chart_width + 20, y, chart_width, chart_height,
            "Pull Requests", "Opened", "Closed",
            pr_purple, pr_dark_purple, data
        ))

        # Pushes & Commits Chart
        charts.append(self._generate_repobeats_chart(
            x + (chart_width + 20) * 2, y, chart_width, chart_height,
            "Pushes & Commits", "Pushes", "Commits",
            commit_orange, commit_red, data
        ))

        return '\n'.join(charts)

    def _generate_repobeats_chart(self, x: int, y: int, width: int, height: int,
                                 title: str, label1: str, label2: str,
                                 color1: str, color2: str, data: Dict) -> str:
        """Generate individual RepoBeats-style chart"""
        stats = data["statistics"]

        # Chart title with icon (using simple ASCII symbols to avoid XML parsing issues)
        icon = "O" if "Issues" in title else (">" if "Pull" in title else "*")

        chart_parts = [
            f'<g>',
            f'<text x="{x}" y="{y+15}" font-family="-apple-system,BlinkMacSystemFont,Segoe UI,Helvetica,Arial,sans-serif" font-size="14" font-weight="600" fill="#24292f">{icon} {title}</text>'
        ]

        # Generate realistic bar chart data (12 weeks)
        bar_width = (width - 20) // 12
        max_height = height - 80

        for week in range(12):
            # Simulate weekly data with realistic patterns
            if "Issues" in title:
                val1 = max(0, 5 + (week % 4) * 3 + (week % 2) * 2)  # Opened
                val2 = max(0, 3 + (week % 3) * 2 + (week % 5) * 1)  # Closed
            elif "Pull" in title:
                val1 = max(0, 3 + (week % 3) * 2 + (week % 4) * 1)  # Opened
                val2 = max(0, 2 + (week % 2) * 3 + (week % 6) * 1)  # Closed
            else:  # Commits
                val1 = max(0, 8 + (week % 5) * 4 + (week % 3) * 2)  # Pushes
                val2 = max(0, 12 + (week % 4) * 6 + (week % 2) * 3)  # Commits

            max_val = max(val1, val2, 1)

            # Bar 1 (left)
            bar1_height = (val1 / max_val) * max_height * 0.6
            bar1_x = x + 10 + week * bar_width
            bar1_y = y + height - 40 - bar1_height

            # Bar 2 (right)
            bar2_height = (val2 / max_val) * max_height * 0.6
            bar2_x = x + 10 + week * bar_width + bar_width // 2
            bar2_y = y + height - 40 - bar2_height

            chart_parts.extend([
                f'<rect x="{bar1_x}" y="{bar1_y}" width="{bar_width//2-1}" height="{bar1_height}" fill="{color1}" rx="1"/>',
                f'<rect x="{bar2_x}" y="{bar2_y}" width="{bar_width//2-1}" height="{bar2_height}" fill="{color2}" rx="1"/>'
            ])

        # Legend
        legend_y = y + height - 25
        chart_parts.extend([
            f'<circle cx="{x+10}" cy="{legend_y}" r="4" fill="{color1}"/>',
            f'<text x="{x+20}" y="{legend_y+4}" font-family="-apple-system,BlinkMacSystemFont,Segoe UI,Helvetica,Arial,sans-serif" font-size="12" fill="#656d76">{label1}</text>',
            f'<circle cx="{x+80}" cy="{legend_y}" r="4" fill="{color2}"/>',
            f'<text x="{x+90}" y="{legend_y+4}" font-family="-apple-system,BlinkMacSystemFont,Segoe UI,Helvetica,Arial,sans-serif" font-size="12" fill="#656d76">{label2}</text>',
            f'</g>'
        ])

        return '\n'.join(chart_parts)

    def _generate_repobeats_contributors(self, x: int, y: int, width: int, contributors: List, colors: Dict) -> str:
        """Generate exact RepoBeats-style contributors section"""
        # Default contributor names if no data
        default_contributors = ["tommoor", "hmacr", "HalfVoxel", "outline-trans", "TimeToCodeSom"]

        contributor_names = []
        if contributors and len(contributors) > 0:
            contributor_names = [c.get("login", f"user{i}") for i, c in enumerate(contributors[:5])]
        else:
            contributor_names = default_contributors

        # Ensure we have exactly 5 contributors
        while len(contributor_names) < 5:
            contributor_names.append(f"contributor{len(contributor_names)+1}")
        contributor_names = contributor_names[:5]

        heatmap_parts = [
            f'<text x="{x}" y="{y+15}" font-family="-apple-system,BlinkMacSystemFont,Segoe UI,Helvetica,Arial,sans-serif" font-size="14" font-weight="600" fill="#24292f">+ Top Contributors</text>'
        ]

        # Generate 5 contributor heatmaps side by side
        contributor_width = (width - 40) // 5

        for i, username in enumerate(contributor_names):
            contrib_x = x + i * (contributor_width + 10)
            contrib_y = y + 25

            # Contributor name
            heatmap_parts.append(
                f'<text x="{contrib_x}" y="{contrib_y}" font-family="-apple-system,BlinkMacSystemFont,Segoe UI,Helvetica,Arial,sans-serif" font-size="12" font-weight="500" fill="#24292f">{username}</text>'
            )

            # GitHub-style contribution heatmap (7 days x 8 weeks = 56 squares)
            cell_size = 3
            cell_gap = 1
            heatmap_width = 7 * (cell_size + cell_gap)
            heatmap_height = 8 * (cell_size + cell_gap)

            # Different shades of green for contributions
            contribution_colors = [
                "#ebedf0",  # No contributions
                "#9be9a8",  # Low
                "#40c463",  # Medium-low
                "#30a14e",  # Medium
                "#216e39"   # High
            ]

            for week in range(8):  # 8 weeks
                for day in range(7):  # 7 days
                    cell_x = contrib_x + day * (cell_size + cell_gap)
                    cell_y = contrib_y + 10 + week * (cell_size + cell_gap)

                    # Simulate contribution intensity
                    intensity = (week + day + i) % 5
                    # Weekend pattern (less activity on weekends)
                    if day == 0 or day == 6:
                        intensity = max(0, intensity - 2)

                    cell_color = contribution_colors[intensity]

                    heatmap_parts.append(
                        f'<rect x="{cell_x}" y="{cell_y}" width="{cell_size}" height="{cell_size}" fill="{cell_color}" rx="0.5"/>'
                    )

        return '\n'.join(heatmap_parts)

    def generate_modern_dark_dashboard(self, data: Dict, theme: str = "dark") -> str:
        """Generate modern dark dashboard matching the sleek design"""
        # Modern dark color scheme
        colors = {
            "background": "#1a1a1a",
            "card_bg": "#2d2d2d",
            "border": "#404040",
            "text_primary": "#ffffff",
            "text_secondary": "#a0a0a0",
            "accent": "#00ff88",
            "purple": "#8b5cf6",
            "green": "#10b981",
            "red": "#ef4444",
            "orange": "#f59e0b"
        }

        # Safe data extraction with defaults
        repo = data.get("repository", {})
        stats = data.get("statistics", {})

        # SVG dimensions
        width = 500
        height = 300

        svg_parts = [
            f'<svg width="{width}" height="{height}" xmlns="http://www.w3.org/2000/svg">',
            f'<rect width="{width}" height="{height}" fill="{colors["background"]}" rx="12"/>',

            # Main content card
            f'<rect x="20" y="20" width="{width-40}" height="{height-40}" fill="{colors["card_bg"]}" stroke="{colors["border"]}" stroke-width="1" rx="8"/>',

            # Repository name
            f'<text x="35" y="45" font-family="Inter, -apple-system, sans-serif" font-size="14" font-weight="500" fill="{colors["text_secondary"]}">Repo name</text>',

            # Chart area
            self._generate_modern_chart_area(35, 60, 280, 160, data, colors),

            # Stats circle on the right
            self._generate_modern_stats_circle(340, 60, 100, 160, data, colors),

            '</svg>'
        ]

        return '\n'.join(svg_parts)

    def _generate_modern_chart_area(self, x: int, y: int, width: int, height: int, data: Dict, colors: Dict) -> str:
        """Generate modern line chart area"""
        stats = data["statistics"]

        # Generate sample data points for the chart
        points_green = []
        points_purple = []

        # Create realistic chart data
        for i in range(20):
            # Green line (commits)
            green_y = y + height - (30 + i * 2 + (i % 4) * 15 + (i % 7) * 10)
            green_x = x + (i * width // 19)
            points_green.append(f"{green_x},{green_y}")

            # Purple line (pushes)
            purple_y = y + height - (20 + i * 3 + (i % 3) * 12 + (i % 5) * 8)
            purple_x = x + (i * width // 19)
            points_purple.append(f"{purple_x},{purple_y}")

        chart_parts = [
            # Chart background
            f'<rect x="{x}" y="{y}" width="{width}" height="{height}" fill="none" stroke="{colors["border"]}" stroke-width="1" rx="4"/>',

            # Green line (commits)
            f'<polyline points="{" ".join(points_green)}" fill="none" stroke="{colors["green"]}" stroke-width="2" opacity="0.8"/>',

            # Purple line (pushes)
            f'<polyline points="{" ".join(points_purple)}" fill="none" stroke="{colors["purple"]}" stroke-width="2" opacity="0.8"/>',

            # Add some glow effect
            f'<polyline points="{" ".join(points_green)}" fill="none" stroke="{colors["green"]}" stroke-width="4" opacity="0.2"/>',
            f'<polyline points="{" ".join(points_purple)}" fill="none" stroke="{colors["purple"]}" stroke-width="4" opacity="0.2"/>',
        ]

        return '\n'.join(chart_parts)

    def _generate_modern_stats_circle(self, x: int, y: int, width: int, height: int, data: Dict, colors: Dict) -> str:
        """Generate modern circular stats display"""
        stats = data["statistics"]

        # Stats text
        push_count = min(stats.get("total_commits", 24) // 4, 99)
        commit_count = min(stats.get("total_commits", 64), 999)

        # Circle center
        center_x = x + width // 2
        center_y = y + height // 2
        radius = 35

        # Create donut chart segments
        total = push_count + commit_count
        if total > 0:
            # Calculate angles
            push_angle = (push_count / total) * 360
            commit_angle = (commit_count / total) * 360

            # Convert to radians for path calculation
            import math
            push_rad = math.radians(push_angle)
            commit_rad = math.radians(commit_angle)

            # Create arc paths
            push_end_x = center_x + radius * math.cos(push_rad - math.pi/2)
            push_end_y = center_y + radius * math.sin(push_rad - math.pi/2)

            commit_start_x = push_end_x
            commit_start_y = push_end_y
            commit_end_x = center_x + radius * math.cos(-math.pi/2)
            commit_end_y = center_y + radius * math.sin(-math.pi/2)
        else:
            push_end_x = center_x
            push_end_y = center_y - radius
            commit_start_x = center_x
            commit_start_y = center_y - radius
            commit_end_x = center_x
            commit_end_y = center_y - radius

        circle_parts = [
            # Stats labels
            f'<text x="{x}" y="{y-10}" font-family="Inter, -apple-system, sans-serif" font-size="12" font-weight="500" fill="{colors["text_secondary"]}">Push : count</text>',
            f'<text x="{x}" y="{y+5}" font-family="Inter, -apple-system, sans-serif" font-size="12" font-weight="500" fill="{colors["text_secondary"]}">Commit: count</text>',

            # Outer circle background
            f'<circle cx="{center_x}" cy="{center_y}" r="{radius}" fill="none" stroke="{colors["border"]}" stroke-width="8"/>',

            # Push segment (orange/red)
            f'<circle cx="{center_x}" cy="{center_y}" r="{radius}" fill="none" stroke="{colors["orange"]}" stroke-width="8" stroke-dasharray="{push_angle * 2.8} 628" stroke-dashoffset="0" transform="rotate(-90 {center_x} {center_y})"/>',

            # Commit segment (green)
            f'<circle cx="{center_x}" cy="{center_y}" r="{radius}" fill="none" stroke="{colors["green"]}" stroke-width="8" stroke-dasharray="{commit_angle * 2.8} 628" stroke-dashoffset="-{push_angle * 2.8}" transform="rotate(-90 {center_x} {center_y})"/>',

            # Inner circle with gradient
            f'<circle cx="{center_x}" cy="{center_y}" r="{radius-15}" fill="url(#modernGradient)"/>',

            # Gradient definition
            f'<defs>',
            f'<radialGradient id="modernGradient" cx="50%" cy="50%" r="50%">',
            f'<stop offset="0%" style="stop-color:{colors["purple"]};stop-opacity:0.8"/>',
            f'<stop offset="100%" style="stop-color:{colors["card_bg"]};stop-opacity:1"/>',
            f'</radialGradient>',
            f'</defs>',

            # Center stats
            f'<text x="{center_x}" y="{center_y-5}" font-family="Inter, -apple-system, sans-serif" font-size="14" font-weight="600" fill="{colors["text_primary"]}" text-anchor="middle">{push_count}</text>',
            f'<text x="{center_x}" y="{center_y+10}" font-family="Inter, -apple-system, sans-serif" font-size="14" font-weight="600" fill="{colors["text_primary"]}" text-anchor="middle">{commit_count}</text>',
        ]

        return '\n'.join(circle_parts)

    def generate_animated_text(self, text: str = "Hello World", font_size: int = 24,
                             color: str = "#ffffff", bg_color: str = "#000000",
                             speed: float = 0.5, theme: str = "default") -> str:
        """Generate animated text SVG with typing and untyping effect"""

        # Handle empty text
        if not text or text.strip() == "":
            text = "Hello World"

        # Theme-based colors
        if theme == "dark":
            bg_color = "#0d1117"
            color = "#f0f6fc"
        elif theme == "light":
            bg_color = "#ffffff"
            color = "#24292f"
        elif theme == "matrix":
            bg_color = "#000000"
            color = "#00ff00"
        elif theme == "neon":
            bg_color = "#1a1a2e"
            color = "#16213e"

        # Calculate dimensions
        char_width = font_size * 0.6  # Approximate character width
        text_width = len(text) * char_width
        padding = 40
        width = max(400, int(text_width + padding * 2))
        height = font_size + padding * 2

        # Animation timing
        char_duration = speed  # seconds per character
        total_type_time = len(text) * char_duration
        pause_time = 1.0  # pause at full text
        total_untype_time = len(text) * char_duration * 0.7  # untype faster
        total_animation_time = total_type_time + pause_time + total_untype_time

        # Generate keyframes for typing effect
        typing_keyframes = []
        untyping_keyframes = []

        # Typing animation keyframes
        for i in range(len(text) + 1):
            time_percent = (i * char_duration / total_animation_time) * 100
            visible_text = text[:i]
            typing_keyframes.append(f'{time_percent:.1f}% {{ opacity: 1; }} ')

        # Pause keyframe
        pause_start = (total_type_time / total_animation_time) * 100
        pause_end = ((total_type_time + pause_time) / total_animation_time) * 100

        # Untyping animation keyframes
        untype_start = pause_end
        for i in range(len(text), -1, -1):
            progress = (len(text) - i) / len(text)
            time_percent = untype_start + (progress * (total_untype_time / total_animation_time) * 100)
            untyping_keyframes.append(f'{time_percent:.1f}% {{ opacity: 1; }} ')

        # Create individual character animations
        char_animations = []
        for i, char in enumerate(text):
            # When this character appears (typing)
            appear_time = (i * char_duration / total_animation_time) * 100
            # When this character disappears (untyping)
            disappear_time = pause_end + ((len(text) - i - 1) * char_duration * 0.7 / total_animation_time) * 100

            char_x = padding + i * char_width
            char_y = padding + font_size * 0.7

            char_animations.append(f'''
                <text x="{char_x}" y="{char_y}"
                      font-family="'Courier New', monospace"
                      font-size="{font_size}"
                      font-weight="bold"
                      fill="{color}"
                      opacity="0">
                    {char}
                    <animate attributeName="opacity"
                             values="0;1;1;0;0"
                             dur="{total_animation_time}s"
                             keyTimes="0;{appear_time/100:.3f};{pause_end/100:.3f};{disappear_time/100:.3f};1"
                             repeatCount="indefinite"/>
                </text>''')

        # Cursor animation
        cursor_x = padding + len(text) * char_width + 5
        cursor_y = char_y

        svg_parts = [
            f'<svg width="{width}" height="{height}" xmlns="http://www.w3.org/2000/svg">',
            f'<rect width="{width}" height="{height}" fill="{bg_color}"/>',

            # Add subtle background pattern for some themes
            self._generate_background_pattern(width, height, theme),

            # Animated characters
            *char_animations,

            # Blinking cursor
            f'''<text x="{cursor_x}" y="{cursor_y}"
                      font-family="'Courier New', monospace"
                      font-size="{font_size}"
                      font-weight="bold"
                      fill="{color}">
                |
                <animate attributeName="opacity"
                         values="1;0;1"
                         dur="1s"
                         repeatCount="indefinite"/>
            </text>''',

            # Title/watermark
            f'<text x="{width-10}" y="{height-10}" font-family="Arial, sans-serif" font-size="8" fill="{color}" opacity="0.3" text-anchor="end">Animated by RepoStats API</text>',

            '</svg>'
        ]

        return '\n'.join(svg_parts)

    def _generate_background_pattern(self, width: int, height: int, theme: str) -> str:
        """Generate background pattern based on theme"""
        if theme == "matrix":
            return f'''
                <defs>
                    <pattern id="matrix" x="0" y="0" width="20" height="20" patternUnits="userSpaceOnUse">
                        <rect width="20" height="20" fill="#000000"/>
                        <text x="10" y="15" font-family="monospace" font-size="10" fill="#003300" text-anchor="middle" opacity="0.3">0</text>
                    </pattern>
                </defs>
                <rect width="{width}" height="{height}" fill="url(#matrix)"/>
            '''
        elif theme == "neon":
            return f'''
                <defs>
                    <radialGradient id="neonGlow" cx="50%" cy="50%" r="50%">
                        <stop offset="0%" style="stop-color:#16213e;stop-opacity:0.8"/>
                        <stop offset="100%" style="stop-color:#1a1a2e;stop-opacity:1"/>
                    </radialGradient>
                </defs>
                <rect width="{width}" height="{height}" fill="url(#neonGlow)"/>
            '''
        else:
            return ""
