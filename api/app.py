from quart import Quart, request, jsonify
from quart_cors import cors
import asyncio
import uuid
import os
from datetime import datetime
from dotenv import load_dotenv
import sys
import traceback

# Add the src directory to the path so we can import our crew
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from linkedin_post_creator.crew import LinkedinPostCreator

# Load environment variables
load_dotenv()

app = Quart(__name__)
app = cors(app, allow_origin="*")

# In-memory storage for job status (in production, use Redis or a database)
job_storage = {}

@app.route('/api/health', methods=['GET'])
async def health_check():
    """Health check endpoint for container monitoring"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'service': 'linkedin-post-creator'
    })

@app.route('/api/generate-post', methods=['POST'])
async def generate_post():
    """Generate a LinkedIn post using the AI crew"""
    try:
        data = await request.get_json()
        
        # Validate required fields
        if not data or 'topic' not in data:
            return jsonify({'error': 'Topic is required'}), 400
        
        # Extract parameters with defaults
        topic = data['topic']
        industry = data.get('industry', 'Technology')
        tone = data.get('tone', 'professional')
        audience = data.get('audience', 'professionals')
        
        # Generate unique job ID
        job_id = str(uuid.uuid4())
        
        # Initialize job status
        job_storage[job_id] = {
            'status': 'started',
            'progress': 'Initializing AI agents...',
            'result': None,
            'error': None,
            'timestamp': datetime.now().isoformat()
        }
        
        # Start the crew execution in the background
        asyncio.create_task(run_crew_async(job_id, topic, industry, tone, audience))
        
        return jsonify({
            'job_id': job_id,
            'status': 'started',
            'message': 'LinkedIn post generation started'
        }), 202
        
    except Exception as e:
        return jsonify({
            'error': 'Failed to start post generation',
            'details': str(e)
        }), 500

@app.route('/api/status/<job_id>', methods=['GET'])
async def get_job_status(job_id):
    """Check the status of a post generation job"""
    if job_id not in job_storage:
        return jsonify({'error': 'Job not found'}), 404
    
    return jsonify(job_storage[job_id])

async def run_crew_async(job_id, topic, industry, tone, audience):
    """Run the CrewAI crew asynchronously"""
    try:
        # Update status
        job_storage[job_id]['status'] = 'running'
        job_storage[job_id]['progress'] = 'Research agent searching for trending topics...'
        
        # Prepare inputs for the crew
        inputs = {
            'topic': topic,
            'industry': industry,
            'tone': tone,
            'audience': audience,
            'current_year': str(datetime.now().year)
        }
        
        # Create and run the crew
        job_storage[job_id]['progress'] = 'Creating LinkedIn post...'
        
        # Run the crew in a thread pool to avoid blocking
        loop = asyncio.get_event_loop()
        result = await loop.run_in_executor(
            None, 
            lambda: LinkedinPostCreator().crew().kickoff(inputs=inputs)
        )
        
        # Update job with success
        job_storage[job_id]['status'] = 'completed'
        job_storage[job_id]['progress'] = 'LinkedIn post generated successfully!'
        job_storage[job_id]['result'] = {
            'post': str(result),
            'topic': topic,
            'industry': industry,
            'tone': tone,
            'audience': audience,
            'word_count': len(str(result).split()),
            'generated_at': datetime.now().isoformat()
        }
        
    except Exception as e:
        # Update job with error
        job_storage[job_id]['status'] = 'failed'
        job_storage[job_id]['error'] = str(e)
        job_storage[job_id]['progress'] = f'Failed: {str(e)}'
        print(f"Error in crew execution: {e}")
        traceback.print_exc()

@app.route('/api/generate-post-sync', methods=['POST'])
async def generate_post_sync():
    """Generate a LinkedIn post synchronously (for testing)"""
    try:
        data = await request.get_json()
        
        # Validate required fields
        if not data or 'topic' not in data:
            return jsonify({'error': 'Topic is required'}), 400
        
        # Extract parameters with defaults
        topic = data['topic']
        industry = data.get('industry', 'Technology')
        tone = data.get('tone', 'professional')
        audience = data.get('audience', 'professionals')
        
        # Prepare inputs for the crew
        inputs = {
            'topic': topic,
            'industry': industry,
            'tone': tone,
            'audience': audience,
            'current_year': str(datetime.now().year)
        }
        
        # Run the crew synchronously (for small requests)
        result = LinkedinPostCreator().crew().kickoff(inputs=inputs)
        
        return jsonify({
            'status': 'completed',
            'result': {
                'post': str(result),
                'topic': topic,
                'industry': industry,
                'tone': tone,
                'audience': audience,
                'word_count': len(str(result).split()),
                'generated_at': datetime.now().isoformat()
            }
        })
        
    except Exception as e:
        return jsonify({
            'error': 'Failed to generate post',
            'details': str(e)
        }), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port, debug=True) 