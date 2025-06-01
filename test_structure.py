#!/usr/bin/env python3
"""
LinkedIn Post Creator - Structure Validation Test

This script tests the application structure without requiring API keys:
1. File structure validation
2. Import validation
3. Configuration validation
4. Basic instantiation tests
"""

import os
import sys
from pathlib import Path

def test_file_structure():
    """Test 1: Validate project file structure"""
    print("📁 Testing File Structure...")
    
    required_files = [
        'src/linkedin_post_creator/config/agents.yaml',
        'src/linkedin_post_creator/config/tasks.yaml',
        'src/linkedin_post_creator/crew.py',
        'src/linkedin_post_creator/main.py',
        'api/app.py',
        'frontend/package.json',
        'requirements.txt',
        '.env.example',
        'Dockerfile',
        'README.md'
    ]
    
    missing_files = []
    for file_path in required_files:
        if not Path(file_path).exists():
            missing_files.append(file_path)
    
    if missing_files:
        print(f"❌ Missing files: {missing_files}")
        return False
    
    print("✅ All required files present")
    return True

def test_python_imports():
    """Test 2: Validate Python imports without API calls"""
    print("\n🐍 Testing Python Imports...")
    
    # Add src to path
    sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))
    
    try:
        # Test core imports
        import crewai
        print("✅ CrewAI imported successfully")
        
        from crewai_tools import SerperDevTool
        print("✅ CrewAI tools imported successfully")
        
        import quart
        print("✅ Quart imported successfully")
        
        from quart_cors import cors
        print("✅ Quart CORS imported successfully")
        
        # Test our modules
        from linkedin_post_creator.crew import LinkedinPostCreator
        print("✅ LinkedinPostCreator imported successfully")
        
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False

def test_configuration_files():
    """Test 3: Validate YAML configuration files"""
    print("\n⚙️ Testing Configuration Files...")
    
    try:
        import yaml
        
        # Test agents.yaml
        with open('src/linkedin_post_creator/config/agents.yaml', 'r') as f:
            agents_config = yaml.safe_load(f)
        
        required_agents = ['career_coach', 'linkedin_writer', 'content_critic']
        for agent in required_agents:
            if agent not in agents_config:
                print(f"❌ Missing agent: {agent}")
                return False
        
        print("✅ All required agents configured")
        
        # Test tasks.yaml
        with open('src/linkedin_post_creator/config/tasks.yaml', 'r') as f:
            tasks_config = yaml.safe_load(f)
        
        required_tasks = ['research_task', 'content_creation_task', 'content_review_task']
        for task in required_tasks:
            if task not in tasks_config:
                print(f"❌ Missing task: {task}")
                return False
        
        print("✅ All required tasks configured")
        return True
        
    except Exception as e:
        print(f"❌ Configuration validation failed: {e}")
        return False

def test_crew_structure():
    """Test 4: Validate crew structure without execution"""
    print("\n🤖 Testing Crew Structure...")
    
    try:
        sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))
        from linkedin_post_creator.crew import LinkedinPostCreator
        
        # Create crew instance (without API keys)
        crew_instance = LinkedinPostCreator()
        print("✅ LinkedinPostCreator instantiated")
        
        # Check if methods exist
        methods = ['career_coach', 'linkedin_writer', 'content_critic', 
                  'research_task', 'content_creation_task', 'content_review_task', 'crew']
        
        for method in methods:
            if not hasattr(crew_instance, method):
                print(f"❌ Missing method: {method}")
                return False
        
        print("✅ All required methods present")
        
        # Check if search tools are initialized
        if hasattr(crew_instance, 'search_tool') and hasattr(crew_instance, 'serper_tool'):
            print("✅ Search tools initialized")
        else:
            print("⚠️  Search tools not properly initialized")
        
        return True
        
    except Exception as e:
        print(f"❌ Crew structure test failed: {e}")
        return False

def test_frontend_structure():
    """Test 5: Validate frontend structure"""
    print("\n⚛️ Testing Frontend Structure...")
    
    try:
        # Check package.json
        import json
        with open('frontend/package.json', 'r') as f:
            package_data = json.load(f)
        
        required_deps = ['react', 'axios', '@mui/material']
        missing_deps = []
        
        dependencies = {**package_data.get('dependencies', {}), **package_data.get('devDependencies', {})}
        
        for dep in required_deps:
            if dep not in dependencies:
                missing_deps.append(dep)
        
        if missing_deps:
            print(f"⚠️  Missing frontend dependencies: {missing_deps}")
        else:
            print("✅ All required frontend dependencies present")
        
        # Check if App.js exists and has basic structure
        if Path('frontend/src/App.js').exists():
            with open('frontend/src/App.js', 'r') as f:
                app_content = f.read()
                if 'LinkedIn Post Creator' in app_content and 'generatePost' in app_content:
                    print("✅ Frontend App.js properly configured")
                else:
                    print("⚠️  Frontend App.js may not be properly configured")
        else:
            print("❌ Frontend App.js not found")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ Frontend structure test failed: {e}")
        return False

def test_api_structure():
    """Test 6: Validate API structure"""
    print("\n🌐 Testing API Structure...")
    
    try:
        # Check if API file exists and has required endpoints
        if not Path('api/app.py').exists():
            print("❌ API app.py not found")
            return False
        
        with open('api/app.py', 'r') as f:
            api_content = f.read()
        
        required_endpoints = ['/api/health', '/api/generate-post', '/api/status']
        missing_endpoints = []
        
        for endpoint in required_endpoints:
            if endpoint not in api_content:
                missing_endpoints.append(endpoint)
        
        if missing_endpoints:
            print(f"❌ Missing API endpoints: {missing_endpoints}")
            return False
        
        print("✅ All required API endpoints present")
        
        # Check for required imports
        required_imports = ['quart', 'LinkedinPostCreator', 'asyncio']
        for imp in required_imports:
            if imp not in api_content:
                print(f"⚠️  Missing import: {imp}")
        
        return True
        
    except Exception as e:
        print(f"❌ API structure test failed: {e}")
        return False

def main():
    """Run all structure validation tests"""
    print("🔍 LinkedIn Post Creator - Structure Validation Test")
    print("=" * 60)
    
    test_results = []
    
    # Run all tests
    tests = [
        ("File Structure", test_file_structure),
        ("Python Imports", test_python_imports),
        ("Configuration Files", test_configuration_files),
        ("Crew Structure", test_crew_structure),
        ("Frontend Structure", test_frontend_structure),
        ("API Structure", test_api_structure)
    ]
    
    for test_name, test_func in tests:
        try:
            result = test_func()
            test_results.append((test_name, result))
        except Exception as e:
            print(f"❌ {test_name} failed with exception: {e}")
            test_results.append((test_name, False))
    
    # Summary
    print("\n" + "=" * 60)
    print("📋 STRUCTURE VALIDATION SUMMARY")
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
        print("🎉 All structure tests passed! Your application is properly set up.")
        print("\n📚 Next Steps:")
        print("1. Add your GEMINI_API_KEY to the .env file")
        print("2. Optionally add SERPER_API_KEY for enhanced search")
        print("3. Run: python test_app.py (with API keys)")
        print("4. Start the API: python api/app.py")
        print("5. Start the frontend: cd frontend && npm start")
    else:
        print("⚠️  Some structure tests failed. Please review the issues above.")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 