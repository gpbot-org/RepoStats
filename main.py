from fastapi import FastAPI, HTTPException, Response
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import os
from dotenv import load_dotenv

from src.github_api import GitHubAPI
from src.svg_generator import SVGGenerator
from src.cache_manager import CacheManager

# Load environment variables
load_dotenv()

app = FastAPI(
    title="GitHub Stats SVG API",
    description="Generate dynamic SVG charts for GitHub repository statistics",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize components
github_api = GitHubAPI(token=os.getenv("GITHUB_TOKEN"))
svg_generator = SVGGenerator()
cache_manager = CacheManager()

@app.get("/")
async def root():
    return {
        "message": "GitHub Stats SVG API",
        "version": "1.0.0",
        "endpoints": {
            "/api/embed/{owner}/{repo}.svg": "Generate repository stats SVG",
            "/api/contributor/{owner}/{repo}/{username}.svg": "Generate contributor stats SVG",
            "/api/activity/{owner}/{repo}.svg": "Generate commit activity chart SVG",
            "/api/repobeats/{owner}/{repo}.svg": "Generate RepoBeats-style comprehensive dashboard SVG",
            "/api/modern/{owner}/{repo}.svg": "Generate modern dark dashboard SVG"
        }
    }

@app.get("/api/embed/{owner}/{repo}.svg")
async def get_repo_stats_svg(owner: str, repo: str, theme: str = "default"):
    """Generate SVG with repository statistics"""
    try:
        # Check cache first
        cache_key = f"repo_stats:{owner}:{repo}:{theme}"
        cached_svg = await cache_manager.get(cache_key)
        if cached_svg:
            return Response(content=cached_svg, media_type="image/svg+xml")
        
        # Fetch repository data
        repo_data = await github_api.get_repository_stats(owner, repo)
        
        # Generate SVG
        svg_content = svg_generator.generate_repo_stats_svg(repo_data, theme)
        
        # Cache the result
        await cache_manager.set(cache_key, svg_content, expire=3600)  # 1 hour cache
        
        return Response(content=svg_content, media_type="image/svg+xml")
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/contributor/{owner}/{repo}/{username}.svg")
async def get_contributor_stats_svg(owner: str, repo: str, username: str, theme: str = "default"):
    """Generate SVG with contributor statistics"""
    try:
        # Check cache first
        cache_key = f"contributor_stats:{owner}:{repo}:{username}:{theme}"
        cached_svg = await cache_manager.get(cache_key)
        if cached_svg:
            return Response(content=cached_svg, media_type="image/svg+xml")
        
        # Fetch contributor data
        contributor_data = await github_api.get_contributor_stats(owner, repo, username)
        
        # Generate SVG
        svg_content = svg_generator.generate_contributor_stats_svg(contributor_data, theme)
        
        # Cache the result
        await cache_manager.set(cache_key, svg_content, expire=3600)  # 1 hour cache
        
        return Response(content=svg_content, media_type="image/svg+xml")
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/activity/{owner}/{repo}.svg")
async def get_commit_activity_svg(owner: str, repo: str, theme: str = "default"):
    """Generate SVG with commit activity chart"""
    try:
        # Check cache first
        cache_key = f"commit_activity:{owner}:{repo}:{theme}"
        cached_svg = await cache_manager.get(cache_key)
        if cached_svg:
            return Response(content=cached_svg, media_type="image/svg+xml")

        # Fetch repository data
        repo_data = await github_api.get_repository_stats(owner, repo)

        # Generate SVG
        svg_content = svg_generator.generate_commit_activity_svg(repo_data, theme)

        # Cache the result
        await cache_manager.set(cache_key, svg_content, expire=3600)  # 1 hour cache

        return Response(content=svg_content, media_type="image/svg+xml")

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/repobeats/{owner}/{repo}.svg")
async def get_repobeats_style_svg(owner: str, repo: str, theme: str = "default"):
    """Generate RepoBeats-style comprehensive dashboard SVG"""
    try:
        # Check cache first
        cache_key = f"repobeats_style:{owner}:{repo}:{theme}"
        cached_svg = await cache_manager.get(cache_key)
        if cached_svg:
            return Response(content=cached_svg, media_type="image/svg+xml")

        # Fetch repository data
        repo_data = await github_api.get_repository_stats(owner, repo)

        # Generate SVG
        svg_content = svg_generator.generate_repobeats_style_svg(repo_data, theme)

        # Cache the result
        await cache_manager.set(cache_key, svg_content, expire=3600)  # 1 hour cache

        return Response(content=svg_content, media_type="image/svg+xml")

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/modern/{owner}/{repo}.svg")
async def get_modern_dark_dashboard(owner: str, repo: str, theme: str = "dark"):
    """Generate modern dark dashboard SVG"""
    try:
        # Check cache first
        cache_key = f"modern_dashboard:{owner}:{repo}:{theme}"
        cached_svg = await cache_manager.get(cache_key)
        if cached_svg:
            return Response(content=cached_svg, media_type="image/svg+xml")

        # Fetch repository data
        repo_data = await github_api.get_repository_stats(owner, repo)

        # Generate SVG
        svg_content = svg_generator.generate_modern_dark_dashboard(repo_data, theme)

        # Cache the result
        await cache_manager.set(cache_key, svg_content, expire=3600)  # 1 hour cache

        return Response(content=svg_content, media_type="image/svg+xml")

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
