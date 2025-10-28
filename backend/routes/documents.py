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
        
        # Check if any document in this LRU is already accepted (final version)
        cur.execute("""
            SELECT document_id, document_number, version
            FROM plan_documents
            WHERE lru_id = %s AND status = 'accepted' AND is_active = TRUE
        """, (lru_id,))
        
        accepted_document = cur.fetchone()
        if accepted_document:
            cur.close()
            return jsonify({
                "success": False, 
                "message": f"Upload restricted. Document {accepted_document[1]} v{accepted_document[2]} has been accepted as the final version for this LRU. No further uploads are allowed."
            }), 400

        # Check for active comments in this LRU/project before allowing upload
        cur.execute("""
            SELECT COUNT(*) 
            FROM document_comments dc
            JOIN plan_documents pd ON dc.document_id = pd.document_id
            WHERE pd.lru_id = %s 
            AND dc.status NOT IN ('accepted', 'rejected')
        """, (lru_id,))
        
        active_comments_count = cur.fetchone()[0]
        if active_comments_count > 0:
            cur.close()
            return jsonify({
                "success": False, 
                "message": f"Upload restricted. There are {active_comments_count} active comment(s) in this project that must be reviewed and accepted before uploading a new document."
            }), 400
        
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
        
        # Send notifications based on version
        from utils.activity_logger import log_notification, get_users_by_role, log_activity
        
        # Get LRU and project info for notification
        cur.execute("""
            SELECT l.lru_name, p.project_name, p.project_id
            FROM lrus l
            JOIN projects p ON l.project_id = p.project_id
            WHERE l.lru_id = %s
        """, (lru_id,))
        
        lru_info = cur.fetchone()
        lru_name = lru_info[0] if lru_info else "Unknown LRU"
        project_name = lru_info[1] if lru_info else "Unknown Project"
        project_id = lru_info[2] if lru_info else None
        
        # Check if this is version A (first version)
        # Check both version and doc_ver fields for version A
        is_version_a = (doc_ver and doc_ver.upper() == 'A') or (version and version.upper() == 'A')
        
        print(f"🔔 Document upload notification check:")
        print(f"   Version field: {version}")
        print(f"   Doc_ver field: {doc_ver}")
        print(f"   Is version A: {is_version_a}")
        
        if is_version_a:
            # Log activity for version A document upload
            log_activity(
                project_id=project_id,
                activity_performed="Document Uploaded (Version A)",
                performed_by=int(uploaded_by),
                additional_info=f"New document '{document_number}' version {version} (doc_ver: {doc_ver}) uploaded for LRU '{lru_name}' in project '{project_name}' by user ID {uploaded_by}."
            )
            
            # Notify QA Head (role_id = 2) when version A is uploaded
            print(f"   Sending notification to QA Heads for version A upload")
            qa_heads = get_users_by_role(2)
            print(f"   Found {len(qa_heads)} QA Head(s)")
            for qa_head in qa_heads:
                log_notification(
                    project_id=project_id,
                    activity_performed="New Document Uploaded (Version A)",
                    performed_by=int(uploaded_by),
                    notified_user_id=qa_head['user_id'],
                    notification_type="document_upload_version_a",
                    additional_info=f"New document '{document_number}' version {version} uploaded for LRU '{lru_name}' in project '{project_name}'. Review required."
                )
                print(f"   ✓ Sent notification to QA Head: {qa_head['name']} (ID: {qa_head['user_id']})")
        else:
            print(f"   Checking for assigned reviewer for LRU {lru_id}")
            # Get the assigned reviewer for this LRU
            cur.execute("""
                SELECT DISTINCT pda.user_id, u.name
                FROM plan_doc_assignment pda
                JOIN plan_documents pd ON pda.document_id = pd.document_id
                JOIN users u ON pda.user_id = u.user_id
                WHERE pd.lru_id = %s
                LIMIT 1
            """, (lru_id,))
            
            reviewer_result = cur.fetchone()
            if reviewer_result:
                reviewer_id = reviewer_result[0]
                reviewer_name = reviewer_result[1]
                
                print(f"   Found assigned reviewer: {reviewer_name} (ID: {reviewer_id})")
                
                # Log activity for new version upload
                log_activity(
                    project_id=project_id,
                    activity_performed=f"Document Version {version} Uploaded",
                    performed_by=int(uploaded_by),
                    additional_info=f"New version '{version}' (doc_ver: {doc_ver}) of document '{document_number}' uploaded for LRU '{lru_name}' in project '{project_name}' by user ID {uploaded_by}. Assigned reviewer: {reviewer_name}."
                )
                
                # Notify the assigned reviewer about the new version
                log_notification(
                    project_id=project_id,
                    activity_performed="New Document Version Uploaded",
                    performed_by=int(uploaded_by),
                    notified_user_id=reviewer_id,
                    notification_type="document_upload_new_version",
                    additional_info=f"New version '{version}' of document '{document_number}' uploaded for LRU '{lru_name}' in project '{project_name}'. Please review."
                )
                print(f"   ✓ Sent notification to reviewer: {reviewer_name}")
            else:
                print(f"   ⚠️ No reviewer assigned for this LRU yet")
                
                # Log activity even when no reviewer is assigned
                log_activity(
                    project_id=project_id,
                    activity_performed=f"Document Version {version} Uploaded",
                    performed_by=int(uploaded_by),
                    additional_info=f"New version '{version}' (doc_ver: {doc_ver}) of document '{document_number}' uploaded for LRU '{lru_name}' in project '{project_name}' by user ID {uploaded_by}. No reviewer assigned yet."
                )
        
        cur.close()
        
        # Auto-assign reviewer if LRU already has a reviewer assigned to other documents
        auto_assign_reviewer_to_new_document(int(lru_id), document_id)
        
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

