#!/usr/bin/env python3
"""
LinkedIn Post Creator - End-to-End Test Script

This script tests the complete application workflow:
1. CrewAI crew instantiation and configuration
2. Agent and task setup
3. Sequential workflow execution
4. API endpoint functionality
5. Post quality validation
"""

import os
import sys
import asyncio
import json
import time
from datetime import datetime
from dotenv import load_dotenv

# Add src to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

def test_environment_setup():
    """Test 1: Verify environment variables and dependencies"""
    print("🔧 Testing Environment Setup...")
    
    # Load environment variables
    load_dotenv()
    
    # Check required environment variables
    required_vars = ['GEMINI_API_KEY']
    missing_vars = []
    
    for var in required_vars:
        if not os.getenv(var):
            missing_vars.append(var)
    
    if missing_vars:
        print(f"❌ Missing environment variables: {missing_vars}")
        print("Please set up your .env file based on .env.example")
        return False
    
    # Test imports
    try:
        from linkedin_post_creator.crew import LinkedinPostCreator
        from crewai_tools import SerperDevTool
        print("✅ All dependencies imported successfully")
        return True
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False

def test_crew_instantiation():
    """Test 2: Test CrewAI crew instantiation and configuration"""
    print("\n🤖 Testing CrewAI Crew Instantiation...")
    
    try:
        from linkedin_post_creator.crew import LinkedinPostCreator
        
        # Create crew instance
        crew_instance = LinkedinPostCreator()
        print("✅ LinkedinPostCreator crew instantiated successfully")
        
        # Test agent creation
        career_coach = crew_instance.career_coach()
        linkedin_writer = crew_instance.linkedin_writer()
        content_critic = crew_instance.content_critic()
        
        print("✅ All agents created successfully:")
        print(f"   - Career Coach: {career_coach.role}")
        print(f"   - LinkedIn Writer: {linkedin_writer.role}")
        print(f"   - Content Critic: {content_critic.role}")
        
        # Test task creation
        research_task = crew_instance.research_task()
        content_task = crew_instance.content_creation_task()
        review_task = crew_instance.content_review_task()
        
        print("✅ All tasks created successfully:")
        print(f"   - Research Task: {research_task.description[:50]}...")
        print(f"   - Content Task: {content_task.description[:50]}...")
        print(f"   - Review Task: {review_task.description[:50]}...")
        
        # Test crew assembly
        crew = crew_instance.crew()
        print(f"✅ Crew assembled with {len(crew.agents)} agents and {len(crew.tasks)} tasks")
        
        return True, crew_instance
        
    except Exception as e:
        print(f"❌ Crew instantiation failed: {e}")
        return False, None

def test_crew_execution(crew_instance):
    """Test 3: Test sequential task execution"""
    print("\n⚡ Testing Crew Execution...")
    
    try:
        # Test inputs
        test_inputs = {
            'topic': 'AI and Machine Learning',
            'industry': 'Technology',
            'tone': 'professional',
            'audience': 'software engineers and data scientists',
            'current_year': str(datetime.now().year)
        }
        
        print(f"📝 Test inputs: {test_inputs}")
        print("🔄 Starting crew execution (this may take 30-60 seconds)...")
        
        start_time = time.time()
        result = crew_instance.crew().kickoff(inputs=test_inputs)
        execution_time = time.time() - start_time
        
        print(f"✅ Crew execution completed in {execution_time:.2f} seconds")
        print(f"📄 Generated post length: {len(str(result))} characters")
        
        return True, str(result)
        
    except Exception as e:
        print(f"❌ Crew execution failed: {e}")
        return False, None

