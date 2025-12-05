#!/usr/bin/env python3
"""
Test Setup Script - Verify Discord Bot Installation
Cek semua requirements sebelum menjalankan bot
"""

import sys
import os
from pathlib import Path

def print_header(text):
    """Print formatted header"""
    print("\n" + "=" * 50)
    print(f"  {text}")
    print("=" * 50)

def print_check(status, message):
    """Print check result"""
    symbol = "✅" if status else "❌"
    print(f"{symbol} {message}")

def check_python_version():
    """Check Python version"""
    print_header("Checking Python Version")
    version = sys.version_info
    required = (3, 8)
    
    current = f"{version.major}.{version.minor}.{version.micro}"
    is_ok = version >= required
    
    print_check(is_ok, f"Python {current}")
    
    if not is_ok:
        print(f"   Required: Python {required[0]}.{required[1]}+")
        return False
    return True

def check_dependencies():
    """Check if all dependencies are installed"""
    print_header("Checking Dependencies")
    
    dependencies = [
        ("discord", "discord.py"),
        ("openai", "openai"),
        ("dotenv", "python-dotenv"),
        ("requests", "requests"),
        ("aiohttp", "aiohttp"),
    ]
    
    all_ok = True
    for module, package in dependencies:
        try:
            __import__(module)
            print_check(True, f"{package} installed")
        except ImportError:
            print_check(False, f"{package} NOT installed")
            print(f"   Install with: pip install {package}")
            all_ok = False
    
    return all_ok

def check_files():
    """Check if required files exist"""
    print_header("Checking Files")
    
    files = {
        "bot.py": "Main bot file",
        ".env": "Environment variables",
        "requirements.txt": "Dependencies list",
    }
    
    all_ok = True
    for file, description in files.items():
        exists = Path(file).exists()
        print_check(exists, f"{file} - {description}")
        if not exists:
            all_ok = False
    
    return all_ok

def check_directories():
    """Check if required directories exist"""
    print_header("Checking Directories")
    
    dirs = ["data", "data/logs", "data/cache"]
    
    all_ok = True
    for directory in dirs:
        path = Path(directory)
        if not path.exists():
            print_check(False, f"{directory}/ NOT found - Creating...")
            try:
                path.mkdir(parents=True, exist_ok=True)
                print_check(True, f"{directory}/ created")
            except Exception as e:
                print_check(False, f"Failed to create {directory}/: {e}")
                all_ok = False
        else:
            print_check(True, f"{directory}/ exists")
    
    return all_ok

def check_env_variables():
    """Check environment variables"""
    print_header("Checking Environment Variables")
    
    if not Path(".env").exists():
        print_check(False, ".env file not found")
        return False
    
    try:
        from dotenv import load_dotenv
        load_dotenv()
        
        required_vars = ["DISCORD_TOKEN", "GROQ_API_KEY"]
        all_ok = True
        
        for var in required_vars:
            value = os.getenv(var)
            if value and value != f"your_{var.lower()}_here":
                print_check(True, f"{var} is set")
            else:
                print_check(False, f"{var} NOT set or using placeholder")
                all_ok = False
        
        return all_ok
    except Exception as e:
        print_check(False, f"Error reading .env: {e}")
        return False

def check_discord_intents():
    """Check if discord.py is properly configured"""
    print_header("Checking Discord.py Configuration")
    
    try:
        import discord
        
        # Test if Intents work
        intents = discord.Intents.default()
        intents.message_content = True
        
        print_check(True, "Discord.py properly configured")
        print("   ⚠️  Remember to enable MESSAGE CONTENT INTENT in Discord Developer Portal!")
        return True
    except Exception as e:
        print_check(False, f"Discord.py configuration error: {e}")
        return False

def test_groq_connection():
    """Test Groq API connection"""
    print_header("Testing Groq API Connection")
    
    try:
        from openai import OpenAI
        from dotenv import load_dotenv
        load_dotenv()
        
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key or api_key == "your_groq_api_key_here":
            print_check(False, "GROQ_API_KEY not set")
            return False
        
        # Test connection
        client = OpenAI(
            api_key=api_key,
            base_url="https://api.groq.com/openai/v1"
        )
        
        # Simple test request
        response = client.chat.completions.create(
            model="groq/compound",
            messages=[{"role": "user", "content": "test"}],
            max_tokens=10
        )
        
        print_check(True, "Groq API connection successful")
        print(f"   Model: {response.model}")
        return True
        
    except Exception as e:
        print_check(False, f"Groq API connection failed: {e}")
        print("   Check your GROQ_API_KEY in .env file")
        return False

def main():
    """Run all checks"""
    print("\n" + "=" * 50)
    print("  🤖 Discord AI Bot - Setup Verification")
    print("=" * 50)
    
    results = {
        "Python Version": check_python_version(),
        "Dependencies": check_dependencies(),
        "Files": check_files(),
        "Directories": check_directories(),
        "Environment Variables": check_env_variables(),
        "Discord.py Config": check_discord_intents(),
        "Groq API": test_groq_connection(),
    }
    
    # Summary
    print_header("Summary")
    
    passed = sum(results.values())
    total = len(results)
    
    for check, status in results.items():
        print_check(status, check)
    
    print("\n" + "=" * 50)
    print(f"  Results: {passed}/{total} checks passed")
    print("=" * 50 + "\n")
    
    if passed == total:
        print("✅ All checks passed! Your bot is ready to run.")
        print("   Start bot with: python bot.py")
        print("   Or use: ./run_bot.sh (Linux/Mac) or run_bot.bat (Windows)")
        return True
    else:
        print("❌ Some checks failed. Please fix the issues above.")
        print("\n📚 Need help?")
        print("   - Read SETUP.md for detailed instructions")
        print("   - Check QUICK_START.md for quick commands")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)