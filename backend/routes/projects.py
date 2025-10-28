"""
Project and LRU management routes
"""
from flask import Blueprint, request, jsonify, Response
from config import get_db_connection
from utils.helpers import handle_database_error
from utils.activity_logger import log_activity
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.units import inch
from datetime import datetime
import io

projects_bp = Blueprint('projects', __name__)

@projects_bp.route('/api/projects', methods=['GET'])
def get_projects():
    """Get all projects"""
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        
        # Fetch all projects from the projects table
        cur.execute("""
            SELECT project_id, project_name, created_at
            FROM projects
            ORDER BY project_id
        """)
        
        projects = cur.fetchall()
        cur.close()
        
        # Convert to list of dictionaries
        project_list = []
        for project in projects:
            project_list.append({
                "id": project[0],
                "name": project[1],
                "created_at": project[2].isoformat() if project[2] else None
            })
        
        return jsonify({
            "success": True,
            "projects": project_list
        })
        
    except Exception as e:
        print(f"Error fetching projects: {str(e)}")
        return jsonify({"success": False, "message": "Internal server error"}), 500

@projects_bp.route('/api/projects/<int:project_id>/lrus', methods=['GET'])
def get_project_lrus(project_id):
    """Get LRUs for a specific project"""
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
        
        # Fetch LRUs for the specific project
        cur.execute("""
            SELECT l.lru_id, l.lru_name, l.created_at
            FROM lrus l
            WHERE l.project_id = %s
            ORDER BY l.lru_id
        """, (project_id,))
        
        lrus = cur.fetchall()
        cur.close()
        
        # Convert to list of dictionaries
        lru_list = []
        for lru in lrus:
            lru_list.append({
                "id": lru[0],
                "name": lru[1],
                "created_at": lru[2].isoformat() if lru[2] else None
            })
        
        return jsonify({
            "success": True,
            "project": {
                "id": project[0],
                "name": project[1]
            },
            "lrus": lru_list
        })
        
    except Exception as e:
        print(f"Error fetching LRUs for project {project_id}: {str(e)}")
        return jsonify({"success": False, "message": "Internal server error"}), 500

@projects_bp.route('/api/projects', methods=['POST'])
def create_project():
    """Create a new project"""
    try:
        data = request.json
        if not data:
            return jsonify({"success": False, "message": "No data provided"}), 400
        
        # Validate required fields
        project_name = data.get('name')
        project_number = data.get('number')
        project_date = data.get('date')
        lrus = data.get('lrus', [])
        created_by = data.get('createdBy')
        
        if not project_name or not project_number or not project_date:
            return jsonify({"success": False, "message": "Project name, number, and date are required"}), 400
        
        if not created_by:
            return jsonify({"success": False, "message": "User authentication required"}), 400
        
        if not lrus or len(lrus) == 0:
            return jsonify({"success": False, "message": "At least one LRU is required"}), 400
        
        # Validate LRUs and serial quantities
        for i, lru in enumerate(lrus):
            if not lru.get('name'):
                return jsonify({"success": False, "message": f"LRU {i+1} name is required"}), 400
            
            serial_quantity = lru.get('serialQuantity')
            if not serial_quantity or not isinstance(serial_quantity, int) or serial_quantity < 1:
                return jsonify({"success": False, "message": f"Valid serial quantity is required for LRU '{lru['name']}'"}), 400
        
        conn = get_db_connection()
        cur = conn.cursor()
        
        # Insert project data as specified
        cur.execute("""
            INSERT INTO projects (project_name, project_id, project_date, created_by)
            VALUES (%s, %s, %s, %s)
            RETURNING project_id
        """, (project_name, project_number, project_date, created_by))
        
        project_id = cur.fetchone()[0]
        
        # Insert LRUs with project number as project_id
        for lru in lrus:
            # Insert LRU with project number as project_id
            cur.execute("""
                INSERT INTO lrus (project_id, lru_name)
                VALUES (%s, %s)
                RETURNING lru_id
            """, (project_number, lru['name']))
            
            lru_id = cur.fetchone()[0]
            
            # Insert multiple serial numbers based on quantity
            serial_quantity = lru['serialQuantity']
            for i in range(1, serial_quantity + 1):
                cur.execute("""
                    INSERT INTO serial_numbers (lru_id, serial_number)
                    VALUES (%s, %s)
                """, (lru_id, i))
        
        conn.commit()
        cur.close()
        
        # Log the project creation activity
        log_activity(
            project_id=project_id,
            activity_performed="Project Added",
            performed_by=created_by,
            additional_info=f"ID:{project_id}|Name:{project_name}|Project '{project_name}' created with {len(lrus)} LRUs"
        )
        
        # Send notifications to Design Head and QA Head
        from utils.activity_logger import log_notification, get_users_by_role
        
        # Get Design Head users (role_id = 4)
        design_heads = get_users_by_role(4)
        for design_head in design_heads:
            log_notification(
                project_id=project_id,
                activity_performed="New Project Created",
                performed_by=created_by,
                notified_user_id=design_head['user_id'],
                notification_type="project_created",
                additional_info=f"New project '{project_name}' (ID: {project_id}) has been created and requires your attention."
            )
        
        # Get QA Head users (role_id = 2)
        qa_heads = get_users_by_role(2)
        for qa_head in qa_heads:
            log_notification(
                project_id=project_id,
                activity_performed="New Project Created",
                performed_by=created_by,
                notified_user_id=qa_head['user_id'],
                notification_type="project_created",
                additional_info=f"New project '{project_name}' (ID: {project_id}) has been created and requires your attention."
            )
        
        return jsonify({
            "success": True,
            "message": "Project created successfully",
            "project_id": project_id
        })
        
    except Exception as e:
        return handle_database_error(get_db_connection(), f"Error creating project: {str(e)}")