@documents_bp.route('/api/documents/<int:document_id>/accept', methods=['POST'])
def accept_document(document_id):
    """Accept a document as final version - prevents further uploads"""
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        
        # First verify the document exists and get its LRU
        cur.execute("""
            SELECT pd.document_id, pd.lru_id, pd.document_number, pd.version, 
                   pd.status, l.lru_name, p.project_name
            FROM plan_documents pd
            JOIN lrus l ON pd.lru_id = l.lru_id
            JOIN projects p ON l.project_id = p.project_id
            WHERE pd.document_id = %s AND pd.is_active = TRUE
        """, (document_id,))
        
        document = cur.fetchone()
        if not document:
            cur.close()
            return jsonify({"success": False, "message": "Document not found"}), 404
        
        lru_id = document[1]
        
        # Check if any document in this LRU is already accepted
        cur.execute("""
            SELECT document_id, document_number, version
            FROM plan_documents
            WHERE lru_id = %s AND status = 'accepted' AND is_active = TRUE
        """, (lru_id,))
        
        existing_accepted = cur.fetchone()
        if existing_accepted:
            cur.close()
            return jsonify({
                "success": False, 
                "message": f"Document {existing_accepted[1]} v{existing_accepted[2]} is already accepted as final version for this LRU"
            }), 400
        
        # Update document status to 'accepted'
        cur.execute("""
            UPDATE plan_documents 
            SET status = 'accepted'
            WHERE document_id = %s AND is_active = TRUE
            RETURNING document_id, document_number, version
        """, (document_id,))
        
        result = cur.fetchone()
        if not result:
            cur.close()
            return jsonify({"success": False, "message": "Failed to update document status"}), 500
        
        conn.commit()
        cur.close()
        
        return jsonify({
            "success": True,
            "message": f"Document {result[1]} v{result[2]} has been accepted as the final version",
            "document_id": result[0],
            "document_number": result[1],
            "version": result[2],
            "lru_name": document[5],
            "project_name": document[6]
        })
        
    except Exception as e:
        return handle_database_error(get_db_connection(), f"Error accepting document: {str(e)}")

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
        # cur.execute("""
        #     SELECT MAX(CAST(doc_ver AS INTEGER)) 
        #     FROM plan_documents 
        #     WHERE lru_id = %s
        # """, (lru_id,))
        cur.execute("""
            SELECT MAX(doc_ver)
            FROM plan_documents
            WHERE lru_id = %s
        """, (lru_id,))
       
        result = cur.fetchone()
        cur.close()
        
        # If no documents exist for this LRU, start with 1
        # max_doc_ver = result[0] if result[0] is not None else 0
        # next_doc_ver = max_doc_ver + 1

        current_doc_ver = result[0]

        if current_doc_ver is None:
            next_doc_ver = 'A'
        else:
            # Convert to next alphabet letter
            if current_doc_ver.upper() == 'Z':
                next_doc_ver = 'AA'  # Optionally handle overflow
            else:
                next_doc_ver = chr(ord(current_doc_ver.upper()) + 1)
        
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
        
        # Check if any reviewer is already assigned to this LRU's active document
        # Enforce one reviewer per LRU constraint
        cur.execute("""
            SELECT pda.assignment_id, pda.user_id, u.name as reviewer_name
            FROM plan_doc_assignment pda
            JOIN plan_documents pd ON pda.document_id = pd.document_id
            JOIN users u ON pda.user_id = u.user_id
            WHERE pd.lru_id = %s AND pd.is_active = TRUE
        """, (lru_id,))
        
        existing_assignment = cur.fetchone()
        
        if existing_assignment:
            if existing_assignment[1] == reviewer_id:
                cur.close()
                return jsonify({"success": False, "message": "This reviewer is already assigned to the active document for this LRU"}), 400
            else:
                cur.close()
                return jsonify({
                    "success": False, 
                    "message": f"This LRU is already assigned to another reviewer: {existing_assignment[2]}. Each LRU can only be assigned to one reviewer at a time."
                }), 400
        
        # Insert new assignment for the active document
        cur.execute("""
            INSERT INTO plan_doc_assignment (document_id, user_id, assigned_at)
            VALUES (%s, %s, NOW())
            RETURNING assignment_id
        """, (document_id, reviewer_id))
        
        assignment_id = cur.fetchone()[0]
        
        # Assign the same reviewer to ALL documents in this LRU (not just the active one)
        # This ensures consistency across all versions
        cur.execute("""
            INSERT INTO plan_doc_assignment (document_id, user_id, assigned_at)
            SELECT pd.document_id, %s, NOW()
            FROM plan_documents pd
            WHERE pd.lru_id = %s 
            AND pd.document_id != %s
            AND NOT EXISTS (
                SELECT 1 FROM plan_doc_assignment pda 
                WHERE pda.document_id = pd.document_id
            )
        """, (reviewer_id, lru_id, document_id))
        
        # Update status to 'assigned' for all documents in this LRU
        cur.execute("""
            UPDATE plan_documents 
            SET status = 'assigned'
            WHERE lru_id = %s
        """, (lru_id,))
        
        conn.commit()
        
        # Send notification to the assigned reviewer
        from utils.activity_logger import log_notification, log_activity
        
        # Get project_id, reviewer name, and assigned_by name for notification
        cur.execute("""
            SELECT l.project_id, u.name as reviewer_name
            FROM lrus l
            JOIN users u ON u.user_id = %s
            WHERE l.lru_id = %s
        """, (reviewer_id, lru_id))
        
        project_and_reviewer = cur.fetchone()
        project_id = project_and_reviewer[0] if project_and_reviewer else None
        reviewer_name = project_and_reviewer[1] if project_and_reviewer else "Unknown Reviewer"
        
        # Get who assigned it
        assigned_by_name = "QA Head"  # Default fallback
        if assigned_by:
            cur.execute("SELECT name FROM users WHERE user_id = %s", (assigned_by,))
            assigned_by_result = cur.fetchone()
            if assigned_by_result:
                assigned_by_name = assigned_by_result[0]
        
        # Log activity for reviewer assignment
        log_activity(
            project_id=project_id,
            activity_performed="Reviewer Assigned to Plan Document",
            performed_by=assigned_by,
            additional_info=f"QA Head assigned {reviewer_name} to review plan documents for LRU '{lru_name}' in project '{project_name}'."
        )
        
        # Send notification to the reviewer
        log_notification(
            project_id=project_id,
            activity_performed="Plan Document Assignment",
            performed_by=assigned_by,
            notified_user_id=reviewer_id,
            notification_type="plan_document_assigned",
            additional_info=f"You have been assigned to review plan documents for LRU '{lru_name}' in project '{project_name}' by {assigned_by_name}."
        )
        
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

