from flask import Blueprint, jsonify

# This will be expanded significantly
# For now, just a placeholder

course_bp = Blueprint('course_bp', __name__)

sample_course_structure = {
    "title": "AI Agent Development Course",
    "chapters": [
        {"id": "chapter1", "title": "Introduction to AI Agents", "order": 1, "sections": []},
        {"id": "chapter2", "title": "Building Your First Agent", "order": 2, "sections": []},
        # ... more chapters
    ]
}

sample_chapter_content = {
    "chapterId": "chapter1",
    "title": "Introduction to AI Agents",
    "sections": [
        {
            "sectionTitle": "What is an AI Agent?",
            "contentBlocks": [
                {"type": "text", "value": "An AI agent is a system that perceives its environment and takes actions to achieve its goals."},
                {"type": "text", "value": "This course will guide you through building practical AI agents."},
            ]
        },
        {
            "sectionTitle": "Key Concepts",
            "contentBlocks": [
                {"type": "text", "value": "We will cover topics like perception, action, goals, and learning."},
                {"type": "code", "language": "python", "value": "print('Hello, AI Agent World!')"}
            ]
        }
    ]
}

@course_bp.route('/structure', methods=['GET'])
def get_course_structure():
    # In the future, this will be dynamically generated from parsed content
    return jsonify(sample_course_structure)

@course_bp.route('/chapter/<string:chapter_id>', methods=['GET'])
def get_chapter_content(chapter_id: str):
    # In the future, this will fetch specific chapter content
    # For now, return sample if id matches, else 404
    if chapter_id == sample_chapter_content["chapterId"]:
        return jsonify(sample_chapter_content)
    return jsonify({"error": "Chapter not found"}), 404

# Later, add routes for:
# - User progress
# - Bookmarks
# - Quiz submissions, etc.
