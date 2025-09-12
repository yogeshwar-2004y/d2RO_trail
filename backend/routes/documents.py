"""
Plan document management routes
"""
import os
import uuid
from datetime import datetime
from flask import Blueprint, request, jsonify
from config import get_db_connection, Config
from utils.helpers import allowed_file, validate_file_size, handle_database_error

documents_bp = Blueprint('documents', __name__)

@documents_bp.route('/api/lrus/<int:lru_id>/plan-documents', methods=['GET'])
def get_lru_plan_documents(lru_id):
    """Get plan documents for a specific LRU"""
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        
        # First verify the LRU exists
        cur.execute("""
            SELECT l.lru_id, l.lru_name, p.project_name
            FROM lrus l
            JOIN projects p ON l.project_id = p.project_id
            WHERE l.lru_id = %s
        """, (lru_id,))
        
        lru = cur.fetchone()
        if not lru:
            cur.close()
            return jsonify({"success": False, "message": "LRU not found"}), 404
        
        # Fetch plan documents for the specific LRU
        cur.execute("""
            SELECT 
                pd.document_id,
                pd.document_number,
                pd.version,
                pd.revision,
                pd.doc_ver,
                pd.uploaded_by,
                pd.upload_date,
                pd.file_path,
                pd.status,
                pd.original_filename,
                u.name as uploaded_by_name
            FROM plan_documents pd
            JOIN users u ON pd.uploaded_by = u.user_id
            WHERE pd.lru_id = %s AND pd.is_active = TRUE
            ORDER BY pd.document_id DESC
        """, (lru_id,))
        
        documents = cur.fetchall()
        cur.close()
        
        # Convert to list of dictionaries
        document_list = []
        for doc in documents:
            document_list.append({
                "document_id": doc[0],
                "document_number": doc[1],
                "version": doc[2],
                "revision": doc[3],
                "doc_ver": doc[4],
                "uploaded_by": doc[5],
                "uploaded_by_name": doc[10],
                "upload_date": doc[6].isoformat() if doc[6] else None,
                "file_path": doc[7],
                "status": doc[8],
                "original_filename": doc[9]
            })
        
        return jsonify({
            "success": True,
            "lru": {
                "lru_id": lru[0],
                "lru_name": lru[1],
                "project_name": lru[2]
            },
            "documents": document_list
        })
        
    except Exception as e:
        print(f"Error fetching plan documents for LRU {lru_id}: {str(e)}")
        return jsonify({"success": False, "message": "Internal server error"}), 500

@documents_bp.route('/api/projects/<int:project_id>/plan-documents', methods=['GET'])
def get_project_plan_documents(project_id):
    """Get plan documents for a project (all LRUs)"""
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        
        # First verify the project exists
        cur.execute("""
            SELECT project_id, project_name
            FROM projects
            WHERE project_id = %s
        """, (project_id,))
        
        project = cur.fetchone()
        if not project:
            cur.close()
            return jsonify({"success": False, "message": "Project not found"}), 404
        
        # Fetch plan documents for all LRUs in the project
        cur.execute("""
            SELECT 
                l.lru_id,
                l.lru_name,
                pd.document_id,
                pd.document_number,
                pd.version,
                pd.revision,
                pd.doc_ver,
                pd.uploaded_by,
                pd.upload_date,
                pd.file_path,
                pd.status,
                u.name as uploaded_by_name
            FROM lrus l
            LEFT JOIN plan_documents pd ON l.lru_id = pd.lru_id AND pd.is_active = TRUE
            LEFT JOIN users u ON pd.uploaded_by = u.user_id
            WHERE l.project_id = %s
            ORDER BY l.lru_id, pd.document_id DESC
        """, (project_id,))
        
        results = cur.fetchall()
        cur.close()
        
        # Organize data by LRU
        lrus_dict = {}
        
        for row in results:
            lru_id = row[0]
            lru_name = row[1]
            
            # Initialize LRU if not exists
            if lru_id not in lrus_dict:
                lrus_dict[lru_id] = {
                    "lru_id": lru_id,
                    "lru_name": lru_name,
                    "documents": []
                }
            
            # Add document if it exists
            if row[2]:  # document_id exists
                lrus_dict[lru_id]["documents"].append({
                    "document_id": row[2],
                    "document_number": row[3],
                    "version": row[4],
                    "revision": row[5],
                    "doc_ver": row[6],
                    "uploaded_by": row[7],
                    "uploaded_by_name": row[11],
                    "upload_date": row[8].isoformat() if row[8] else None,
                    "file_path": row[9],
                    "status": row[10]
                })
        
        return jsonify({
            "success": True,
            "project": {
                "project_id": project[0],
                "project_name": project[1]
            },
            "lrus": list(lrus_dict.values())
        })
        
    except Exception as e:
        print(f"Error fetching plan documents for project {project_id}: {str(e)}")
        return jsonify({"success": False, "message": "Internal server error"}), 500

