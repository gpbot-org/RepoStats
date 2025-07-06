#!/usr/bin/env python3
"""
Test script for the Text Animation API
"""

import asyncio
import aiohttp
import urllib.parse

async def test_text_animation_api():
    """Test the text animation API with various parameters"""
    base_url = "http://localhost:8000"
    
    test_cases = [
        # Basic tests
        {"text": "test", "description": "Basic test case"},
        {"text": "Hello World", "description": "Default example"},
        
        # Theme tests
        {"text": "Matrix", "theme": "matrix", "description": "Matrix theme"},
        {"text": "Dark Mode", "theme": "dark", "description": "Dark theme"},
        {"text": "Light Mode", "theme": "light", "description": "Light theme"},
        {"text": "Neon Glow", "theme": "neon", "description": "Neon theme"},
        
        # Custom styling
        {"text": "Big Text", "font_size": 48, "description": "Large font size"},
        {"text": "Small", "font_size": 12, "description": "Small font size"},
        {"text": "Red Text", "color": "#ff0000", "description": "Custom color"},
        {"text": "Blue BG", "bg_color": "#0000ff", "description": "Custom background"},
        
        # Speed tests
        {"text": "Fast!", "speed": 0.2, "description": "Fast animation"},
        {"text": "Slow...", "speed": 1.0, "description": "Slow animation"},
        
        # Complex combinations
        {
            "text": "Custom Style",
            "font_size": 32,
            "color": "#ff6b6b",
            "bg_color": "#282c34",
            "speed": 0.3,
            "description": "Complex custom styling"
        },
        
        # Special characters
        {"text": "Hello! @#$%", "description": "Special characters"},
        {"text": "123 Numbers", "description": "Numbers and text"},
        
        # Long text
        {"text": "This is a longer text to test wrapping", "description": "Long text"},
        
        # Edge cases
        {"text": "A", "description": "Single character"},
        {"text": "", "description": "Empty text (should use default)"},
    ]
    
    print("🎬 Testing Text Animation API")
    print("=" * 50)
    
    async with aiohttp.ClientSession() as session:
        for i, test_case in enumerate(test_cases, 1):
            print(f"\n📝 Test {i}: {test_case['description']}")
            
            # Build URL with parameters
            params = {}
            for key, value in test_case.items():
                if key != "description":
                    params[key] = str(value)
            
            # URL encode parameters
            query_string = urllib.parse.urlencode(params)
            url = f"{base_url}/api/text?{query_string}"
            
            print(f"   URL: {url}")
            
            try:
                async with session.get(url) as response:
                    if response.status == 200:
                        content = await response.text()
                        
                        # Basic validation
                        checks = [
                            ("Valid SVG start", content.startswith('<svg')),
                            ("Valid SVG end", content.endswith('</svg>')),
                            ("Contains animation", 'animate' in content),
                            ("Contains text elements", '<text' in content),
                            ("Has proper xmlns", 'xmlns="http://www.w3.org/2000/svg"' in content),
                        ]
                        
                        all_passed = True
                        for check_name, passed in checks:
                            status = "✅" if passed else "❌"
                            print(f"   {status} {check_name}")
                            if not passed:
                                all_passed = False
                        
                        if all_passed:
                            print(f"   🎉 Test passed! ({len(content)} characters)")
                        else:
                            print(f"   ⚠️  Test has issues")
                            
                        # Extract some info
                        if 'width=' in content:
                            width = content.split('width="')[1].split('"')[0]
                            height = content.split('height="')[1].split('"')[0]
                            print(f"   📐 Dimensions: {width}x{height}")
                            
                    else:
                        print(f"   ❌ HTTP Error: {response.status}")
                        error_text = await response.text()
                        print(f"   Error: {error_text}")
                        
            except Exception as e:
                print(f"   ❌ Exception: {str(e)}")

async def test_animation_behavior():
    """Test specific animation behavior"""
    print("\n\n🎭 Testing Animation Behavior")
    print("=" * 50)
    
    base_url = "http://localhost:8000"
    
    # Test with known text to verify animation timing
    test_text = "test"
    url = f"{base_url}/api/text?text={test_text}&speed=0.5"
    
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                content = await response.text()
                
                # Count text elements (should be one per character + cursor)
                text_count = content.count('<text')
                expected_chars = len(test_text)
                
                print(f"📊 Text: '{test_text}' ({expected_chars} characters)")
                print(f"📊 Text elements found: {text_count}")
                print(f"📊 Expected: {expected_chars} chars + 1 cursor + 1 watermark = {expected_chars + 2}")
                
                if text_count == expected_chars + 2:
                    print("✅ Correct number of text elements")
                else:
                    print("⚠️  Unexpected number of text elements")
                
                # Check for animation attributes
                animation_checks = [
                    ("Has animate elements", '<animate' in content),
                    ("Has opacity animation", 'attributeName="opacity"' in content),
                    ("Has keyTimes", 'keyTimes=' in content),
                    ("Has repeatCount", 'repeatCount="indefinite"' in content),
                    ("Has cursor animation", 'values="1;0;1"' in content),
                ]
                
                for check_name, passed in animation_checks:
                    status = "✅" if passed else "❌"
                    print(f"{status} {check_name}")

if __name__ == "__main__":
    print("🔧 Text Animation API Test Suite")
    print("Testing all endpoints and parameters...")
    print()
    
    try:
        asyncio.run(test_text_animation_api())
        asyncio.run(test_animation_behavior())
        print("\n✅ All tests completed!")
    except KeyboardInterrupt:
        print("\n⏹️  Tests interrupted")
    except Exception as e:
        print(f"\n❌ Test suite error: {e}")
