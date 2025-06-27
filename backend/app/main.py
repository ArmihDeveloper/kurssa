from flask import Flask, jsonify
from flask_cors import CORS
import os
import json

from app.api.course_routes import course_bp

app = Flask(__name__)
CORS(app) # Allow all origins for now, can be configured more strictly

# Load course data at startup
COURSE_DATA_FILE = os.path.join(os.path.dirname(__file__), 'data', 'course_data.json')
course_data_content = None

try:
    with open(COURSE_DATA_FILE, 'r', encoding='utf-8') as f:
        course_data_content = json.load(f)
    print(f"Successfully loaded course data from {COURSE_DATA_FILE}")
    # Make course_data_content accessible to blueprints, e.g., by attaching to app config
    app.config['COURSE_DATA'] = course_data_content
except FileNotFoundError:
    print(f"[ERROR] Course data file not found: {COURSE_DATA_FILE}. API might not serve course content.")
    app.config['COURSE_DATA'] = {"courseTitle": "Course Data Not Loaded", "chapters": []} # Default empty data
except json.JSONDecodeError as e:
    print(f"[ERROR] Could not decode JSON from {COURSE_DATA_FILE}: {e}")
    app.config['COURSE_DATA'] = {"courseTitle": "Course Data Invalid", "chapters": []} # Default empty data


@app.route('/')
def home():
    return "Backend for AI Agents Course Platform is running!"

@app.route('/api/health')
def health_check():
    return jsonify({"status": "healthy", "message": "API is up and running"})

# Register Blueprints for API routes
app.register_blueprint(course_bp, url_prefix='/api/course')

if __name__ == '__main__':
    # Ensure the 'data' directory exists if it doesn't, to prevent error on first run if file is missing
    data_dir = os.path.join(os.path.dirname(__file__), 'data')
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)
        print(f"Created directory: {data_dir}")
        # Optionally, create an empty course_data.json if it's absolutely critical for app to start
        # with open(COURSE_DATA_FILE, 'w', encoding='utf-8') as f_empty:
        #     json.dump({"courseTitle": "Initial Empty Course", "chapters": []}, f_empty)
        #     print(f"Created empty placeholder: {COURSE_DATA_FILE}")


    port = int(os.environ.get('PORT', 5001)) # Use 5001 to avoid conflict with Next.js default 3000
    app.run(debug=True, port=port)
