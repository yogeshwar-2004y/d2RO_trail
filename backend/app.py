"""
Main Flask application with modular structure using blueprints
"""
from flask import Flask
from flask_cors import CORS

# Import configuration and utilities
from config import Config
from utils.helpers import create_upload_directories
from utils.database_init import initialize_database

# Import all blueprints
from routes.auth import auth_bp
from routes.projects import projects_bp
from routes.users import users_bp
from routes.documents import documents_bp
from routes.tests import tests_bp
from routes.news import news_bp
from routes.files import files_bp

def create_app():
    """Application factory pattern"""
    app = Flask(__name__)
    
    # Load configuration
    app.config.from_object(Config)
    
    # Enable CORS
    CORS(app)
    
    # Create upload directories
    create_upload_directories()
    
    # Initialize database
    initialize_database()
    
    # Register blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(projects_bp)
    app.register_blueprint(users_bp)
    app.register_blueprint(documents_bp)
    app.register_blueprint(tests_bp)
    app.register_blueprint(news_bp)
    app.register_blueprint(files_bp)
    
    return app

# Create the application instance
app = create_app()

# Users API Endpoints

# Get available reviewers
@app.route('/api/users/reviewers', methods=['GET'])
def get_reviewers():
    """Get all users with reviewer role"""
    try:
        cur = conn.cursor()
        
        cur.execute("""
            SELECT u.user_id, u.name, u.email
            FROM users u
            JOIN user_roles ur ON u.user_id = ur.user_id
            JOIN roles r ON ur.role_id = r.role_id
            WHERE r.role_name = 'QA Reviewer'
            ORDER BY u.name
        """)
        
        rows = cur.fetchall()
        cur.close()
        
        reviewers = []
        for row in rows:
            reviewers.append({
                "id": row[0],
                "name": row[1],
                "email": row[2]
            })
        
        return jsonify({
            "success": True,
            "reviewers": reviewers
        })
        
    except Exception as e:
        print(f"Error fetching reviewers: {str(e)}")
        return jsonify({"success": False, "message": "Internal server error"}), 500

# Comments and Annotations API Endpoints

# Get comments for a document
@app.route('/api/comments', methods=['GET'])
def get_comments():
    """Get all comments and annotations for a specific document"""
    try:
        document_id = request.args.get('document_id')
        if not document_id:
            return jsonify({"success": False, "message": "Document ID is required"}), 400
        
        cur = conn.cursor()
        
        # Get comments with annotations
        cur.execute("""
            SELECT 
                c.comment_id,
                c.document_id,
                c.document_name,
                c.version,
                c.reviewer_id,
                c.page_no,
                c.section,
                c.description,
                c.author,
                c.created_at,
                c.is_annotation,
                a.annotation_id,
                a.x_position,
                a.y_position
            FROM document_comments c
            LEFT JOIN document_annotations a ON c.comment_id = a.comment_id
            WHERE c.document_id = %s
            ORDER BY c.created_at DESC
        """, (document_id,))
        
        rows = cur.fetchall()
        cur.close()
        
        # Group comments and annotations
        comments = []
        annotations = []
        
        for row in rows:
            comment = {
                "id": row[0],
                "document_id": row[1],
                "document_name": row[2],
                "version": row[3],
                "reviewer_id": row[4],
                "page_no": row[5],
                "section": row[6],
                "description": row[7],
                "author": row[8],
                "created_at": row[9].isoformat() if row[9] else None,
                "annotation": row[10]
            }
            comments.append(comment)
            
            # Add annotation if exists
            if row[11] is not None:  # annotation_id exists
                annotation = {
                    "id": row[11],
                    "comment_id": row[0],
                    "document_id": row[1],
                    "page": row[5],
                    "x": float(row[12]),
                    "y": float(row[13]),
                    "description": row[7]
                }
                annotations.append(annotation)
        
        return jsonify({
            "success": True,
            "comments": comments,
            "annotations": annotations
        })
        
    except Exception as e:
        print(f"Error fetching comments: {str(e)}")
        return jsonify({"success": False, "message": "Internal server error"}), 500

# Create a new comment
@app.route('/api/comments', methods=['POST'])
def create_comment():
    """Create a new comment with optional annotation"""
    try:
        data = request.json
        if not data:
            return jsonify({"success": False, "message": "No data provided"}), 400
        
        # Validate required fields
        required_fields = ['document_id', 'document_name', 'description', 'author']
        for field in required_fields:
            if field not in data or not data[field]:
                return jsonify({"success": False, "message": f"Missing required field: {field}"}), 400
        
        cur = conn.cursor()
        
        # Insert comment
        cur.execute("""
            INSERT INTO document_comments (
                document_id, document_name, version, reviewer_id, 
                page_no, section, description, author, is_annotation
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            RETURNING comment_id
        """, (
            data['document_id'],
            data['document_name'],
            data.get('version'),
            data.get('reviewer_id'),
            data.get('page_no'),
            data.get('section'),
            data['description'],
            data['author'],
            data.get('is_annotation', False)
        ))
        
        comment_id = cur.fetchone()[0]
        
        # Insert annotation if provided
        if data.get('is_annotation') and 'x' in data and 'y' in data:
            cur.execute("""
                INSERT INTO document_annotations (
                    comment_id, document_id, page_no, x_position, y_position
                ) VALUES (%s, %s, %s, %s, %s)
            """, (
                comment_id,
                data['document_id'],
                data.get('page_no', 1),
                data['x'],
                data['y']
            ))
        
        conn.commit()
        cur.close()
        
        return jsonify({
            "success": True,
            "message": "Comment created successfully",
            "comment_id": comment_id
        })
        
    except Exception as e:
        conn.rollback()
        print(f"Error creating comment: {str(e)}")
        return jsonify({"success": False, "message": "Internal server error"}), 500

# Update a comment
@app.route('/api/comments/<int:comment_id>', methods=['PUT'])
def update_comment(comment_id):
    """Update an existing comment"""
    try:
        data = request.json
        if not data:
            return jsonify({"success": False, "message": "No data provided"}), 400
        
        cur = conn.cursor()
        
        # Update comment
        cur.execute("""
            UPDATE document_comments 
            SET description = %s, section = %s, page_no = %s
            WHERE comment_id = %s
        """, (
            data.get('description'),
            data.get('section'),
            data.get('page_no'),
            comment_id
        ))
        
        if cur.rowcount == 0:
            cur.close()
            return jsonify({"success": False, "message": "Comment not found"}), 404
        
        conn.commit()
        cur.close()
        
        return jsonify({
            "success": True,
            "message": "Comment updated successfully"
        })
        
    except Exception as e:
        conn.rollback()
        print(f"Error updating comment: {str(e)}")
        return jsonify({"success": False, "message": "Internal server error"}), 500

# Delete a comment
@app.route('/api/comments/<int:comment_id>', methods=['DELETE'])
def delete_comment(comment_id):
    """Delete a comment and its associated annotation"""
    try:
        cur = conn.cursor()
        
        # Delete comment (annotations will be deleted due to CASCADE)
        cur.execute("DELETE FROM document_comments WHERE comment_id = %s", (comment_id,))
        
        if cur.rowcount == 0:
            cur.close()
            return jsonify({"success": False, "message": "Comment not found"}), 404
        
        conn.commit()
        cur.close()
        
        return jsonify({
            "success": True,
            "message": "Comment deleted successfully"
        })
        
    except Exception as e:
        conn.rollback()
        print(f"Error deleting comment: {str(e)}")
        return jsonify({"success": False, "message": "Internal server error"}), 500

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=8000)