def validate_post_quality(post_content):
    """Test 4: Validate generated post quality"""
    print("\n📊 Validating Post Quality...")
    
    if not post_content:
        print("❌ No post content to validate")
        return False
    
    # Word count validation
    words = post_content.split()
    word_count = len(words)
    print(f"📝 Word count: {word_count}")
    
    if word_count > 200:
        print("⚠️  Warning: Post exceeds 200 words")
    else:
        print("✅ Word count within limit")
    
    # Check for emojis
    emoji_count = sum(1 for char in post_content if ord(char) > 127)
    print(f"😊 Emoji characters detected: {emoji_count}")
    
    # Check for hashtags
    hashtag_count = post_content.count('#')
    print(f"#️⃣ Hashtags detected: {hashtag_count}")
    
    if hashtag_count >= 3:
        print("✅ Adequate hashtags included")
    else:
        print("⚠️  Warning: Few hashtags detected")
    
    # Check for engagement elements
    has_question = '?' in post_content
    has_call_to_action = any(phrase in post_content.lower() for phrase in 
                           ['what do you think', 'share your', 'let me know', 'comment', 'thoughts'])
    
    print(f"❓ Contains question: {has_question}")
    print(f"📢 Contains call-to-action: {has_call_to_action}")
    
    print("\n📄 Generated Post Preview:")
    print("-" * 50)
    print(post_content[:300] + "..." if len(post_content) > 300 else post_content)
    print("-" * 50)
    
    return True

async def test_api_endpoints():
    """Test 5: Test API endpoints"""
    print("\n🌐 Testing API Endpoints...")
    
    try:
        import aiohttp
        
        # Test health endpoint
        async with aiohttp.ClientSession() as session:
            try:
                async with session.get('http://localhost:8080/api/health') as response:
                    if response.status == 200:
                        health_data = await response.json()
                        print("✅ Health endpoint working")
                        print(f"   Status: {health_data.get('status')}")
                    else:
                        print(f"⚠️  Health endpoint returned status: {response.status}")
            except aiohttp.ClientConnectorError:
                print("⚠️  API server not running - skipping API tests")
                print("   To test APIs, run: python api/app.py")
                return False
        
        return True
        
    except ImportError:
        print("⚠️  aiohttp not installed - skipping API tests")
        print("   Install with: pip install aiohttp")
        return False

def test_search_tools():
    """Test 6: Test search tool functionality"""
    print("\n🔍 Testing Search Tools...")
    
    try:
        from crewai_tools import SerperDevTool
        
        # Test Serper tool (if API key available)
        if os.getenv('SERPER_API_KEY'):
            serper_tool = SerperDevTool()
            print("✅ Serper search tool initialized")
        else:
            print("⚠️  SERPER_API_KEY not found - Serper tool will not be available")
        
        return True
        
    except Exception as e:
        print(f"❌ Search tools test failed: {e}")
        return False

def main():
    """Run all tests"""
    print("🚀 LinkedIn Post Creator - End-to-End Test Suite")
    print("=" * 60)
    
    test_results = []
    
    # Test 1: Environment Setup
    env_ok = test_environment_setup()
    test_results.append(("Environment Setup", env_ok))
    
    if not env_ok:
        print("\n❌ Environment setup failed. Please fix issues before continuing.")
        return
    
    # Test 2: Crew Instantiation
    crew_ok, crew_instance = test_crew_instantiation()
    test_results.append(("Crew Instantiation", crew_ok))
    
    if not crew_ok:
        print("\n❌ Crew instantiation failed. Cannot continue with execution tests.")
        return
    
    # Test 3: Search Tools
    search_ok = test_search_tools()
    test_results.append(("Search Tools", search_ok))
    
    # Test 4: Crew Execution
    exec_ok, post_content = test_crew_execution(crew_instance)
    test_results.append(("Crew Execution", exec_ok))
    
    if exec_ok and post_content:
        # Test 5: Post Quality Validation
        quality_ok = validate_post_quality(post_content)
        test_results.append(("Post Quality", quality_ok))
    
    # Test 6: API Endpoints (async)
    try:
        api_ok = asyncio.run(test_api_endpoints())
        test_results.append(("API Endpoints", api_ok))
    except Exception as e:
        print(f"⚠️  API test failed: {e}")
        test_results.append(("API Endpoints", False))
    
    # Summary
    print("\n" + "=" * 60)
    print("📋 TEST SUMMARY")
    print("=" * 60)
    
    passed = 0
    total = len(test_results)
    
    for test_name, result in test_results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{test_name:<20} {status}")
        if result:
            passed += 1
    
    print(f"\nResults: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Your LinkedIn Post Creator is ready to use.")
    else:
        print("⚠️  Some tests failed. Please review the issues above.")
    
    print("\n📚 Next Steps:")
    print("1. Start the API server: python api/app.py")
    print("2. Start the frontend: cd frontend && npm start")
    print("3. Open http://localhost:3000 in your browser")

if __name__ == "__main__":
    main() 