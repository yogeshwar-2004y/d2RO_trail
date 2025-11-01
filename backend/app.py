"""
Main Flask application with modular structure using blueprints
"""
from flask import Flask, request, jsonify
from flask_cors import CORS

# Import configuration and utilities
from config import Config, get_db_connection
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
from routes.memos import memos_bp
from routes.reports import reports_bp
from routes.conformal_coating_inspection import conformal_coating_bp
from routes.mechanical_inspection import mechanical_inspection_bp
from routes.kit_of_parts import kit_of_parts_bp
from routes.login_logs import login_logs_bp
from routes.tech_support import tech_support_bp

def create_app():
    """Application factory pattern"""
    app = Flask(__name__)
    
    # Load configuration
    app.config.from_object(Config)
    
    # Enable CORS
    CORS(app, resources={r"/api/*": {"origins": "*"}})
    

    # Create upload directories
    create_upload_directories()
    
    # Initialize database - DISABLED: Tables are managed manually in pgAdmin
    # initialize_database()
    
    # Register blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(projects_bp)
    app.register_blueprint(users_bp)
    app.register_blueprint(documents_bp)
    app.register_blueprint(tests_bp)
    app.register_blueprint(news_bp)
    app.register_blueprint(files_bp)
    app.register_blueprint(memos_bp)
    app.register_blueprint(reports_bp)
    app.register_blueprint(conformal_coating_bp)
    app.register_blueprint(mechanical_inspection_bp)
    app.register_blueprint(kit_of_parts_bp)
    app.register_blueprint(login_logs_bp)
    app.register_blueprint(tech_support_bp)
    
    return app

# Create the application instance
app = create_app()

# Users API Endpoints