@projects_bp.route('/api/projects/<int:project_id>', methods=['PUT'])
def update_project(project_id):
    """Update an existing project"""
    try:
        data = request.json
        if not data:
            return jsonify({"success": False, "message": "No data provided"}), 400
        
        conn = get_db_connection()
        cur = conn.cursor()
        
        # Check if project exists
        cur.execute("SELECT project_id, project_name FROM projects WHERE project_id = %s", (project_id,))
        existing_project = cur.fetchone()
        
        if not existing_project:
            cur.close()
            return jsonify({"success": False, "message": "Project not found"}), 404
        
        # Update project basic info
        update_fields = []
        update_values = []
        
        if 'name' in data and data['name']:
            update_fields.append("project_name = %s")
            update_values.append(data['name'])
            
        if 'date' in data and data['date']:
            update_fields.append("project_date = %s")
            update_values.append(data['date'])
        
        # Update project table if there are fields to update
        if update_fields:
            update_values.append(project_id)
            update_query = f"UPDATE projects SET {', '.join(update_fields)} WHERE project_id = %s"
            cur.execute(update_query, update_values)
        
        # Handle LRUs updates
        if 'lrus' in data:
            existing_lru_ids = []
            
            # Process each LRU
            for lru_data in data['lrus']:
                if 'lru_id' in lru_data and lru_data['lru_id']:
                    # Update existing LRU
                    lru_id = lru_data['lru_id']
                    existing_lru_ids.append(lru_id)
                    
                    if 'lru_name' in lru_data:
                        cur.execute("""
                            UPDATE lrus SET lru_name = %s WHERE lru_id = %s
                        """, (lru_data['lru_name'], lru_id))
                        
                else:
                    # Create new LRU
                    if lru_data.get('lru_name') and lru_data.get('serialQuantity'):
                        cur.execute("""
                            INSERT INTO lrus (project_id, lru_name)
                            VALUES (%s, %s)
                            RETURNING lru_id
                        """, (project_id, lru_data['lru_name']))
                        
                        new_lru_id = cur.fetchone()[0]
                        existing_lru_ids.append(new_lru_id)
                        
                        # Add serial numbers for new LRU
                        serial_quantity = lru_data['serialQuantity']
                        for i in range(1, serial_quantity + 1):
                            cur.execute("""
                                INSERT INTO serial_numbers (lru_id, serial_number)
                                VALUES (%s, %s)
                            """, (new_lru_id, i))
            
            # Remove LRUs that are no longer in the list (if any were removed)
            if existing_lru_ids:
                placeholders = ','.join(['%s'] * len(existing_lru_ids))
                cur.execute(f"""
                    DELETE FROM serial_numbers 
                    WHERE lru_id IN (
                        SELECT lru_id FROM lrus 
                        WHERE project_id = %s AND lru_id NOT IN ({placeholders})
                    )
                """, [project_id] + existing_lru_ids)
                
                cur.execute(f"""
                    DELETE FROM lrus 
                    WHERE project_id = %s AND lru_id NOT IN ({placeholders})
                """, [project_id] + existing_lru_ids)
        
        conn.commit()
        cur.close()
        
        # Log the project update activity
        # Get the user who performed the update from request data
        updated_by = data.get('updatedBy', existing_project[1])  # Default to project name if no user specified
        
        # For now, we'll use a default user ID since the frontend might not send updatedBy
        # In a real implementation, you'd get this from the authenticated user session
        log_activity(
            project_id=project_id,
            activity_performed="Project Updated",
            performed_by=updated_by if isinstance(updated_by, int) else 1002,  # Default to admin user
            additional_info=f"ID:{project_id}|Name:{existing_project[1]}|Project '{existing_project[1]}' was updated"
        )
        
        return jsonify({
            "success": True,
            "message": "Project updated successfully"
        })
        
    except Exception as e:
        return handle_database_error(get_db_connection(), f"Error updating project: {str(e)}")

@projects_bp.route('/api/projects/<int:project_id>', methods=['GET'])
def get_project(project_id):
    """Get single project with details"""
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        
        # Fetch project with LRUs and serial numbers
        cur.execute("""
            SELECT 
                p.project_id,
                p.project_name,
                p.project_date,
                p.created_at,
                l.lru_id,
                l.lru_name,
                s.serial_id,
                s.serial_number
            FROM projects p
            LEFT JOIN lrus l ON p.project_id = l.project_id
            LEFT JOIN serial_numbers s ON l.lru_id = s.lru_id
            WHERE p.project_id = %s
            ORDER BY l.lru_id, s.serial_number
        """, (project_id,))
        
        results = cur.fetchall()
        cur.close()
        
        if not results or not results[0][0]:
            return jsonify({"success": False, "message": "Project not found"}), 404
        
        # Organize data
        project_info = {
            "project_id": results[0][0],
            "project_name": results[0][1],
            "project_date": results[0][2].isoformat() if results[0][2] else None,
            "created_at": results[0][3].isoformat() if results[0][3] else None,
            "lrus": {}
        }
        
        for row in results:
            if row[4]:  # lru_id exists
                lru_id = row[4]
                if lru_id not in project_info["lrus"]:
                    project_info["lrus"][lru_id] = {
                        "lru_id": lru_id,
                        "lru_name": row[5],
                        "serial_numbers": []
                    }
                
                if row[6]:  # serial_id exists
                    project_info["lrus"][lru_id]["serial_numbers"].append({
                        "serial_id": row[6],
                        "serial_number": row[7]
                    })
        
        # Convert lrus dict to list
        project_info["lrus"] = list(project_info["lrus"].values())
        
        return jsonify({
            "success": True,
            "project": project_info
        })
        
    except Exception as e:
        print(f"Error fetching project: {str(e)}")
        return jsonify({"success": False, "message": "Internal server error"}), 500

