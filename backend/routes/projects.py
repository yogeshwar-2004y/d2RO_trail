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
