"""
Project and LRU management routes
"""
from flask import Blueprint, request, jsonify
from config import get_db_connection
from utils.helpers import handle_database_error

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
        if not user_id:
            return jsonify({"success": False, "message": "User ID is required"}), 400
        
        conn = get_db_connection()
        cur = conn.cursor()
        
        # Check if project exists
        cur.execute("SELECT project_id FROM projects WHERE project_id = %s", (project_id,))
        if not cur.fetchone():
            cur.close()
            return jsonify({"success": False, "message": "Project not found"}), 404
        
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