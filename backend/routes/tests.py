"""
Test configuration management routes
"""
from flask import Blueprint, request, jsonify
from config import get_db_connection
from utils.helpers import handle_database_error

tests_bp = Blueprint('tests', __name__)

@tests_bp.route('/api/tests', methods=['GET'])
def get_tests():
    """Get all tests"""
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        
        cur.execute("""
            SELECT test_id, test_name, created_at
            FROM tests
            ORDER BY test_id
        """)
        
        tests = cur.fetchall()
        cur.close()
        
        test_list = []
        for test in tests:
            test_list.append({
                "test_id": test[0],
                "test_name": test[1],
                "created_at": test[2].isoformat() if test[2] else None
            })
        
        return jsonify({
            "success": True,
            "tests": test_list
        })
        
    except Exception as e:
        print(f"Error fetching tests: {str(e)}")
        return jsonify({"success": False, "message": "Internal server error"}), 500

@tests_bp.route('/api/stages', methods=['GET'])
def get_stages():
    """Get all stages"""
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        
        cur.execute("""
            SELECT stage_id, stage_name, created_at
            FROM stages
            ORDER BY stage_id
        """)
        
        stages = cur.fetchall()
        cur.close()
        
        stage_list = []
        for stage in stages:
            stage_list.append({
                "stage_id": stage[0],
                "stage_name": stage[1],
                "created_at": stage[2].isoformat() if stage[2] else None
            })
        
        return jsonify({
            "success": True,
            "stages": stage_list
        })
        
    except Exception as e:
        print(f"Error fetching stages: {str(e)}")
        return jsonify({"success": False, "message": "Internal server error"}), 500

@tests_bp.route('/api/stage-types', methods=['GET'])
def get_stage_types():
    """Get all stage types"""
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        
        cur.execute("""
            SELECT type_id, type_name
            FROM stage_types
            ORDER BY type_name
        """)
        
        types = cur.fetchall()
        cur.close()
        
        type_list = []
        for stage_type in types:
            type_list.append({
                "type_id": stage_type[0],
                "type_name": stage_type[1]
            })
        
        return jsonify({
            "success": True,
            "stage_types": type_list
        })
        
    except Exception as e:
        print(f"Error fetching stage types: {str(e)}")
        return jsonify({"success": False, "message": "Internal server error"}), 500

@tests_bp.route('/api/tests-configuration', methods=['GET'])
def get_tests_configuration():
    """Get complete test configuration matrix"""
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        
        # Get all tests
        cur.execute("""
            SELECT test_id, test_name, created_at
            FROM tests
            ORDER BY test_id
        """)
        tests = cur.fetchall()
        
        # Get all stages
        cur.execute("""
            SELECT stage_id, stage_name, created_at
            FROM stages
            ORDER BY stage_id
        """)
        stages = cur.fetchall()
        
        # Get all stage types
        cur.execute("""
            SELECT type_id, type_name
            FROM stage_types
            ORDER BY type_name
        """)
        stage_types = cur.fetchall()
        
        # Get current configurations
        cur.execute("""
            SELECT 
                tst.test_id,
                tst.stage_id,
                tst.type_id,
                t.test_name,
                s.stage_name,
                st.type_name
            FROM test_stage_types tst
            JOIN tests t ON tst.test_id = t.test_id
            JOIN stages s ON tst.stage_id = s.stage_id
            JOIN stage_types st ON tst.type_id = st.type_id
            ORDER BY t.test_id, s.stage_id
        """)
        configurations = cur.fetchall()
        
        cur.close()
        
        # Format tests
        test_list = []
        for test in tests:
            test_list.append({
                "test_id": test[0],
                "test_name": test[1],
                "created_at": test[2].isoformat() if test[2] else None
            })
        
        # Format stages
        stage_list = []
        for stage in stages:
            stage_list.append({
                "stage_id": stage[0],
                "stage_name": stage[1],
                "created_at": stage[2].isoformat() if stage[2] else None
            })
        
        # Format stage types
        type_list = []
        for stage_type in stage_types:
            type_list.append({
                "type_id": stage_type[0],
                "type_name": stage_type[1]
            })
        
        # Format configurations
        config_list = []
        for config in configurations:
            config_list.append({
                "test_id": config[0],
                "stage_id": config[1],
                "type_id": config[2],
                "test_name": config[3],
                "stage_name": config[4],
                "type_name": config[5]
            })
        
        return jsonify({
            "success": True,
            "tests": test_list,
            "stages": stage_list,
            "stage_types": type_list,
            "configurations": config_list
        })
        
    except Exception as e:
        print(f"Error fetching test configuration matrix: {str(e)}")
        return jsonify({"success": False, "message": "Internal server error"}), 500