@projects_bp.route('/api/projects/manage', methods=['GET'])
def get_projects_with_details():
    """Get projects with LRUs and serial numbers for management"""
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        
        # Fetch all projects with their LRUs and serial numbers
        cur.execute("""
            SELECT 
                p.project_id,
                p.project_name,
                l.lru_id,
                l.lru_name,
                s.serial_id,
                s.serial_number
            FROM projects p
            LEFT JOIN lrus l ON p.project_id = l.project_id
            LEFT JOIN serial_numbers s ON l.lru_id = s.lru_id
            ORDER BY p.project_id, l.lru_id, s.serial_number
        """)
        
        results = cur.fetchall()
        cur.close()
        
        # Organize data hierarchically
        projects_dict = {}
        
        for row in results:
            project_id = row[0]
            project_name = row[1]
            lru_id = row[2]
            lru_name = row[3]
            serial_id = row[4]
            serial_number = row[5]
            
            # Initialize project if not exists
            if project_id not in projects_dict:
                projects_dict[project_id] = {
                    "project_id": project_id,
                    "project_name": project_name,
                    "lrus": {}
                }
            
            # Add LRU if it exists and not already added
            if lru_id and lru_id not in projects_dict[project_id]["lrus"]:
                projects_dict[project_id]["lrus"][lru_id] = {
                    "lru_id": lru_id,
                    "lru_name": lru_name,
                    "serial_numbers": []
                }
            
            # Add serial number if it exists
            if serial_id and lru_id:
                projects_dict[project_id]["lrus"][lru_id]["serial_numbers"].append({
                    "serial_id": serial_id,
                    "serial_number": serial_number
                })
        
        # Convert to list format for frontend
        projects_list = []
        for project_id, project_data in projects_dict.items():
            project = {
                "project_id": project_data["project_id"],
                "project_name": project_data["project_name"],
                "lrus": list(project_data["lrus"].values())
            }
            projects_list.append(project)
        
        return jsonify({
            "success": True,
            "projects": projects_list
        })
        
    except Exception as e:
        print(f"Error fetching projects with details: {str(e)}")
        return jsonify({"success": False, "message": "Internal server error"}), 500

@projects_bp.route('/api/project-options', methods=['GET'])
def get_project_options():
    """Get project name and project number for assign reviewer form"""
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        
        # Fetch project name and project number from projects table
        cur.execute("""
            SELECT project_name, project_id
            FROM projects
            ORDER BY project_name
        """)
        
        projects = cur.fetchall()
        cur.close()
        
        # Convert to list of dictionaries
        project_options = []
        for project in projects:
            project_options.append({
                "project_name": project[0],
                "project_id": project[1]
            })
        
        return jsonify({
            "success": True,
            "project_options": project_options
        })
        
    except Exception as e:
        print(f"Error fetching project options: {str(e)}")
        return jsonify({"success": False, "message": "Internal server error"}), 500

@projects_bp.route('/api/lru-options', methods=['GET'])
def get_lru_options():
    """Get LRU names for assign reviewer form"""
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        
        # Fetch LRU names from lrus table
        cur.execute("""
            SELECT l.lru_name, l.project_id, p.project_name
            FROM lrus l
            JOIN projects p ON l.project_id = p.project_id
            ORDER BY l.lru_name
        """)
        
        lrus = cur.fetchall()
        cur.close()
        
        # Convert to list of dictionaries
        lru_options = []
        for lru in lrus:
            lru_options.append({
                "lru_name": lru[0],
                "project_id": lru[1],
                "project_name": lru[2]
            })
        
        return jsonify({
            "success": True,
            "lru_options": lru_options
        })
        
    except Exception as e:
        print(f"Error fetching LRU options: {str(e)}")
        return jsonify({"success": False, "message": "Internal server error"}), 500

@projects_bp.route('/api/reviewer/<int:reviewer_id>/assigned-projects', methods=['GET'])
def get_reviewer_assigned_projects(reviewer_id):
    """Get projects that contain LRUs with plan documents assigned to a specific reviewer"""
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        
        # Get projects that have LRUs with plan documents assigned to this reviewer
        cur.execute("""
            SELECT DISTINCT p.project_id, p.project_name, p.created_at
            FROM projects p
            JOIN lrus l ON p.project_id = l.project_id
            JOIN plan_documents pd ON l.lru_id = pd.lru_id
            JOIN plan_doc_assignment pda ON pd.document_id = pda.document_id
            WHERE pda.user_id = %s AND pd.is_active = TRUE
            ORDER BY p.project_name
        """, (reviewer_id,))
        
        projects = cur.fetchall()
        cur.close()
        
        # Convert to list of dictionaries
        project_list = []
        for project in projects:
            project_list.append({
                "id": project[0],
                "name": project[1],
                "created_at": project[2].isoformat() if project[2] else None
            })
        
        return jsonify({
            "success": True,
            "projects": project_list
        })
        
    except Exception as e:
        print(f"Error fetching assigned projects for reviewer {reviewer_id}: {str(e)}")
        return jsonify({"success": False, "message": "Internal server error"}), 500