def auto_assign_reviewer_to_new_document(lru_id, document_id):
    """
    Automatically assign a reviewer to a new document if the LRU already has a reviewer assigned.
    This ensures consistency across all document versions in an LRU.
    """
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        
        # Check if this LRU already has a reviewer assigned to any document
        cur.execute("""
            SELECT DISTINCT pda.user_id
            FROM plan_doc_assignment pda
            JOIN plan_documents pd ON pda.document_id = pd.document_id
            WHERE pd.lru_id = %s
            LIMIT 1
        """, (lru_id,))
        
        existing_reviewer = cur.fetchone()
        
        if existing_reviewer:
            reviewer_id = existing_reviewer[0]
            
            # Check if this specific document already has an assignment
            cur.execute("""
                SELECT assignment_id FROM plan_doc_assignment 
                WHERE document_id = %s
            """, (document_id,))
            
            if not cur.fetchone():
                # Assign the existing reviewer to this new document
                cur.execute("""
                    INSERT INTO plan_doc_assignment (document_id, user_id, assigned_at)
                    VALUES (%s, %s, NOW())
                """, (document_id, reviewer_id))
                
                # Update document status to 'assigned'
                cur.execute("""
                    UPDATE plan_documents 
                    SET status = 'assigned'
                    WHERE document_id = %s
                """, (document_id,))
                
                conn.commit()
                print(f"Auto-assigned reviewer {reviewer_id} to new document {document_id} in LRU {lru_id}")
        
        cur.close()
        return True
        
    except Exception as e:
        print(f"Error in auto-assigning reviewer: {str(e)}")
        return False