@tests_bp.route('/api/test-stage-types', methods=['GET'])
def get_test_stage_types():
    """Get test-stage-type configurations (legacy endpoint)"""
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        
        cur.execute("""
            SELECT 
                tst.test_id,
                tst.stage_id,
                tst.type_id,
                t.test_name,
                s.stage_name,
                st.type_name
            FROM test_stage_types tst
            JOIN tests t ON tst.test_id = t.test_id
            JOIN stages s ON tst.stage_id = s.stage_id
            JOIN stage_types st ON tst.type_id = st.type_id
            ORDER BY t.test_id, s.stage_id
        """)
        
        configurations = cur.fetchall()
        cur.close()
        
        config_list = []
        for config in configurations:
            config_list.append({
                "test_id": config[0],
                "stage_id": config[1],
                "type_id": config[2],
                "test_name": config[3],
                "stage_name": config[4],
                "type_name": config[5]
            })
        
        return jsonify({
            "success": True,
            "configurations": config_list
        })
        
    except Exception as e:
        print(f"Error fetching test-stage-type configurations: {str(e)}")
        return jsonify({"success": False, "message": "Internal server error"}), 500

@tests_bp.route('/api/test/<int:test_id>/stage-types', methods=['GET'])
def get_test_stage_types_by_test(test_id):
    """Get stage types for a specific test ID"""
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        
        # First verify the test exists
        cur.execute("SELECT test_id, test_name FROM tests WHERE test_id = %s", (test_id,))
        test = cur.fetchone()
        if not test:
            cur.close()
            return jsonify({"success": False, "message": "Test not found"}), 404
        
        # Get stage types for this specific test
        cur.execute("""
            SELECT 
                s.stage_id,
                s.stage_name,
                st.type_id,
                st.type_name
            FROM test_stage_types tst
            JOIN stages s ON tst.stage_id = s.stage_id
            JOIN stage_types st ON tst.type_id = st.type_id
            WHERE tst.test_id = %s
            ORDER BY s.stage_id, st.type_name
        """, (test_id,))
        
        stage_types = cur.fetchall()
        cur.close()
        
        # Group by stage
        stages_with_types = {}
        for stage_type in stage_types:
            stage_id = stage_type[0]
            stage_name = stage_type[1]
            type_id = stage_type[2]
            type_name = stage_type[3]
            
            if stage_id not in stages_with_types:
                stages_with_types[stage_id] = {
                    "stage_id": stage_id,
                    "stage_name": stage_name,
                    "types": []
                }
            
            stages_with_types[stage_id]["types"].append({
                "type_id": type_id,
                "type_name": type_name
            })
        
        return jsonify({
            "success": True,
            "test": {
                "test_id": test[0],
                "test_name": test[1]
            },
            "stages": list(stages_with_types.values())
        })
        
    except Exception as e:
        print(f"Error fetching stage types for test {test_id}: {str(e)}")
        return jsonify({"success": False, "message": "Internal server error"}), 500

@tests_bp.route('/api/tests', methods=['POST'])
def create_test():
    """Create new test"""
    try:
        data = request.json
        if not data or not data.get('test_name'):
            return jsonify({"success": False, "message": "Test name is required"}), 400
        
        conn = get_db_connection()
        cur = conn.cursor()
        
        # Check if test name already exists
        cur.execute("SELECT test_id FROM tests WHERE test_name = %s", (data['test_name'],))
        if cur.fetchone():
            cur.close()
            return jsonify({"success": False, "message": "Test name already exists"}), 400
        
        # Insert new test
        cur.execute("""
            INSERT INTO tests (test_name)
            VALUES (%s)
            RETURNING test_id
        """, (data['test_name'],))
        
        test_id = cur.fetchone()[0]
        conn.commit()
        cur.close()
        
        return jsonify({
            "success": True,
            "message": "Test created successfully",
            "test_id": test_id
        })
        
    except Exception as e:
        return handle_database_error(get_db_connection(), f"Error creating test: {str(e)}")

@tests_bp.route('/api/stages', methods=['POST'])
def create_stage():
    """Create new stage"""
    try:
        data = request.json
        if not data or not data.get('stage_name'):
            return jsonify({"success": False, "message": "Stage name is required"}), 400
        
        conn = get_db_connection()
        cur = conn.cursor()
        
        # Check if stage name already exists
        cur.execute("SELECT stage_id FROM stages WHERE stage_name = %s", (data['stage_name'],))
        if cur.fetchone():
            cur.close()
            return jsonify({"success": False, "message": "Stage name already exists"}), 400
        
        # Insert new stage
        cur.execute("""
            INSERT INTO stages (stage_name)
            VALUES (%s)
            RETURNING stage_id
        """, (data['stage_name'],))
        
        stage_id = cur.fetchone()[0]
        conn.commit()
        cur.close()
        
        return jsonify({
            "success": True,
            "message": "Stage created successfully",
            "stage_id": stage_id
        })
        
    except Exception as e:
        return handle_database_error(get_db_connection(), f"Error creating stage: {str(e)}")