@projects_bp.route('/api/reviewer/<int:reviewer_id>/assigned-lrus/<int:project_id>', methods=['GET'])
def get_reviewer_assigned_lrus_in_project(reviewer_id, project_id):
    """Get LRUs in a specific project that have plan documents assigned to a specific reviewer"""
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
        
        # Get LRUs in this project that have plan documents assigned to this reviewer
        cur.execute("""
            SELECT DISTINCT l.lru_id, l.lru_name, l.created_at
            FROM lrus l
            JOIN plan_documents pd ON l.lru_id = pd.lru_id
            JOIN plan_doc_assignment pda ON pd.document_id = pda.document_id
            WHERE l.project_id = %s AND pda.user_id = %s AND pd.is_active = TRUE
            ORDER BY l.lru_name
        """, (project_id, reviewer_id))
        
        lrus = cur.fetchall()
        cur.close()
        
        # Convert to list of dictionaries
        lru_list = []
        for lru in lrus:
            lru_list.append({
                "id": lru[0],
                "name": lru[1],
                "created_at": lru[2].isoformat() if lru[2] else None
            })
        
        return jsonify({
            "success": True,
            "project": {
                "id": project[0],
                "name": project[1]
            },
            "lrus": lru_list
        })
        
    except Exception as e:
        print(f"Error fetching assigned LRUs for reviewer {reviewer_id} in project {project_id}: {str(e)}")
        return jsonify({"success": False, "message": "Internal server error"}), 500

@projects_bp.route('/api/test-reviewer-assignments', methods=['GET'])
def test_reviewer_assignments():
    """Test endpoint to view all reviewer assignments and check our filtering logic"""
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        
        # Show all current assignments with full details
        cur.execute("""
            SELECT 
                pda.assignment_id,
                pda.user_id,
                u.name as reviewer_name,
                u.email as reviewer_email,
                p.project_id,
                p.project_name,
                l.lru_id,
                l.lru_name,
                pd.document_id,
                pd.document_number,
                pd.status,
                pda.assigned_at
            FROM plan_doc_assignment pda
            JOIN users u ON pda.user_id = u.user_id
            JOIN plan_documents pd ON pda.document_id = pd.document_id
            JOIN lrus l ON pd.lru_id = l.lru_id
            JOIN projects p ON l.project_id = p.project_id
            WHERE pd.is_active = TRUE
            ORDER BY pda.assigned_at DESC
        """)
        
        assignments = cur.fetchall()
        cur.close()
        
        # Convert to list of dictionaries
        assignment_list = []
        for assignment in assignments:
            assignment_list.append({
                "assignment_id": assignment[0],
                "user_id": assignment[1],
                "reviewer_name": assignment[2],
                "reviewer_email": assignment[3],
                "project_id": assignment[4],
                "project_name": assignment[5],
                "lru_id": assignment[6],
                "lru_name": assignment[7],
                "document_id": assignment[8],
                "document_number": assignment[9],
                "status": assignment[10],
                "assigned_at": assignment[11].isoformat() if assignment[11] else None
            })
        
        return jsonify({
            "success": True,
            "message": "All active reviewer assignments",
            "total_assignments": len(assignment_list),
            "assignments": assignment_list
        })
        
    except Exception as e:
        print(f"Error fetching test assignments: {str(e)}")
        return jsonify({"success": False, "message": "Internal server error"}), 500

@projects_bp.route('/api/designer/<int:designer_id>/assigned-projects', methods=['GET'])
def get_designer_assigned_projects(designer_id):
    """Get projects that are assigned to a specific designer"""
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        
        # Get projects assigned to this designer via project_users table
        cur.execute("""
            SELECT DISTINCT p.project_id, p.project_name, p.created_at
            FROM projects p
            JOIN project_users pu ON p.project_id = pu.project_id
            WHERE pu.user_id = %s
            ORDER BY p.project_name
        """, (designer_id,))
        
        projects = cur.fetchall()
        cur.close()
        
        # Convert to list of dictionaries
        project_list = []
        for project in projects:
            project_list.append({
                "id": project[0],
                "name": project[1],
                "created_at": project[2].isoformat() if project[2] else None
            })
        
        return jsonify({
            "success": True,
            "projects": project_list
        })
        
    except Exception as e:
        print(f"Error fetching assigned projects for designer {designer_id}: {str(e)}")
        return jsonify({"success": False, "message": "Internal server error"}), 500