@documents_bp.route('/api/test-lru-constraint', methods=['GET'])
def test_lru_constraint():
    """Test endpoint to verify one reviewer per LRU constraint"""
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        
        # Get LRUs with multiple active assignments (should be none after constraint)
        cur.execute("""
            SELECT 
                l.lru_name,
                p.project_name,
                COUNT(DISTINCT pda.user_id) as reviewer_count,
                STRING_AGG(DISTINCT u.name, ', ') as reviewers
            FROM lrus l
            JOIN projects p ON l.project_id = p.project_id
            JOIN plan_documents pd ON l.lru_id = pd.lru_id
            JOIN plan_doc_assignment pda ON pd.document_id = pda.document_id
            JOIN users u ON pda.user_id = u.user_id
            WHERE pd.is_active = TRUE
            GROUP BY l.lru_id, l.lru_name, p.project_name
            HAVING COUNT(DISTINCT pda.user_id) > 1
        """)
        
        violations = cur.fetchall()
        
        # Get all LRU assignments
        cur.execute("""
            SELECT 
                l.lru_name,
                p.project_name,
                u.name as reviewer_name,
                pd.doc_ver,
                pda.assigned_at
            FROM lrus l
            JOIN projects p ON l.project_id = p.project_id
            JOIN plan_documents pd ON l.lru_id = pd.lru_id
            JOIN plan_doc_assignment pda ON pd.document_id = pda.document_id
            JOIN users u ON pda.user_id = u.user_id
            WHERE pd.is_active = TRUE
            ORDER BY l.lru_name, pda.assigned_at DESC
        """)
        
        all_assignments = cur.fetchall()
        cur.close()
        
        # Convert to lists
        violation_list = []
        for violation in violations:
            violation_list.append({
                "lru_name": violation[0],
                "project_name": violation[1],
                "reviewer_count": violation[2],
                "reviewers": violation[3]
            })
        
        assignment_list = []
        for assignment in all_assignments:
            assignment_list.append({
                "lru_name": assignment[0],
                "project_name": assignment[1],
                "reviewer_name": assignment[2],
                "doc_ver": assignment[3],
                "assigned_at": assignment[4].isoformat() if assignment[4] else None
            })
        
        return jsonify({
            "success": True,
            "constraint_violations": violation_list,
            "total_violations": len(violation_list),
            "all_lru_assignments": assignment_list,
            "message": "One reviewer per LRU constraint is enforced" if len(violation_list) == 0 else f"Found {len(violation_list)} constraint violations"
        })
        
    except Exception as e:
        print(f"Error in LRU constraint test: {str(e)}")
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
        
        # Get assigned reviewer information for this LRU (check any document in the LRU)
        # Since we now assign reviewers to ALL documents in an LRU, we can check any document
        cur.execute("""
            SELECT 
                pda.assignment_id,
                pda.user_id,
                pda.assigned_at,
                u.name as reviewer_name,
                u.email as reviewer_email,
                pd.document_id
            FROM plan_doc_assignment pda
            JOIN users u ON pda.user_id = u.user_id
            JOIN plan_documents pd ON pda.document_id = pd.document_id
            WHERE pd.lru_id = %s AND pd.is_active = TRUE
            ORDER BY pda.assigned_at DESC
            LIMIT 1
        """, (lru_id,))
        
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
                "document_id": assignment[5],  # document_id from the query result
                "lru_id": lru_id
            })
        else:
            return jsonify({
                "success": True,
                "has_reviewer": False,
                "reviewer": None,
                "document_id": None,
                "lru_id": lru_id
            })
        
    except Exception as e:
        print(f"Error getting assigned reviewer: {str(e)}")
        return jsonify({"success": False, "message": "Internal server error"}), 500

