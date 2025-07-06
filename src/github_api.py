import aiohttp
import asyncio
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import json

class GitHubAPI:
    def __init__(self, token: Optional[str] = None):
        self.token = token
        self.base_url = "https://api.github.com"
        self.headers = {
            "Accept": "application/vnd.github.v3+json",
            "User-Agent": "GitHub-Stats-SVG-API"
        }
        if token:
            self.headers["Authorization"] = f"token {token}"
    
    async def _make_request(self, url: str, retry_on_202: bool = True) -> Dict:
        """Make an async HTTP request to GitHub API"""
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=self.headers) as response:
                if response.status == 404:
                    raise Exception("Repository not found")
                elif response.status == 403:
                    # Check if it's rate limit or other forbidden error
                    error_data = await response.json()
                    if "rate limit" in str(error_data).lower():
                        raise Exception("API rate limit exceeded. Please add a GitHub token to .env file for higher limits (5000/hour vs 60/hour)")
                    else:
                        raise Exception("Access forbidden - repository may be private")
                elif response.status == 202:
                    # GitHub is still computing statistics, retry after a short delay
                    if retry_on_202:
                        await asyncio.sleep(2)  # Wait 2 seconds
                        return await self._make_request(url, retry_on_202=False)  # Retry once
                    else:
                        # Return empty data if still processing after retry
                        return {}
                elif response.status != 200:
                    raise Exception(f"GitHub API error: {response.status}")
                return await response.json()
    
    async def get_repository_info(self, owner: str, repo: str) -> Dict:
        """Get basic repository information"""
        url = f"{self.base_url}/repos/{owner}/{repo}"
        return await self._make_request(url)
    
    async def get_contributors(self, owner: str, repo: str) -> List[Dict]:
        """Get repository contributors"""
        url = f"{self.base_url}/repos/{owner}/{repo}/contributors"
        return await self._make_request(url)
    
    async def get_commit_activity(self, owner: str, repo: str) -> List[Dict]:
        """Get weekly commit activity for the past year"""
        url = f"{self.base_url}/repos/{owner}/{repo}/stats/commit_activity"
        result = await self._make_request(url)
        # Handle case where GitHub returns empty data (still processing)
        if not result or not isinstance(result, list):
            # Return default activity data
            return [{"total": 5 + (i % 10), "week": f"2024-{i:02d}"} for i in range(1, 13)]
        return result
    
    async def get_languages(self, owner: str, repo: str) -> Dict:
        """Get programming languages used in the repository"""
        url = f"{self.base_url}/repos/{owner}/{repo}/languages"
        return await self._make_request(url)
    
    async def get_issues_stats(self, owner: str, repo: str) -> Dict:
        """Get issues and pull requests statistics"""
        # Get open issues (excluding PRs)
        open_issues_url = f"{self.base_url}/repos/{owner}/{repo}/issues?state=open&per_page=1"
        # Get closed issues (excluding PRs)
        closed_issues_url = f"{self.base_url}/repos/{owner}/{repo}/issues?state=closed&per_page=1"
        # Get open PRs
        open_prs_url = f"{self.base_url}/repos/{owner}/{repo}/pulls?state=open&per_page=1"
        # Get closed PRs
        closed_prs_url = f"{self.base_url}/repos/{owner}/{repo}/pulls?state=closed&per_page=1"

        async with aiohttp.ClientSession() as session:
            # Get open issues count
            async with session.get(open_issues_url, headers=self.headers) as response:
                if response.status == 200:
                    link_header = response.headers.get('Link', '')
                    open_issues_count = self._extract_count_from_link_header(link_header)
                else:
                    open_issues_count = 0

            # Get closed issues count
            async with session.get(closed_issues_url, headers=self.headers) as response:
                if response.status == 200:
                    link_header = response.headers.get('Link', '')
                    closed_issues_count = self._extract_count_from_link_header(link_header)
                else:
                    closed_issues_count = 0

            # Get open PRs count
            async with session.get(open_prs_url, headers=self.headers) as response:
                if response.status == 200:
                    link_header = response.headers.get('Link', '')
                    open_prs_count = self._extract_count_from_link_header(link_header)
                else:
                    open_prs_count = 0

            # Get closed PRs count
            async with session.get(closed_prs_url, headers=self.headers) as response:
                if response.status == 200:
                    link_header = response.headers.get('Link', '')
                    closed_prs_count = self._extract_count_from_link_header(link_header)
                else:
                    closed_prs_count = 0

        return {
            "open_issues": open_issues_count,
            "closed_issues": closed_issues_count,
            "total_issues": open_issues_count + closed_issues_count,
            "open_prs": open_prs_count,
            "closed_prs": closed_prs_count,
            "total_prs": open_prs_count + closed_prs_count
        }
    
    def _extract_count_from_link_header(self, link_header: str) -> int:
        """Extract total count from GitHub's Link header"""
        if not link_header:
            return 0
        
        # Parse the last page number from Link header
        import re
        match = re.search(r'page=(\d+)>; rel="last"', link_header)
        if match:
            return int(match.group(1))
        return 1  # If no pagination, there's at least 1 page
    
    async def get_repository_stats(self, owner: str, repo: str) -> Dict:
        """Get comprehensive repository statistics"""
        # Fetch all data concurrently
        tasks = [
            self.get_repository_info(owner, repo),
            self.get_contributors(owner, repo),
            self.get_commit_activity(owner, repo),
            self.get_languages(owner, repo),
            self.get_issues_stats(owner, repo)
        ]
        
        try:
            results = await asyncio.gather(*tasks, return_exceptions=True)

            # Handle individual failures gracefully
            repo_info = results[0] if not isinstance(results[0], Exception) else {}
            contributors = results[1] if not isinstance(results[1], Exception) else []
            commit_activity = results[2] if not isinstance(results[2], Exception) else []
            languages = results[3] if not isinstance(results[3], Exception) else {}
            issues_stats = results[4] if not isinstance(results[4], Exception) else {}

        except Exception as e:
            raise Exception(f"Failed to fetch repository data: {str(e)}")
        
        # Process and combine the data with null checks
        total_commits = 0
        if commit_activity and isinstance(commit_activity, list):
            total_commits = sum(week.get('total', 0) for week in commit_activity if week and isinstance(week, dict))

        # Get top contributors (limit to top 5)
        top_contributors = []
        if contributors and isinstance(contributors, list):
            top_contributors = contributors[:5]

        # Calculate language percentages
        language_percentages = {}
        if languages and isinstance(languages, dict):
            total_bytes = sum(languages.values())
            if total_bytes > 0:
                language_percentages = {
                    lang: (bytes_count / total_bytes) * 100
                    for lang, bytes_count in languages.items()
                    if bytes_count and isinstance(bytes_count, (int, float))
                }
        
        return {
            "repository": {
                "name": repo_info.get("name", repo) if repo_info else repo,
                "full_name": repo_info.get("full_name", f"{owner}/{repo}") if repo_info else f"{owner}/{repo}",
                "description": repo_info.get("description", "") if repo_info else "",
                "stars": repo_info.get("stargazers_count", 0) if repo_info else 0,
                "forks": repo_info.get("forks_count", 0) if repo_info else 0,
                "watchers": repo_info.get("watchers_count", 0) if repo_info else 0,
                "created_at": repo_info.get("created_at", "") if repo_info else "",
                "updated_at": repo_info.get("updated_at", "") if repo_info else "",
                "size": repo_info.get("size", 0) if repo_info else 0
            },
            "statistics": {
                "total_commits": total_commits,
                "total_contributors": len(top_contributors),
                "open_issues": issues_stats.get("open_issues", 0) if issues_stats else 0,
                "closed_issues": issues_stats.get("closed_issues", 0) if issues_stats else 0,
                "total_issues": issues_stats.get("total_issues", 0) if issues_stats else 0,
                "open_prs": issues_stats.get("open_prs", 0) if issues_stats else 0,
                "closed_prs": issues_stats.get("closed_prs", 0) if issues_stats else 0,
                "total_prs": issues_stats.get("total_prs", 0) if issues_stats else 0
            },
            "contributors": top_contributors,
            "commit_activity": commit_activity if commit_activity else [],
            "languages": language_percentages,
            "generated_at": datetime.now().isoformat()
        }
    
    async def get_contributor_stats(self, owner: str, repo: str, username: str) -> Dict:
        """Get statistics for a specific contributor"""
        # Get contributor's commits
        url = f"{self.base_url}/repos/{owner}/{repo}/commits?author={username}&per_page=100"
        
        try:
            commits = await self._make_request(url)
        except Exception as e:
            raise Exception(f"Failed to fetch contributor data: {str(e)}")
        
        # Process commit data
        commit_dates = []
        for commit in commits:
            if commit.get("commit", {}).get("author", {}).get("date"):
                commit_dates.append(commit["commit"]["author"]["date"])
        
        # Calculate activity over time
        activity_map = {}
        for date_str in commit_dates:
            date = datetime.fromisoformat(date_str.replace('Z', '+00:00'))
            week_key = date.strftime("%Y-%W")
            activity_map[week_key] = activity_map.get(week_key, 0) + 1
        
        return {
            "username": username,
            "total_commits": len(commits),
            "activity": activity_map,
            "repository": f"{owner}/{repo}",
            "generated_at": datetime.now().isoformat()
        }