@projects_bp.route('/api/designer/<int:designer_id>/assigned-lrus/<int:project_id>', methods=['GET'])
def get_designer_assigned_lrus_in_project(designer_id, project_id):
    """Get all LRUs in a project that is assigned to a specific designer"""
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        
        # First verify the project exists and is assigned to this designer
        cur.execute("""
            SELECT p.project_id, p.project_name
            FROM projects p
            JOIN project_users pu ON p.project_id = pu.project_id
            WHERE p.project_id = %s AND pu.user_id = %s
        """, (project_id, designer_id))
        
        project = cur.fetchone()
        if not project:
            cur.close()
            return jsonify({"success": False, "message": "Project not found or not assigned to this designer"}), 404
        
        # Get all LRUs in this project (designers see all LRUs in assigned projects)
        cur.execute("""
            SELECT l.lru_id, l.lru_name, l.created_at
            FROM lrus l
            WHERE l.project_id = %s
            ORDER BY l.lru_name
        """, (project_id,))
        
        lrus = cur.fetchall()
        cur.close()
        
        # Convert to list of dictionaries
        lru_list = []
        for lru in lrus:
            lru_list.append({
                "id": lru[0],
                "name": lru[1],
                "created_at": lru[2].isoformat() if lru[2] else None
            })
        
        return jsonify({
            "success": True,
            "project": {
                "id": project[0],
                "name": project[1]
            },
            "lrus": lru_list
        })
        
    except Exception as e:
        print(f"Error fetching assigned LRUs for designer {designer_id} in project {project_id}: {str(e)}")
        return jsonify({"success": False, "message": "Internal server error"}), 500

@projects_bp.route('/api/lrus-filtered', methods=['GET'])
def get_filtered_lrus():
    """Get LRUs filtered by user role and assigned projects"""
    try:
        # Get user_id and user_role from query parameters
        user_id = request.args.get('user_id', type=int)
        user_role = request.args.get('user_role', type=int)
        
        if not user_id or not user_role:
            return jsonify({"success": False, "message": "user_id and user_role are required"}), 400
        
        conn = get_db_connection()
        cur = conn.cursor()
        
        if user_role == 4:  # Design Head - see all LRUs
            cur.execute("""
                SELECT l.lru_id, l.lru_name, p.project_name, l.created_at
                FROM lrus l
                JOIN projects p ON l.project_id = p.project_id
                ORDER BY p.project_name, l.lru_name
            """)
        elif user_role == 5:  # Designer - see only LRUs from assigned projects
            cur.execute("""
                SELECT DISTINCT l.lru_id, l.lru_name, p.project_name, l.created_at
                FROM lrus l
                JOIN projects p ON l.project_id = p.project_id
                JOIN project_users pu ON p.project_id = pu.project_id
                WHERE pu.user_id = %s
                ORDER BY p.project_name, l.lru_name
            """, (user_id,))
        else:
            # Other roles - return empty list (they shouldn't be submitting memos)
            cur.close()
            return jsonify({
                "success": True,
                "lrus": [],
                "message": "No LRUs available for this role"
            })
        
        lrus = cur.fetchall()
        cur.close()
        
        # Convert to list of dictionaries
        lru_list = []
        for lru in lrus:
            lru_list.append({
                "lru_id": lru[0],
                "lru_name": lru[1],
                "project_name": lru[2],
                "created_at": lru[3].isoformat() if lru[3] else None
            })
        
        return jsonify({
            "success": True,
            "lrus": lru_list
        })
        
    except Exception as e:
        print(f"Error fetching filtered LRUs: {str(e)}")
        return jsonify({"success": False, "message": "Internal server error"}), 500

@projects_bp.route('/api/lru-names', methods=['GET'])
def get_all_lru_names():
    """Get all LRU names from the lrus table"""
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        
        # Fetch all unique LRU names from the lrus table
        cur.execute("""
            SELECT DISTINCT lru_name
            FROM lrus
            ORDER BY lru_name
        """)
        
        lrus = cur.fetchall()
        cur.close()
        
        # Convert to simple list of LRU names
        lru_names = [lru[0] for lru in lrus]
        
        return jsonify({
            "success": True,
            "lru_names": lru_names
        })
        
    except Exception as e:
        print(f"Error fetching LRU names: {str(e)}")
        return jsonify({"success": False, "message": "Internal server error"}), 500

@projects_bp.route('/api/lrus', methods=['GET'])
def get_all_lrus():
    """Get all LRUs with detailed information from the lrus table"""
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        
        # Fetch all LRUs with project information
        cur.execute("""
            SELECT 
                l.lru_id,
                l.lru_name,
                l.project_id,
                p.project_name,
                l.created_at
            FROM lrus l
            JOIN projects p ON l.project_id = p.project_id
            ORDER BY l.lru_name
        """)
        
        lrus = cur.fetchall()
        cur.close()
        
        # Convert to list of dictionaries
        lru_list = []
        for lru in lrus:
            lru_list.append({
                "lru_id": lru[0],
                "lru_name": lru[1],
                "project_id": lru[2],
                "project_name": lru[3],
                "created_at": lru[4].isoformat() if lru[4] else None
            })
        
        return jsonify({
            "success": True,
            "lrus": lru_list
        })
        
    except Exception as e:
        print(f"Error fetching LRUs: {str(e)}")
        return jsonify({"success": False, "message": "Internal server error"}), 500

@projects_bp.route('/api/lrus/<int:lru_id>/serial-numbers', methods=['GET'])
def get_lru_serial_numbers(lru_id):
    """Get serial numbers for a specific LRU"""
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
        
        # Fetch serial numbers for the LRU
        cur.execute("""
            SELECT serial_id, serial_number
            FROM serial_numbers
            WHERE lru_id = %s
            ORDER BY serial_number
        """, (lru_id,))
        
        serials = cur.fetchall()
        cur.close()
        
        # Convert to list of dictionaries
        serial_list = []
        for serial in serials:
            serial_list.append({
                "serial_id": serial[0],
                "serial_number": serial[1]
            })
        
        return jsonify({
            "success": True,
            "lru": {
                "lru_id": lru[0],
                "lru_name": lru[1],
                "project_name": lru[2]
            },
            "serial_numbers": serial_list
        })
        
    except Exception as e:
        print(f"Error fetching serial numbers for LRU {lru_id}: {str(e)}")
        return jsonify({"success": False, "message": "Internal server error"}), 500