@documents_bp.route('/api/debug-assignment/<lru_name>/<project_name>', methods=['GET'])
def debug_assignment(lru_name, project_name):
    """Debug endpoint to check assignment status for an LRU"""
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        
        # Find the LRU ID
        cur.execute("""
            SELECT l.lru_id, l.lru_name, p.project_name
            FROM lrus l
            JOIN projects p ON l.project_id = p.project_id
            WHERE l.lru_name = %s AND p.project_name = %s
        """, (lru_name, project_name))
        
        lru_info = cur.fetchone()
        if not lru_info:
            cur.close()
            return jsonify({"success": False, "message": "LRU not found"}), 404
        
        lru_id = lru_info[0]
        
        # Get all documents in this LRU
        cur.execute("""
            SELECT document_id, document_number, status, is_active
            FROM plan_documents
            WHERE lru_id = %s
            ORDER BY upload_date DESC
        """, (lru_id,))
        
        documents = cur.fetchall()
        
        # Get all assignments for this LRU
        cur.execute("""
            SELECT pda.document_id, pda.user_id, u.name, pda.assigned_at
            FROM plan_doc_assignment pda
            JOIN users u ON pda.user_id = u.user_id
            JOIN plan_documents pd ON pda.document_id = pd.document_id
            WHERE pd.lru_id = %s
            ORDER BY pda.assigned_at DESC
        """, (lru_id,))
        
        assignments = cur.fetchall()
        cur.close()
        
        return jsonify({
            "success": True,
            "lru_info": {
                "lru_id": lru_info[0],
                "lru_name": lru_info[1],
                "project_name": lru_info[2]
            },
            "documents": [{"document_id": d[0], "document_number": d[1], "status": d[2], "is_active": d[3]} for d in documents],
            "assignments": [{"document_id": a[0], "user_id": a[1], "reviewer_name": a[2], "assigned_at": a[3].isoformat() if a[3] else None} for a in assignments]
        })
        
    except Exception as e:
        return jsonify({"success": False, "message": f"Debug error: {str(e)}"}), 500

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
        
        # Check if there's an existing assignment for this LRU's active document
        # Enforce one reviewer per LRU constraint
        cur.execute("""
            SELECT pda.assignment_id, pda.user_id, u.name as reviewer_name
            FROM plan_doc_assignment pda
            JOIN plan_documents pd ON pda.document_id = pd.document_id
            JOIN users u ON pda.user_id = u.user_id
            WHERE pd.lru_id = %s AND pd.is_active = TRUE
            ORDER BY pda.assigned_at DESC
            LIMIT 1
        """, (lru_id,))
        
        existing_assignment = cur.fetchone()
        
        if existing_assignment:
            # Update ALL assignments in this LRU to the new reviewer
            cur.execute("""
                UPDATE plan_doc_assignment 
                SET user_id = %s, assigned_at = NOW()
                WHERE document_id IN (
                    SELECT pd.document_id 
                    FROM plan_documents pd 
                    WHERE pd.lru_id = %s
                )
            """, (new_reviewer_id, lru_id))
            
            assignment_id = existing_assignment[0]
        else:
            # Create new assignment for the active document
            cur.execute("""
                INSERT INTO plan_doc_assignment (document_id, user_id, assigned_at)
                VALUES (%s, %s, NOW())
                RETURNING assignment_id
            """, (document_id, new_reviewer_id))
            
            assignment_id = cur.fetchone()[0]
            
            # Assign to all other documents in this LRU as well
            cur.execute("""
                INSERT INTO plan_doc_assignment (document_id, user_id, assigned_at)
                SELECT pd.document_id, %s, NOW()
                FROM plan_documents pd
                WHERE pd.lru_id = %s 
                AND pd.document_id != %s
                AND NOT EXISTS (
                    SELECT 1 FROM plan_doc_assignment pda 
                    WHERE pda.document_id = pd.document_id
                )
            """, (new_reviewer_id, lru_id, document_id))
        
        # Update status to 'assigned' for all documents in this LRU
        cur.execute("""
            UPDATE plan_documents 
            SET status = 'assigned'
            WHERE lru_id = %s
        """, (lru_id,))
        
        conn.commit()
        
        # Send notification to the updated reviewer
        from utils.activity_logger import log_notification, log_activity
        
        # Get project_id, reviewer name, and assigned_by name for notification
        cur.execute("""
            SELECT l.project_id, u.name as reviewer_name
            FROM lrus l
            JOIN users u ON u.user_id = %s
            WHERE l.lru_id = %s
        """, (new_reviewer_id, lru_id))
        
        project_and_reviewer = cur.fetchone()
        project_id = project_and_reviewer[0] if project_and_reviewer else None
        reviewer_name = project_and_reviewer[1] if project_and_reviewer else "Unknown Reviewer"
        
        # Get who assigned it
        assigned_by_name = "QA Head"  # Default fallback
        if assigned_by:
            cur.execute("SELECT name FROM users WHERE user_id = %s", (assigned_by,))
            assigned_by_result = cur.fetchone()
            if assigned_by_result:
                assigned_by_name = assigned_by_result[0]
        
        # Get previous reviewer info if assignment was updated
        previous_reviewer_name = None
        if existing_assignment:
            previous_reviewer_id = existing_assignment[1]
            if previous_reviewer_id != new_reviewer_id:
                cur.execute("SELECT name FROM users WHERE user_id = %s", (previous_reviewer_id,))
                prev_result = cur.fetchone()
                if prev_result:
                    previous_reviewer_name = prev_result[0]
        
        # Log activity for reviewer update
        log_activity(
            project_id=project_id,
            activity_performed="Reviewer Updated for Plan Document",
            performed_by=assigned_by,
            additional_info=f"QA Head updated reviewer assignment to {reviewer_name} for plan documents in LRU '{lru_name}' in project '{project_name}'."
        )
        
        # Send notification to the new reviewer
        log_notification(
            project_id=project_id,
            activity_performed="Plan Document Assignment Updated",
            performed_by=assigned_by,
            notified_user_id=new_reviewer_id,
            notification_type="plan_document_assigned",
            additional_info=f"You have been assigned to review plan documents for LRU '{lru_name}' in project '{project_name}' by {assigned_by_name}."
        )
        
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