# Get available reviewers
@app.route('/api/users/reviewers', methods=['GET'])
def get_reviewers():
    """Get all users with reviewer role"""
    try:
        conn = get_db_connection()
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
        
        # Convert document_id to integer since it's now an INT foreign key
        try:
            document_id = int(document_id)
        except ValueError:
            return jsonify({"success": False, "message": "Document ID must be a valid integer"}), 400
        
        conn = get_db_connection()
        cur = conn.cursor()
        
        # Test the connection first
        cur.execute("SELECT 1")
        cur.fetchone()
        
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
                c.created_at,
                c.is_annotation,
                c.status,
                c.justification,
                c.accepted_by,
                c.accepted_at,
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
        conn.close()
        
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
                "created_at": row[8].isoformat() if row[8] else None,
                "annotation": row[9],
                "status": row[10],
                "justification": row[11],
                "accepted_by": row[12],
                "accepted_at": row[13].isoformat() if row[13] else None
            }
            comments.append(comment)
            
            # Add annotation if exists
            if row[14] is not None:  # annotation_id exists
                annotation = {
                    "id": row[14],
                    "comment_id": row[0],
                    "document_id": row[1],
                    "page": row[5],
                    "x": float(row[15]),
                    "y": float(row[16]),
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
        try:
            if 'cur' in locals():
                cur.close()
            if 'conn' in locals():
                conn.close()
        except:
            pass
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
        required_fields = ['document_id', 'document_name', 'description', 'reviewer_id', 'user_role']
        for field in required_fields:
            if field not in data or not data[field]:
                return jsonify({"success": False, "message": f"Missing required field: {field}"}), 400
        
        # Convert document_id to integer since it's now an INT foreign key
        try:
            document_id = int(data['document_id'])
        except (ValueError, TypeError):
            return jsonify({"success": False, "message": "Document ID must be a valid integer"}), 400
        
        # Check if user has permission to add comments (only QA Reviewer)
        if data.get('user_role') != 'QA Reviewer':
            return jsonify({"success": False, "message": "Only QA Reviewers can add comments"}), 403
        
        conn = get_db_connection()
        cur = conn.cursor()
        
        # Additionally block comments if THIS specific document is already accepted
        cur.execute(
            """
            SELECT status
            FROM plan_documents
            WHERE document_id = %s AND is_active = TRUE
            """,
            (document_id,),
        )
        doc_status_row = cur.fetchone()
        if doc_status_row and doc_status_row[0] == 'accepted':
            cur.close()
            return jsonify({
                "success": False,
                "message": "Cannot add comments. This document is already accepted as the final version."
            }), 400

        # Prepare commented_by (string) - prefer explicit field, else use reviewer_id, else 'Anonymous'
        commented_by_val = data.get('commented_by') or (str(data.get('reviewer_id')) if data.get('reviewer_id') else 'Anonymous')
        print(f"Creating comment: document_id={data.get('document_id')} reviewer_id={data.get('reviewer_id')} commented_by={commented_by_val}")

        # Insert comment (include commented_by to satisfy NOT NULL constraint)
        cur.execute("""
            INSERT INTO document_comments (
                document_id, document_name, version, reviewer_id, 
                page_no, section, description, is_annotation, commented_by
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            RETURNING comment_id
        """, (
            document_id,  # Use the converted integer document_id
            data['document_name'],
            data.get('version'),
            data.get('reviewer_id'),
            data.get('page_no'),
            data.get('section'),
            data['description'],
            data.get('is_annotation', False),
            commented_by_val
        ))
        
        comment_id = cur.fetchone()[0]
        
        # Insert annotation if provided
        if data.get('is_annotation') and 'x' in data and 'y' in data:
            print(f"Creating annotation for comment {comment_id}: x={data['x']}, y={data['y']}, page={data.get('page_no', 1)}")
            cur.execute("""
                INSERT INTO document_annotations (
                    comment_id, document_id, page_no, x_position, y_position
                ) VALUES (%s, %s, %s, %s, %s)
            """, (
                comment_id,
                document_id,  # Use the converted integer document_id
                data.get('page_no', 1),
                data['x'],
                data['y']
            ))
            print(f"Annotation created successfully for comment {comment_id}")
        else:
            print(f"No annotation data for comment {comment_id}: is_annotation={data.get('is_annotation')}, x={data.get('x')}, y={data.get('y')}")
        
        conn.commit()
        
        # Send notifications to all designers in the project when a reviewer adds a comment
        from utils.activity_logger import log_notification, log_activity
        
        # Get project_id from the document (plan_documents -> lrus -> projects)
        cur.execute("""
            SELECT p.project_id, p.project_name, l.lru_id, l.lru_name
            FROM plan_documents pd
            JOIN lrus l ON pd.lru_id = l.lru_id
            JOIN projects p ON l.project_id = p.project_id
            WHERE pd.document_id = %s
        """, (document_id,))
        
        project_info = cur.fetchone()
        if project_info:
            project_id = project_info[0]
            project_name = project_info[1]
            lru_id = project_info[2]
            lru_name = project_info[3]
            
            # Get reviewer name
            reviewer_name = "Unknown Reviewer"
            reviewer_id = data.get('reviewer_id')
            if reviewer_id:
                cur.execute("SELECT name FROM users WHERE user_id = %s", (reviewer_id,))
                reviewer_result = cur.fetchone()
                if reviewer_result:
                    reviewer_name = reviewer_result[0]
            
            # Get all designers in the project (role_id = 5)
            cur.execute("""
                SELECT DISTINCT u.user_id, u.name, u.email
                FROM users u
                JOIN user_roles ur ON u.user_id = ur.user_id
                JOIN project_users pu ON u.user_id = pu.user_id
                WHERE pu.project_id = %s AND ur.role_id = 5
            """, (project_id,))
            
            designers = cur.fetchall()
            
            # Log activity for comment creation
            log_activity(
                project_id=project_id,
                activity_performed=f"Comment Added to Plan Document",
                performed_by=reviewer_id,
                additional_info=f"Reviewer {reviewer_name} added a comment to document '{data.get('document_name')}' in LRU '{lru_name}' for project '{project_name}'."
            )
            
            # Send notification to all designers in the project
            for designer in designers:
                designer_id = designer[0]
                designer_name = designer[1]
                
                log_notification(
                    project_id=project_id,
                    activity_performed="New Comment on Plan Document",
                    performed_by=reviewer_id,
                    notified_user_id=designer_id,
                    notification_type="plan_document_comment",
                    additional_info=f"Reviewer {reviewer_name} added a comment to document '{data.get('document_name')}' in LRU '{lru_name}' of project '{project_name}'. Please review and address the feedback."
                )
                
                print(f"   ✓ Sent notification to designer: {designer_name} (ID: {designer_id})")
        
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
        
        conn = get_db_connection()
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
        data = request.json or {}
        user_role = data.get('user_role')
        
        # Check if user has permission to delete comments (only QA Reviewer)
        if user_role != 'QA Reviewer':
            return jsonify({"success": False, "message": "Only QA Reviewers can delete comments"}), 403
        
        conn = get_db_connection()
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

# Accept a comment
@app.route('/api/comments/<int:comment_id>/accept', methods=['POST'])
def accept_comment(comment_id):
    """Accept a comment with justification"""
    try:
        data = request.json
        if not data:
            return jsonify({"success": False, "message": "No data provided"}), 400
        
        # Validate required fields
        required_fields = ['justification', 'accepted_by', 'user_role']
        for field in required_fields:
            if field not in data or not data[field]:
                return jsonify({"success": False, "message": f"Missing required field: {field}"}), 400
        
        # Check if user has permission to accept comments (only Designer or Design Head)
        if data.get('user_role') not in ['Designer', 'Design Head']:
            return jsonify({"success": False, "message": "Only Designers and Design Heads can accept comments"}), 403
        
        conn = get_db_connection()
        cur = conn.cursor()
        
        # Debug logging
        print(f"Accepting comment {comment_id} with data: {data}")
        
        # Update comment status to accepted
        cur.execute("""
            UPDATE document_comments 
            SET status = 'accepted', 
                justification = %s, 
                accepted_by = %s, 
                accepted_at = CURRENT_TIMESTAMP
            WHERE comment_id = %s
        """, (
            data['justification'],
            int(data['accepted_by']),
            comment_id
        ))
        
        print(f"Updated {cur.rowcount} rows for comment {comment_id}")
        
        if cur.rowcount == 0:
            cur.close()
            return jsonify({"success": False, "message": "Comment not found"}), 404
        
        conn.commit()
        
        # Send notification to the reviewer when their comment is accepted
        from utils.activity_logger import log_notification, log_activity
        
        # Get comment details including reviewer_id, document info, and project info
        cur.execute("""
            SELECT dc.reviewer_id, dc.document_name, dc.description,
                   pd.document_id, pd.document_number,
                   l.lru_id, l.lru_name, p.project_id, p.project_name
            FROM document_comments dc
            JOIN plan_documents pd ON dc.document_id = pd.document_id
            JOIN lrus l ON pd.lru_id = l.lru_id
            JOIN projects p ON l.project_id = p.project_id
            WHERE dc.comment_id = %s
        """, (comment_id,))
        
        comment_info = cur.fetchone()
        if comment_info:
            reviewer_id = comment_info[0]
            document_name = comment_info[1]
            comment_description = comment_info[2]
            document_number = comment_info[5]
            lru_name = comment_info[6]
            project_id = comment_info[7]
            project_name = comment_info[8]
            
            # Get designer/design head name who accepted the comment
            designer_name = "Unknown Designer"
            accepted_by_id = int(data['accepted_by'])
            cur.execute("SELECT name FROM users WHERE user_id = %s", (accepted_by_id,))
            designer_result = cur.fetchone()
            if designer_result:
                designer_name = designer_result[0]
            
            # Get reviewer name
            reviewer_name = "Unknown Reviewer"
            if reviewer_id:
                cur.execute("SELECT name FROM users WHERE user_id = %s", (reviewer_id,))
                reviewer_result = cur.fetchone()
                if reviewer_result:
                    reviewer_name = reviewer_result[0]
            
            # Log activity for comment acceptance
            log_activity(
                project_id=project_id,
                activity_performed="Comment Accepted",
                performed_by=accepted_by_id,
                additional_info=f"{designer_name} accepted a comment on document '{document_name}' ({document_number}) in LRU '{lru_name}' for project '{project_name}'."
            )
            
            # Send notification to the reviewer
            log_notification(
                project_id=project_id,
                activity_performed="Your Comment Was Accepted",
                performed_by=accepted_by_id,
                notified_user_id=reviewer_id,
                notification_type="comment_accepted",
                additional_info=f"Designer {designer_name} accepted your comment on document '{document_name}' ({document_number}) in LRU '{lru_name}' of project '{project_name}'. Justification: {data.get('justification', 'N/A')}"
            )
            
            print(f"   ✓ Sent notification to reviewer: {reviewer_name} (ID: {reviewer_id})")
        
        cur.close()
        
        return jsonify({
            "success": True,
            "message": "Comment accepted successfully"
        })
        
    except Exception as e:
        if 'conn' in locals():
            conn.rollback()
        print(f"Error accepting comment: {str(e)}")
        return jsonify({"success": False, "message": f"Internal server error: {str(e)}"}), 500

# Reject a comment
@app.route('/api/comments/<int:comment_id>/reject', methods=['POST'])
def reject_comment(comment_id):
    """Reject a comment with justification"""
    try:
        data = request.json
        if not data:
            return jsonify({"success": False, "message": "No data provided"}), 400
        
        # Validate required fields
        required_fields = ['justification', 'accepted_by', 'user_role']
        for field in required_fields:
            if field not in data or not data[field]:
                return jsonify({"success": False, "message": f"Missing required field: {field}"}), 400
        
        # Check if user has permission to reject comments (only Designer or Design Head)
        if data.get('user_role') not in ['Designer', 'Design Head']:
            return jsonify({"success": False, "message": "Only Designers and Design Heads can reject comments"}), 403
        
        conn = get_db_connection()
        cur = conn.cursor()
        
        # Debug logging
        print(f"Rejecting comment {comment_id} with data: {data}")
        
        # Update comment status to rejected
        cur.execute("""
            UPDATE document_comments 
            SET status = 'rejected', 
                justification = %s, 
                accepted_by = %s, 
                accepted_at = CURRENT_TIMESTAMP
            WHERE comment_id = %s
        """, (
            data['justification'],
            int(data['accepted_by']),
            comment_id
        ))
        
        print(f"Updated {cur.rowcount} rows for comment {comment_id}")
        
        if cur.rowcount == 0:
            cur.close()
            return jsonify({"success": False, "message": "Comment not found"}), 404
        
        conn.commit()
        
        # Send notification to the reviewer when their comment is rejected
        from utils.activity_logger import log_notification, log_activity
        
        # Get comment details including reviewer_id, document info, and project info
        cur.execute("""
            SELECT dc.reviewer_id, dc.document_name, dc.description,
                   pd.document_id, pd.document_number,
                   l.lru_id, l.lru_name, p.project_id, p.project_name
            FROM document_comments dc
            JOIN plan_documents pd ON dc.document_id = pd.document_id
            JOIN lrus l ON pd.lru_id = l.lru_id
            JOIN projects p ON l.project_id = p.project_id
            WHERE dc.comment_id = %s
        """, (comment_id,))
        
        comment_info = cur.fetchone()
        if comment_info:
            reviewer_id = comment_info[0]
            document_name = comment_info[1]
            comment_description = comment_info[2]
            document_number = comment_info[5]
            lru_name = comment_info[6]
            project_id = comment_info[7]
            project_name = comment_info[8]
            
            # Get designer/design head name who rejected the comment
            designer_name = "Unknown Designer"
            accepted_by_id = int(data['accepted_by'])
            cur.execute("SELECT name FROM users WHERE user_id = %s", (accepted_by_id,))
            designer_result = cur.fetchone()
            if designer_result:
                designer_name = designer_result[0]
            
            # Get reviewer name
            reviewer_name = "Unknown Reviewer"
            if reviewer_id:
                cur.execute("SELECT name FROM users WHERE user_id = %s", (reviewer_id,))
                reviewer_result = cur.fetchone()
                if reviewer_result:
                    reviewer_name = reviewer_result[0]
            
            # Log activity for comment rejection
            log_activity(
                project_id=project_id,
                activity_performed="Comment Rejected",
                performed_by=accepted_by_id,
                additional_info=f"{designer_name} rejected a comment on document '{document_name}' ({document_number}) in LRU '{lru_name}' for project '{project_name}'."
            )
            
            # Send notification to the reviewer
            log_notification(
                project_id=project_id,
                activity_performed="Your Comment Was Rejected",
                performed_by=accepted_by_id,
                notified_user_id=reviewer_id,
                notification_type="comment_rejected",
                additional_info=f"Designer {designer_name} rejected your comment on document '{document_name}' ({document_number}) in LRU '{lru_name}' of project '{project_name}'. Justification: {data.get('justification', 'N/A')}"
            )
            
            print(f"   ✓ Sent notification to reviewer: {reviewer_name} (ID: {reviewer_id})")
        
        cur.close()
        
        return jsonify({
            "success": True,
            "message": "Comment rejected successfully"
        })
        
    except Exception as e:
        if 'conn' in locals():
            conn.rollback()
        print(f"Error rejecting comment: {str(e)}")
        return jsonify({"success": False, "message": f"Internal server error: {str(e)}"}), 500

# Test endpoint to check database tables
@app.route('/api/test-db', methods=['GET'])
def test_database():
    """Test endpoint to check if database tables exist and are accessible"""
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        
        # Check if document_comments table exists
        cur.execute("""
            SELECT EXISTS (
                SELECT FROM information_schema.tables 
                WHERE table_name = 'document_comments'
            );
        """)
        comments_table_exists = cur.fetchone()[0]
        
        # Check if document_annotations table exists
        cur.execute("""
            SELECT EXISTS (
                SELECT FROM information_schema.tables 
                WHERE table_name = 'document_annotations'
            );
        """)
        annotations_table_exists = cur.fetchone()[0]
        
        # Get table schemas
        cur.execute("""
            SELECT column_name, data_type, is_nullable
            FROM information_schema.columns 
            WHERE table_name = 'document_comments'
            ORDER BY ordinal_position;
        """)
        comments_schema = cur.fetchall()
        
        cur.execute("""
            SELECT column_name, data_type, is_nullable
            FROM information_schema.columns 
            WHERE table_name = 'document_annotations'
            ORDER BY ordinal_position;
        """)
        annotations_schema = cur.fetchall()
        
        cur.close()
        
        return jsonify({
            "success": True,
            "tables": {
                "document_comments": {
                    "exists": comments_table_exists,
                    "schema": [{"column": row[0], "type": row[1], "nullable": row[2]} for row in comments_schema]
                },
                "document_annotations": {
                    "exists": annotations_table_exists,
                    "schema": [{"column": row[0], "type": row[1], "nullable": row[2]} for row in annotations_schema]
                }
            }
        })
        
    except Exception as e:
        return jsonify({"success": False, "message": f"Database test failed: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000)
