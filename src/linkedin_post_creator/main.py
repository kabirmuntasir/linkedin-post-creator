#!/usr/bin/env python
import sys
import warnings
import os

from datetime import datetime
from dotenv import load_dotenv

from linkedin_post_creator.crew import LinkedinPostCreator

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

# Load environment variables
load_dotenv()

# This main file is intended to be a way for you to run your
# crew locally, so refrain from adding unnecessary logic into this file.
# Replace with inputs you want to test with, it will automatically
# interpolate any tasks and agents information

def run():
    """
    Run the crew with default parameters for testing.
    """
    inputs = {
        'topic': 'AI and Machine Learning',
        'industry': 'Technology',
        'tone': 'professional',
        'audience': 'software engineers and data scientists',
        'current_year': str(datetime.now().year)
    }
    
    try:
        result = LinkedinPostCreator().crew().kickoff(inputs=inputs)
        print("\n" + "="*50)
        print("LINKEDIN POST GENERATED SUCCESSFULLY!")
        print("="*50)
        print(result)
        return result
    except Exception as e:
        print(f"An error occurred while running the crew: {e}")
        raise Exception(f"An error occurred while running the crew: {e}")


def run_with_params(topic, industry="Technology", tone="professional", audience="professionals"):
    """
    Run the crew with custom parameters.
    """
    inputs = {
        'topic': topic,
        'industry': industry,
        'tone': tone,
        'audience': audience,
        'current_year': str(datetime.now().year)
    }
    
    try:
        result = LinkedinPostCreator().crew().kickoff(inputs=inputs)
        return result
    except Exception as e:
        raise Exception(f"An error occurred while running the crew: {e}")


def train():
    """
    Train the crew for a given number of iterations.
    """
    inputs = {
        "topic": "AI and Machine Learning",
        "industry": "Technology",
        "tone": "professional",
        "audience": "software engineers and data scientists",
        'current_year': str(datetime.now().year)
    }
    try:
        LinkedinPostCreator().crew().train(n_iterations=int(sys.argv[1]), filename=sys.argv[2], inputs=inputs)

    except Exception as e:
        raise Exception(f"An error occurred while training the crew: {e}")

def replay():
    """
    Replay the crew execution from a specific task.
    """
    try:
        LinkedinPostCreator().crew().replay(task_id=sys.argv[1])

    except Exception as e:
        raise Exception(f"An error occurred while replaying the crew: {e}")

def test():
    """
    Test the crew execution and returns the results.
    """
    inputs = {
        "topic": "AI and Machine Learning",
        "industry": "Technology", 
        "tone": "professional",
        "audience": "software engineers and data scientists",
        "current_year": str(datetime.now().year)
    }
    
    try:
        result = LinkedinPostCreator().crew().test(n_iterations=int(sys.argv[1]), eval_llm=sys.argv[2], inputs=inputs)
        return result
    except Exception as e:
        raise Exception(f"An error occurred while testing the crew: {e}")


if __name__ == "__main__":
    # Check if environment variables are set
    if not os.getenv('GEMINI_API_KEY'):
        print("Warning: GEMINI_API_KEY not found in environment variables")
        print("Please set up your .env file based on .env.example")
    
    # Run the crew
    run()