@documents_bp.route('/api/plan-documents/<int:document_id>', methods=['DELETE'])
def delete_plan_document(document_id):
    """Delete a plan document and all its associated comments"""
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        
        # First, get the document details for confirmation
        cur.execute("""
            SELECT document_id, document_number, version, file_path, lru_id
            FROM plan_documents 
            WHERE document_id = %s AND is_active = TRUE
        """, (document_id,))
        
        document = cur.fetchone()
        if not document:
            cur.close()
            return jsonify({"success": False, "message": "Document not found"}), 404
        
        # Delete all comments associated with this document
        cur.execute("DELETE FROM document_comments WHERE document_id = %s", (document_id,))
        comments_deleted = cur.rowcount
        
        # Delete all annotations associated with this document
        cur.execute("""
            DELETE FROM document_annotations 
            WHERE document_id = %s
        """, (document_id,))
        annotations_deleted = cur.rowcount
        
        # Delete the document record
        cur.execute("DELETE FROM plan_documents WHERE document_id = %s", (document_id,))
        if cur.rowcount == 0:
            cur.close()
            return jsonify({"success": False, "message": "Document not found"}), 404
        
        # Delete the physical file if it exists
        file_path = document[3]  # file_path is the 4th column
        if file_path and os.path.exists(file_path):
            try:
                os.remove(file_path)
            except Exception as e:
                print(f"Warning: Could not delete file {file_path}: {str(e)}")
        
        conn.commit()
        cur.close()
        
        return jsonify({
            "success": True,
            "message": f"Document deleted successfully. Removed {comments_deleted} comments and {annotations_deleted} annotations.",
            "deleted_comments": comments_deleted,
            "deleted_annotations": annotations_deleted
        })
        
    except Exception as e:
        return handle_database_error(get_db_connection(), f"Error deleting plan document: {str(e)}")