@projects_bp.route('/api/test-designer-assignments', methods=['GET'])
def test_designer_assignments():
    """Test endpoint to view all designer-project assignments"""
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        
        # Show all current designer assignments with full details
        cur.execute("""
            SELECT 
                pu.project_user_id,
                pu.user_id,
                u.name as designer_name,
                u.email as designer_email,
                p.project_id,
                p.project_name,
                pu.assigned_at,
                r.role_name
            FROM project_users pu
            JOIN users u ON pu.user_id = u.user_id
            JOIN projects p ON pu.project_id = p.project_id
            JOIN user_roles ur ON u.user_id = ur.user_id
            JOIN roles r ON ur.role_id = r.role_id
            WHERE ur.role_id = 5  -- Designer role
            ORDER BY pu.assigned_at DESC
        """)
        
        assignments = cur.fetchall()
        cur.close()
        
        # Convert to list of dictionaries
        assignment_list = []
        for assignment in assignments:
            assignment_list.append({
                "project_user_id": assignment[0],
                "user_id": assignment[1],
                "designer_name": assignment[2],
                "designer_email": assignment[3],
                "project_id": assignment[4],
                "project_name": assignment[5],
                "assigned_at": assignment[6].isoformat() if assignment[6] else None,
                "role_name": assignment[7]
            })
        
        return jsonify({
            "success": True,
            "message": "All designer-project assignments",
            "total_assignments": len(assignment_list),
            "assignments": assignment_list
        })
        
    except Exception as e:
        print(f"Error fetching test designer assignments: {str(e)}")
        return jsonify({"success": False, "message": "Internal server error"}), 500

@projects_bp.route('/api/lrus/<int:lru_id>/metadata', methods=['GET'])
def get_lru_metadata(lru_id):
    """Get LRU and associated project metadata"""
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        
        cur.execute("""
            SELECT l.lru_id, l.lru_name, l.project_id,
                   p.project_name
            FROM lrus l
            LEFT JOIN projects p ON l.project_id = p.project_id
            WHERE l.lru_id = %s
        """, (lru_id,))
        
        result = cur.fetchone()
        cur.close()
        
        if not result:
            return jsonify({"success": False, "message": "LRU not found"}), 404
        
        return jsonify({
            "success": True,
            "lru": {
                "lru_id": result[0],
                "lru_name": result[1],
                "project_id": result[2],
                "project_name": result[3]
            }
        })
        
    except Exception as e:
        print(f"Error getting LRU metadata for {lru_id}: {str(e)}")
        # Rollback the transaction to clear the error state
        try:
            get_db_connection().rollback()
        except:
            pass
        return jsonify({"success": False, "message": "Internal server error"}), 500

@projects_bp.route('/api/projects/<int:project_id>/members', methods=['GET'])
def get_project_members(project_id):
    """Get all members assigned to a specific project"""
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        
        # Verify project exists
        cur.execute("""
            SELECT project_id, project_name FROM projects WHERE project_id = %s
        """, (project_id,))
        
        project = cur.fetchone()
        if not project:
            cur.close()
            return jsonify({"success": False, "message": "Project not found"}), 404
        
        # Get all members assigned to this project
        cur.execute("""
            SELECT 
                pu.project_user_id,
                pu.user_id,
                u.name,
                pu.assigned_at
            FROM project_users pu
            JOIN users u ON pu.user_id = u.user_id
            WHERE pu.project_id = %s
            ORDER BY pu.assigned_at
        """, (project_id,))
        
        members = cur.fetchall()
        cur.close()
        
        # Convert to list of dictionaries
        member_list = []
        for member in members:
            member_list.append({
                "project_user_id": member[0],
                "user_id": member[1],
                "user_name": member[2],
                "assigned_at": member[3].isoformat() if member[3] else None
            })
        
        return jsonify({
            "success": True,
            "project": {
                "project_id": project[0],
                "project_name": project[1]
            },
            "members": member_list
        })
        
    except Exception as e:
        print(f"Error fetching project members for project {project_id}: {str(e)}")
        return jsonify({"success": False, "message": "Internal server error"}), 500