@documents_bp.route('/api/plan-documents', methods=['POST'])
def upload_plan_document():
    """Upload plan document"""
    try:
        # Check if file is present in request
        if 'file' not in request.files:
            return jsonify({"success": False, "message": "No file provided"}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({"success": False, "message": "No file selected"}), 400
        
        # Get form data
        lru_id = request.form.get('lru_id')
        document_number = request.form.get('document_number')
        version = request.form.get('version')
        revision = request.form.get('revision')
        doc_ver = request.form.get('doc_ver')
        uploaded_by = request.form.get('uploaded_by')
        
        # Validate required fields
        if not all([lru_id, document_number, version, uploaded_by]):
            return jsonify({"success": False, "message": "Missing required fields"}), 400
        
        # Validate file
        if not allowed_file(file.filename):
            return jsonify({"success": False, "message": "File type not allowed"}), 400
        
        # Check file size
        if not validate_file_size(file, Config.MAX_FILE_SIZE):
            return jsonify({"success": False, "message": "File too large. Maximum size is 50MB"}), 400
        
        conn = get_db_connection()
        cur = conn.cursor()
        
        # Verify LRU exists
        cur.execute("SELECT lru_id FROM lrus WHERE lru_id = %s", (lru_id,))
        if not cur.fetchone():
            cur.close()
            return jsonify({"success": False, "message": "LRU not found"}), 404
        
        # Generate unique filename
        file_extension = file.filename.rsplit('.', 1)[1].lower()
        unique_filename = f"{uuid.uuid4()}.{file_extension}"
        file_path = os.path.join(Config.UPLOAD_FOLDER, unique_filename)
        
        # Save file to local storage
        file.save(file_path)
        
        # Get file size for database
        file_size = os.path.getsize(file_path)
        
        # Insert plan document with actual file path
        cur.execute("""
            INSERT INTO plan_documents 
            (lru_id, document_number, version, revision, doc_ver, uploaded_by, file_path, status, original_filename, file_size, upload_date)
            VALUES (%s, %s, %s, %s, %s, %s, %s, 'not assigned', %s, %s, %s)
            RETURNING document_id
        """, (lru_id, document_number, version, revision, doc_ver, uploaded_by, file_path, file.filename, file_size, datetime.now()))
        
        document_id = cur.fetchone()[0]
        conn.commit()
        cur.close()
        
        return jsonify({
            "success": True,
            "message": "Plan document uploaded successfully",
            "document_id": document_id,
            "file_path": file_path,
            "original_filename": file.filename
        })
        
    except Exception as e:
        # Clean up file if database insert failed
        if 'file_path' in locals() and os.path.exists(file_path):
            os.remove(file_path)
        return handle_database_error(get_db_connection(), f"Error uploading plan document: {str(e)}")

@documents_bp.route('/api/plan-documents/<int:document_id>/status', methods=['PUT'])
def update_plan_document_status(document_id):
    """Update plan document status"""
    try:
        data = request.json
        if not data:
            return jsonify({"success": False, "message": "No data provided"}), 400
        
        new_status = data.get('status')
        if not new_status:
            return jsonify({"success": False, "message": "Status is required"}), 400
        
        # Validate status
        valid_statuses = ['cleared', 'disapproved', 'assigned and returned', 'moved to next stage', 'not cleared', 'not assigned']
        if new_status not in valid_statuses:
            return jsonify({"success": False, "message": "Invalid status"}), 400
        
        conn = get_db_connection()
        cur = conn.cursor()
        
        # Update document status
        cur.execute("""
            UPDATE plan_documents 
            SET status = %s
            WHERE document_id = %s AND is_active = TRUE
            RETURNING document_id
        """, (new_status, document_id))
        
        result = cur.fetchone()
        if not result:
            cur.close()
            return jsonify({"success": False, "message": "Document not found"}), 404
        
        conn.commit()
        cur.close()
        
        return jsonify({
            "success": True,
            "message": "Document status updated successfully"
        })
        
    except Exception as e:
        return handle_database_error(get_db_connection(), f"Error updating plan document status: {str(e)}")

@documents_bp.route('/api/plan-documents/<int:document_id>', methods=['GET'])
def get_plan_document(document_id):
    """Get plan document details including file path"""
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        
        cur.execute("""
            SELECT pd.document_id, pd.lru_id, pd.document_number, pd.version, pd.revision, 
                   pd.doc_ver, pd.uploaded_by, pd.file_path, pd.status, pd.original_filename, 
                   pd.file_size, pd.upload_date, u.name as uploaded_by_name, l.lru_name
            FROM plan_documents pd
            LEFT JOIN users u ON pd.uploaded_by = u.user_id
            LEFT JOIN lrus l ON pd.lru_id = l.lru_id
            WHERE pd.document_id = %s
        """, (document_id,))
        
        document = cur.fetchone()
        cur.close()
        
        if not document:
            return jsonify({"success": False, "message": "Document not found"}), 404
        
        return jsonify({
            "success": True,
            "document": {
                "document_id": document[0],
                "lru_id": document[1],
                "document_number": document[2],
                "version": document[3],
                "revision": document[4],
                "doc_ver": document[5],
                "uploaded_by": document[6],
                "file_path": document[7],
                "status": document[8],
                "original_filename": document[9],
                "file_size": document[10],
                "upload_date": document[11].isoformat() if document[11] else None,
                "uploaded_by_name": document[12],
                "lru_name": document[13]
            }
        })
        
    except Exception as e:
        print(f"Error fetching document {document_id}: {str(e)}")
        return jsonify({"success": False, "message": "Internal server error"}), 500

@documents_bp.route('/api/plan-documents/next-doc-ver/<int:lru_id>', methods=['GET'])
def get_next_doc_ver(lru_id):
    """Get the next doc_ver number for a specific LRU"""
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        
        # Get the highest doc_ver for this LRU
        cur.execute("""
            SELECT MAX(CAST(doc_ver AS INTEGER)) 
            FROM plan_documents 
            WHERE lru_id = %s
        """, (lru_id,))
        
        result = cur.fetchone()
        cur.close()
        
        # If no documents exist for this LRU, start with 1
        max_doc_ver = result[0] if result[0] is not None else 0
        next_doc_ver = max_doc_ver + 1
        
        return jsonify({
            "success": True,
            "nextDocVer": next_doc_ver,
            "lruId": lru_id
        })
        
    except Exception as e:
        print(f"Error getting next doc_ver for LRU {lru_id}: {str(e)}")
        # Rollback the transaction to clear the error state
        try:
            get_db_connection().rollback()
        except:
            pass
        return jsonify({"success": False, "message": "Internal server error"}), 500

@documents_bp.route('/api/assign-reviewer', methods=['POST'])
def assign_reviewer():
    """Assign a reviewer to a document based on LRU context"""
    try:
        data = request.json
        if not data:
            return jsonify({"success": False, "message": "No data provided"}), 400
        
        # Validate required fields
        lru_name = data.get('lru_name')
        project_name = data.get('project_name')
        reviewer_id = data.get('reviewer_id')
        assigned_by = data.get('assigned_by', 1002)  # Default assigned_by
        
        if not all([lru_name, project_name, reviewer_id]):
            return jsonify({"success": False, "message": "Missing required fields: lru_name, project_name, reviewer_id"}), 400
        
        conn = get_db_connection()
        cur = conn.cursor()
        
        # Find the LRU ID based on LRU name and project name
        cur.execute("""
            SELECT l.lru_id
            FROM lrus l
            JOIN projects p ON l.project_id = p.project_id
            WHERE l.lru_name = %s AND p.project_name = %s
        """, (lru_name, project_name))
        
        lru_result = cur.fetchone()
        if not lru_result:
            cur.close()
            return jsonify({"success": False, "message": "LRU not found for the specified project"}), 404
        
        lru_id = lru_result[0]
        
        # Find the active document for this LRU
        cur.execute("""
            SELECT document_id
            FROM plan_documents
            WHERE lru_id = %s AND is_active = TRUE
            ORDER BY upload_date DESC
            LIMIT 1
        """, (lru_id,))
        
        doc_result = cur.fetchone()
        if not doc_result:
            cur.close()
            return jsonify({"success": False, "message": "No active document found for this LRU"}), 404
        
        document_id = doc_result[0]
        
        # Check if reviewer exists and has QA Reviewer role
        cur.execute("""
            SELECT u.user_id 
            FROM users u
            JOIN user_roles ur ON u.user_id = ur.user_id
            WHERE u.user_id = %s AND ur.role_id = 3
        """, (reviewer_id,))
        
        if not cur.fetchone():
            cur.close()
            return jsonify({"success": False, "message": "Reviewer not found or not a QA Reviewer"}), 404
        
        # Check if assignment already exists for this document
        cur.execute("""
            SELECT assignment_id FROM plan_doc_assignment 
            WHERE document_id = %s AND user_id = %s
        """, (document_id, reviewer_id))
        
        existing_assignment = cur.fetchone()
        
        if existing_assignment:
            cur.close()
            return jsonify({"success": False, "message": "This reviewer is already assigned to the active document for this LRU"}), 400
        
        # Insert new assignment
        cur.execute("""
            INSERT INTO plan_doc_assignment (document_id, user_id, assigned_at)
            VALUES (%s, %s, NOW())
            RETURNING assignment_id
        """, (document_id, reviewer_id))
        
        assignment_id = cur.fetchone()[0]
        
        # Update document status to 'assigned'
        cur.execute("""
            UPDATE plan_documents 
            SET status = 'assigned'
            WHERE document_id = %s
        """, (document_id,))
        
        conn.commit()
        cur.close()
        
        return jsonify({
            "success": True,
            "message": "Reviewer assigned successfully",
            "assignment_id": assignment_id,
            "document_id": document_id,
            "lru_id": lru_id
        })
        
    except Exception as e:
        return handle_database_error(get_db_connection(), f"Error assigning reviewer: {str(e)}")

@documents_bp.route('/api/test-assignments', methods=['GET'])
def test_assignments():
    """Test endpoint to view all assignments"""
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        
        # Show all assignments with details
        cur.execute("""
            SELECT 
                pda.assignment_id,
                pda.document_id,
                pda.user_id,
                pda.assigned_at,
                u.name as reviewer_name,
                pd.document_number,
                pd.status as doc_status,
                l.lru_name,
                p.project_name
            FROM plan_doc_assignment pda
            JOIN users u ON pda.user_id = u.user_id
            JOIN plan_documents pd ON pda.document_id = pd.document_id
            JOIN lrus l ON pd.lru_id = l.lru_id
            JOIN projects p ON l.project_id = p.project_id
            ORDER BY pda.assigned_at DESC
        """)
        assignments = cur.fetchall()
        
        cur.close()
        
        assignment_list = []
        for assignment in assignments:
            assignment_list.append({
                "assignment_id": assignment[0],
                "document_id": assignment[1],
                "user_id": assignment[2],
                "assigned_at": assignment[3].isoformat() if assignment[3] else None,
                "reviewer_name": assignment[4],
                "document_number": assignment[5],
                "doc_status": assignment[6],
                "lru_name": assignment[7],
                "project_name": assignment[8]
            })
        
        return jsonify({
            "success": True,
            "assignments": assignment_list
        })
        
    except Exception as e:
        print(f"Test assignments error: {str(e)}")
        return jsonify({"success": False, "message": f"Test error: {str(e)}"}), 500

@documents_bp.route('/api/assigned-reviewer', methods=['GET'])
def get_assigned_reviewer():
    """Get the assigned reviewer for a document based on LRU and project context"""
    try:
        lru_name = request.args.get('lru_name')
        project_name = request.args.get('project_name')
        
        if not all([lru_name, project_name]):
            return jsonify({"success": False, "message": "Missing required parameters: lru_name, project_name"}), 400
        
        conn = get_db_connection()
        cur = conn.cursor()
        
        # Find the LRU ID based on LRU name and project name
        cur.execute("""
            SELECT l.lru_id
            FROM lrus l
            JOIN projects p ON l.project_id = p.project_id
            WHERE l.lru_name = %s AND p.project_name = %s
        """, (lru_name, project_name))
        
        lru_result = cur.fetchone()
        if not lru_result:
            cur.close()
            return jsonify({"success": False, "message": "LRU not found for the specified project"}), 404
        
        lru_id = lru_result[0]
        
        # Find the active document for this LRU
        cur.execute("""
            SELECT document_id
            FROM plan_documents
            WHERE lru_id = %s AND is_active = TRUE
            ORDER BY upload_date DESC
            LIMIT 1
        """, (lru_id,))
        
        doc_result = cur.fetchone()
        if not doc_result:
            cur.close()
            return jsonify({"success": False, "message": "No active document found for this LRU"}), 404
        
        document_id = doc_result[0]
        
        # Get assigned reviewer information
        cur.execute("""
            SELECT 
                pda.assignment_id,
                pda.user_id,
                pda.assigned_at,
                u.name as reviewer_name,
                u.email as reviewer_email
            FROM plan_doc_assignment pda
            JOIN users u ON pda.user_id = u.user_id
            WHERE pda.document_id = %s
            ORDER BY pda.assigned_at DESC
            LIMIT 1
        """, (document_id,))
        
        assignment = cur.fetchone()
        cur.close()
        
        if assignment:
            return jsonify({
                "success": True,
                "has_reviewer": True,
                "reviewer": {
                    "assignment_id": assignment[0],
                    "user_id": assignment[1],
                    "assigned_at": assignment[2].isoformat() if assignment[2] else None,
                    "name": assignment[3],
                    "email": assignment[4]
                },
                "document_id": document_id,
                "lru_id": lru_id
            })
        else:
            return jsonify({
                "success": True,
                "has_reviewer": False,
                "reviewer": None,
                "document_id": document_id,
                "lru_id": lru_id
            })
        
    except Exception as e:
        print(f"Error getting assigned reviewer: {str(e)}")
        return jsonify({"success": False, "message": "Internal server error"}), 500

@documents_bp.route('/api/update-reviewer', methods=['PUT'])
def update_reviewer():
    """Update/edit reviewer assignment for a document"""
    try:
        data = request.json
        if not data:
            return jsonify({"success": False, "message": "No data provided"}), 400
        
        # Validate required fields
        lru_name = data.get('lru_name')
        project_name = data.get('project_name')
        new_reviewer_id = data.get('reviewer_id')
        assigned_by = data.get('assigned_by', 1002)  # Default assigned_by
        
        if not all([lru_name, project_name, new_reviewer_id]):
            return jsonify({"success": False, "message": "Missing required fields: lru_name, project_name, reviewer_id"}), 400
        
        conn = get_db_connection()
        cur = conn.cursor()
        
        # Find the LRU ID based on LRU name and project name
        cur.execute("""
            SELECT l.lru_id
            FROM lrus l
            JOIN projects p ON l.project_id = p.project_id
            WHERE l.lru_name = %s AND p.project_name = %s
        """, (lru_name, project_name))
        
        lru_result = cur.fetchone()
        if not lru_result:
            cur.close()
            return jsonify({"success": False, "message": "LRU not found for the specified project"}), 404
        
        lru_id = lru_result[0]
        
        # Find the active document for this LRU
        cur.execute("""
            SELECT document_id
            FROM plan_documents
            WHERE lru_id = %s AND is_active = TRUE
            ORDER BY upload_date DESC
            LIMIT 1
        """, (lru_id,))
        
        doc_result = cur.fetchone()
        if not doc_result:
            cur.close()
            return jsonify({"success": False, "message": "No active document found for this LRU"}), 404
        
        document_id = doc_result[0]
        
        # Check if new reviewer exists and has QA Reviewer role
        cur.execute("""
            SELECT u.user_id 
            FROM users u
            JOIN user_roles ur ON u.user_id = ur.user_id
            WHERE u.user_id = %s AND ur.role_id = 3
        """, (new_reviewer_id,))
        
        if not cur.fetchone():
            cur.close()
            return jsonify({"success": False, "message": "New reviewer not found or not a QA Reviewer"}), 404
        
        # Check if there's an existing assignment to update
        cur.execute("""
            SELECT assignment_id FROM plan_doc_assignment 
            WHERE document_id = %s
            ORDER BY assigned_at DESC
            LIMIT 1
        """, (document_id,))
        
        existing_assignment = cur.fetchone()
        
        if existing_assignment:
            # Update existing assignment
            cur.execute("""
                UPDATE plan_doc_assignment 
                SET user_id = %s, assigned_at = NOW()
                WHERE assignment_id = %s
                RETURNING assignment_id
            """, (new_reviewer_id, existing_assignment[0]))
            
            assignment_id = existing_assignment[0]
        else:
            # Create new assignment if none exists
            cur.execute("""
                INSERT INTO plan_doc_assignment (document_id, user_id, assigned_at)
                VALUES (%s, %s, NOW())
                RETURNING assignment_id
            """, (document_id, new_reviewer_id))
            
            assignment_id = cur.fetchone()[0]
        
        # Update document status to 'assigned'
        cur.execute("""
            UPDATE plan_documents 
            SET status = 'assigned'
            WHERE document_id = %s
        """, (document_id,))
        
        conn.commit()
        cur.close()
        
        return jsonify({
            "success": True,
            "message": "Reviewer updated successfully",
            "assignment_id": assignment_id,
            "document_id": document_id,
            "lru_id": lru_id
        })
        
    except Exception as e:
        return handle_database_error(get_db_connection(), f"Error updating reviewer: {str(e)}")