@tests_bp.route('/api/test-stage-types', methods=['POST'])
def update_test_stage_types():
    """Update test-stage-type configurations"""
    try:
        data = request.json
        if not data or 'configurations' not in data:
            return jsonify({"success": False, "message": "Configurations data is required"}), 400
        
        # Get current user from request (you might want to implement proper auth)
        current_user = data.get('assigned_by', 1002)  # Default user for now
        
        conn = get_db_connection()
        cur = conn.cursor()
        
        # Clear existing configurations
        cur.execute("DELETE FROM test_stage_types")
        
        # Insert new configurations
        for config in data['configurations']:
            if config.get('test_id') and config.get('stage_id') and config.get('type_id'):
                cur.execute("""
                    INSERT INTO test_stage_types (test_id, stage_id, type_id, assigned_by)
                    VALUES (%s, %s, %s, %s)
                """, (config['test_id'], config['stage_id'], config['type_id'], current_user))
        
        conn.commit()
        cur.close()
        
        return jsonify({
            "success": True,
            "message": "Test-stage-type configurations updated successfully"
        })
        
    except Exception as e:
        return handle_database_error(get_db_connection(), f"Error updating test-stage-type configurations: {str(e)}")

@tests_bp.route('/api/tests/<int:test_id>', methods=['DELETE'])
def delete_test(test_id):
    """Delete test"""
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        
        # Delete test-stage-type configurations first
        cur.execute("DELETE FROM test_stage_types WHERE test_id = %s", (test_id,))
        
        # Delete test
        cur.execute("DELETE FROM tests WHERE test_id = %s RETURNING test_id", (test_id,))
        deleted = cur.fetchone()
        
        if not deleted:
            cur.close()
            return jsonify({"success": False, "message": "Test not found"}), 404
        
        conn.commit()
        cur.close()
        
        return jsonify({
            "success": True,
            "message": "Test deleted successfully"
        })
        
    except Exception as e:
        return handle_database_error(get_db_connection(), f"Error deleting test: {str(e)}")

@tests_bp.route('/api/stages/<int:stage_id>', methods=['DELETE'])
def delete_stage(stage_id):
    """Delete stage"""
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        
        # Delete test-stage-type configurations for this stage first
        cur.execute("DELETE FROM test_stage_types WHERE stage_id = %s", (stage_id,))
        
        # Delete stage
        cur.execute("DELETE FROM stages WHERE stage_id = %s RETURNING stage_id", (stage_id,))
        deleted = cur.fetchone()
        
        if not deleted:
            cur.close()
            return jsonify({"success": False, "message": "Stage not found"}), 404
        
        conn.commit()
        cur.close()
        
        return jsonify({
            "success": True,
            "message": "Stage deleted successfully"
        })
        
    except Exception as e:
        return handle_database_error(get_db_connection(), f"Error deleting stage: {str(e)}")

@tests_bp.route('/api/tests-debug', methods=['GET'])
def get_tests_debug():
    """Diagnostic endpoint to check database contents"""
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        
        # Check tests table
        cur.execute("SELECT COUNT(*) FROM tests")
        test_count = cur.fetchone()[0]
        
        cur.execute("SELECT test_id, test_name FROM tests LIMIT 5")
        test_samples = cur.fetchall()
        
        # Check stages table
        cur.execute("SELECT COUNT(*) FROM stages")
        stage_count = cur.fetchone()[0]
        
        cur.execute("SELECT stage_id, stage_name FROM stages LIMIT 5")
        stage_samples = cur.fetchall()
        
        # Check stage_types table
        cur.execute("SELECT COUNT(*) FROM stage_types")
        type_count = cur.fetchone()[0]
        
        cur.execute("SELECT type_id, type_name FROM stage_types LIMIT 5")
        type_samples = cur.fetchall()
        
        # Check test_stage_types table
        cur.execute("SELECT COUNT(*) FROM test_stage_types")
        config_count = cur.fetchone()[0]
        
        cur.execute("""
            SELECT tst.test_id, tst.stage_id, tst.type_id, t.test_name, s.stage_name, st.type_name
            FROM test_stage_types tst
            JOIN tests t ON tst.test_id = t.test_id
            JOIN stages s ON tst.stage_id = s.stage_id
            JOIN stage_types st ON tst.type_id = st.type_id
            LIMIT 5
        """)
        config_samples = cur.fetchall()
        
        cur.close()
        
        return jsonify({
            "success": True,
            "debug_info": {
                "tests": {
                    "count": test_count,
                    "samples": [{"test_id": t[0], "test_name": t[1]} for t in test_samples]
                },
                "stages": {
                    "count": stage_count,
                    "samples": [{"stage_id": s[0], "stage_name": s[1]} for s in stage_samples]
                },
                "stage_types": {
                    "count": type_count,
                    "samples": [{"type_id": st[0], "type_name": st[1]} for st in type_samples]
                },
                "configurations": {
                    "count": config_count,
                    "samples": [{"test_id": c[0], "stage_id": c[1], "type_id": c[2], "test_name": c[3], "stage_name": c[4], "type_name": c[5]} for c in config_samples]
                }
            }
        })
        
    except Exception as e:
        print(f"Debug error: {str(e)}")
        return jsonify({"success": False, "message": f"Debug error: {str(e)}"}), 500