@projects_bp.route('/api/projects/<int:project_id>/members', methods=['POST'])
def add_project_member(project_id):
    """Add a member to a project"""
    try:
        data = request.json
        if not data:
            return jsonify({"success": False, "message": "No data provided"}), 400
        
        user_id = data.get('user_id')
        assigned_by = data.get('assigned_by')  # Get who assigned this project
        
        if not user_id:
            return jsonify({"success": False, "message": "User ID is required"}), 400
        
        conn = get_db_connection()
        cur = conn.cursor()
        
        # Check if project exists and get project name
        cur.execute("SELECT project_id, project_name FROM projects WHERE project_id = %s", (project_id,))
        project_result = cur.fetchone()
        if not project_result:
            cur.close()
            return jsonify({"success": False, "message": "Project not found"}), 404
        
        project_name = project_result[1]
        
        # Check if user exists
        cur.execute("SELECT user_id FROM users WHERE user_id = %s", (user_id,))
        if not cur.fetchone():
            cur.close()
            return jsonify({"success": False, "message": "User not found"}), 404
        
        # Check if user is already assigned to this project
        cur.execute("""
            SELECT project_user_id FROM project_users 
            WHERE project_id = %s AND user_id = %s
        """, (project_id, user_id))
        
        if cur.fetchone():
            cur.close()
            return jsonify({"success": False, "message": "User is already assigned to this project"}), 400
        
        # Add user to project
        cur.execute("""
            INSERT INTO project_users (project_id, user_id)
            VALUES (%s, %s)
            RETURNING project_user_id
        """, (project_id, user_id))
        
        project_user_id = cur.fetchone()[0]
        conn.commit()
        
        # Send notification to the designer
        from utils.activity_logger import log_notification
        
        # Get the name of who assigned the project
        assigned_by_name = 'Design Head'  # Default fallback
        if assigned_by:
            cur.execute("SELECT name FROM users WHERE user_id = %s", (assigned_by,))
            user_result = cur.fetchone()
            if user_result:
                assigned_by_name = user_result[0]
        else:
            # Try to get the first Design Head user as fallback
            cur.execute("""
                SELECT u.name FROM users u
                JOIN user_roles ur ON u.user_id = ur.user_id
                WHERE ur.role_id = 4
                LIMIT 1
            """)
            design_head_result = cur.fetchone()
            if design_head_result:
                assigned_by_name = design_head_result[0]
        
        log_notification(
            project_id=project_id,
            activity_performed="Project Assigned",
            performed_by=assigned_by if assigned_by else None,
            notified_user_id=user_id,
            notification_type="project_assigned",
            additional_info=f"You have been assigned to project '{project_name}' (ID: {project_id}) by {assigned_by_name}."
        )
        
        cur.close()
        
        return jsonify({
            "success": True,
            "message": "Member added to project successfully",
            "project_user_id": project_user_id
        })
        
    except Exception as e:
        return handle_database_error(get_db_connection(), f"Error adding member to project: {str(e)}")

@projects_bp.route('/api/projects/<int:project_id>/members/<int:user_id>', methods=['DELETE'])
def remove_project_member(project_id, user_id):
    """Remove a member from a project"""
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        
        # Check if the assignment exists
        cur.execute("""
            SELECT project_user_id FROM project_users 
            WHERE project_id = %s AND user_id = %s
        """, (project_id, user_id))
        
        assignment = cur.fetchone()
        if not assignment:
            cur.close()
            return jsonify({"success": False, "message": "User is not assigned to this project"}), 404
        
        # Remove the assignment
        cur.execute("""
            DELETE FROM project_users 
            WHERE project_id = %s AND user_id = %s
        """, (project_id, user_id))
        
        conn.commit()
        cur.close()
        
        return jsonify({
            "success": True,
            "message": "Member removed from project successfully"
        })
        
    except Exception as e:
        return handle_database_error(get_db_connection(), f"Error removing member from project: {str(e)}")

@projects_bp.route('/api/projects/<int:project_id>/details', methods=['GET'])
def get_project_details(project_id):
    """Get project details for assignment form"""
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        
        # Get project details
        cur.execute("""
            SELECT project_id, project_name, project_date
            FROM projects
            WHERE project_id = %s
        """, (project_id,))
        
        project = cur.fetchone()
        cur.close()
        
        if not project:
            return jsonify({"success": False, "message": "Project not found"}), 404
        
        return jsonify({
            "success": True,
            "project": {
                "project_id": project[0],
                "project_name": project[1],
                "project_date": project[2].isoformat() if project[2] else None
            }
        })
        
    except Exception as e:
        print(f"Error fetching project details for project {project_id}: {str(e)}")
        return jsonify({"success": False, "message": "Internal server error"}), 500

@projects_bp.route('/api/activity-logs', methods=['GET'])
def get_activity_logs():
    """Get activity logs for admin dashboard"""
    try:
        from utils.activity_logger import get_activity_logs
        
        # Get query parameters
        project_id = request.args.get('project_id', type=int)
        limit = request.args.get('limit', 100, type=int)
        
        # Fetch activity logs
        logs = get_activity_logs(project_id=project_id, limit=limit)
        
        return jsonify({
            "success": True,
            "logs": logs,
            "total": len(logs)
        })
        
    except Exception as e:
        print(f"Error fetching activity logs: {str(e)}")
        return jsonify({"success": False, "message": "Internal server error"}), 500

