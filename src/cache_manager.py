import asyncio
import json
import os
from typing import Optional
import hashlib

try:
    import redis.asyncio as redis
    REDIS_AVAILABLE = True
except ImportError:
    REDIS_AVAILABLE = False

class CacheManager:
    def __init__(self):
        self.redis_client = None
        self.memory_cache = {}
        self.cache_ttl = {}
        
        # Try to connect to Redis if available
        if REDIS_AVAILABLE:
            redis_url = os.getenv("REDIS_URL", "redis://localhost:6379/0")
            try:
                self.redis_client = redis.from_url(redis_url)
            except Exception:
                print("Warning: Could not connect to Redis, using in-memory cache")
                self.redis_client = None
    
    async def get(self, key: str) -> Optional[str]:
        """Get value from cache"""
        # Try Redis first
        if self.redis_client:
            try:
                value = await self.redis_client.get(key)
                return value.decode('utf-8') if value else None
            except Exception:
                pass
        
        # Fallback to memory cache
        if key in self.memory_cache:
            # Check if expired
            import time
            if key in self.cache_ttl and time.time() > self.cache_ttl[key]:
                del self.memory_cache[key]
                del self.cache_ttl[key]
                return None
            return self.memory_cache[key]
        
        return None
    
    async def set(self, key: str, value: str, expire: int = 3600) -> bool:
        """Set value in cache with expiration"""
        # Try Redis first
        if self.redis_client:
            try:
                await self.redis_client.setex(key, expire, value)
                return True
            except Exception:
                pass
        
        # Fallback to memory cache
        import time
        self.memory_cache[key] = value
        self.cache_ttl[key] = time.time() + expire
        
        # Clean up expired entries periodically
        await self._cleanup_memory_cache()
        
        return True
    
    async def delete(self, key: str) -> bool:
        """Delete value from cache"""
        # Try Redis first
        if self.redis_client:
            try:
                await self.redis_client.delete(key)
            except Exception:
                pass
        
        # Remove from memory cache
        if key in self.memory_cache:
            del self.memory_cache[key]
        if key in self.cache_ttl:
            del self.cache_ttl[key]
        
        return True
    
    async def _cleanup_memory_cache(self):
        """Clean up expired entries from memory cache"""
        import time
        current_time = time.time()
        expired_keys = [
            key for key, expiry in self.cache_ttl.items()
            if current_time > expiry
        ]
        
        for key in expired_keys:
            if key in self.memory_cache:
                del self.memory_cache[key]
            del self.cache_ttl[key]
    
    def generate_cache_key(self, *args) -> str:
        """Generate a cache key from arguments"""
        key_string = ":".join(str(arg) for arg in args)
        return hashlib.md5(key_string.encode()).hexdigest()
    
    async def close(self):
        """Close cache connections"""
        if self.redis_client:
            await self.redis_client.close()