@projects_bp.route('/api/notifications/<int:user_id>', methods=['GET'])
def get_user_notifications(user_id):
    """Get notifications for a specific user"""
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        
        # Get limit from query parameters
        limit = request.args.get('limit', 50, type=int)
        unread_only = request.args.get('unread_only', 'false').lower() == 'true'
        
        # Build query
        if unread_only:
            cur.execute("""
                SELECT al.activity_id, al.project_id, al.activity_performed, 
                       al.performed_by, al.timestamp, al.additional_info,
                       al.is_read, al.notification_type,
                       u.name as performed_by_name, p.project_name
                FROM activity_logs al
                LEFT JOIN users u ON al.performed_by = u.user_id
                LEFT JOIN projects p ON al.project_id = p.project_id
                WHERE al.notified_user_id = %s AND al.is_read = FALSE
                ORDER BY al.timestamp DESC
                LIMIT %s
            """, (user_id, limit))
        else:
            cur.execute("""
                SELECT al.activity_id, al.project_id, al.activity_performed, 
                       al.performed_by, al.timestamp, al.additional_info,
                       al.is_read, al.notification_type,
                       u.name as performed_by_name, p.project_name
                FROM activity_logs al
                LEFT JOIN users u ON al.performed_by = u.user_id
                LEFT JOIN projects p ON al.project_id = p.project_id
                WHERE al.notified_user_id = %s
                ORDER BY al.timestamp DESC
                LIMIT %s
            """, (user_id, limit))
        
        notifications = cur.fetchall()
        cur.close()
        
        # Convert to list of dictionaries
        notification_list = []
        for notif in notifications:
            notification_list.append({
                "activity_id": notif[0],
                "project_id": notif[1],
                "activity_performed": notif[2],
                "performed_by": notif[3],
                "performed_by_name": notif[8],
                "timestamp": notif[4].isoformat() if notif[4] else None,
                "additional_info": notif[5],
                "is_read": notif[6],
                "notification_type": notif[7],
                "project_name": notif[9]
            })
        
        return jsonify({
            "success": True,
            "notifications": notification_list,
            "total": len(notification_list)
        })
        
    except Exception as e:
        print(f"Error fetching notifications: {str(e)}")
        return jsonify({"success": False, "message": "Internal server error"}), 500

@projects_bp.route('/api/notifications/<int:notification_id>/mark-read', methods=['PUT'])
def mark_notification_read(notification_id):
    """Mark a notification as read"""
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        
        # Check if notification exists
        cur.execute("""
            SELECT activity_id FROM activity_logs 
            WHERE activity_id = %s
        """, (notification_id,))
        
        if not cur.fetchone():
            cur.close()
            return jsonify({"success": False, "message": "Notification not found"}), 404
        
        # Update notification as read
        cur.execute("""
            UPDATE activity_logs 
            SET is_read = TRUE 
            WHERE activity_id = %s
        """, (notification_id,))
        
        conn.commit()
        cur.close()
        
        return jsonify({
            "success": True,
            "message": "Notification marked as read"
        })
        
    except Exception as e:
        print(f"Error marking notification as read: {str(e)}")
        return jsonify({"success": False, "message": "Internal server error"}), 500

@projects_bp.route('/api/activity-logs/pdf', methods=['GET'])
def download_activity_logs_pdf():
    """Generate and download activity logs as PDF"""
    try:
        from utils.activity_logger import get_activity_logs
        from reportlab.lib.pagesizes import A4
        from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
        from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
        from reportlab.lib import colors
        from reportlab.lib.units import inch
        from datetime import datetime
        import io
        
        # Get all activity logs
        logs = get_activity_logs(limit=1000)  # Get more logs for PDF
        
        # Create PDF
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=A4)
        story = []
        
        # Styles
        styles = getSampleStyleSheet()
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=16,
            spaceAfter=30,
            alignment=1  # Center alignment
        )
        
        # Title
        title = Paragraph("Activity Logs Report", title_style)
        story.append(title)
        story.append(Spacer(1, 12))
        
        # Date
        date_para = Paragraph(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", styles['Normal'])
        story.append(date_para)
        story.append(Spacer(1, 20))
        
        # Table data
        table_data = [['ID', 'User', 'Activity', 'Project', 'Timestamp']]
        
        for log in logs:
            # Format timestamp properly
            timestamp_str = 'N/A'
            if log.get('timestamp'):
                try:
                    if isinstance(log['timestamp'], str):
                        dt = datetime.fromisoformat(log['timestamp'].replace('Z', '+00:00'))
                        timestamp_str = dt.strftime('%Y-%m-%d %H:%M:%S')
                    else:
                        timestamp_str = log['timestamp'].strftime('%Y-%m-%d %H:%M:%S')
                except:
                    timestamp_str = str(log['timestamp'])
            
            # Clean up activity and project names - use correct field names
            activity = str(log.get('activity_performed', 'N/A')).strip()
            project = str(log.get('project_name', 'N/A')).strip()
            
            table_data.append([
                str(log.get('activity_id', 'N/A')),
                str(log.get('user_name', 'Unknown')).strip(),
                activity,
                project,
                timestamp_str
            ])
        
        # Create table with better column widths (removed details column)
        table = Table(table_data, colWidths=[0.6*inch, 1.5*inch, 2*inch, 1.5*inch, 1.8*inch])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, 0), 'CENTER'),  # Headers centered
            ('ALIGN', (0, 1), (0, -1), 'CENTER'),   # ID column centered
            ('ALIGN', (1, 1), (1, -1), 'LEFT'),     # User column left-aligned
            ('ALIGN', (2, 1), (2, -1), 'LEFT'),     # Activity column left-aligned
            ('ALIGN', (3, 1), (3, -1), 'LEFT'),     # Project column left-aligned
            ('ALIGN', (4, 1), (4, -1), 'CENTER'),   # Timestamp column centered
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('FONTSIZE', (0, 1), (-1, -1), 8),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.beige]),
        ]))
        
        story.append(table)
        
        # Build PDF
        doc.build(story)
        buffer.seek(0)
        
        return Response(
            buffer.getvalue(),
            mimetype='application/pdf',
            headers={
                'Content-Disposition': f'attachment; filename=activity_logs_{datetime.now().strftime("%Y%m%d")}.pdf'
            }
        )
        
    except Exception as e:
        print(f"Error generating PDF: {str(e)}")
        return jsonify({"success": False, "message": "Error generating PDF"}), 500