"""
Mechanical Inspection Report management routes
"""
from flask import Blueprint, request, jsonify
from config import get_db_connection
from utils.helpers import handle_database_error

mechanical_inspection_bp = Blueprint('mechanical_inspection', __name__)

@mechanical_inspection_bp.route('/api/mechanical-inspection', methods=['POST'])
def create_mechanical_inspection():
    """Create a new mechanical inspection report"""
    try:
        data = request.json
        if not data:
            return jsonify({"success": False, "message": "No data provided"}), 400
        
        # Validate required fields
        required_fields = ['project_name', 'report_ref_no', 'lru_name', 'dp_name', 'part_no', 'quantity']
        for field in required_fields:
            if field not in data or not data[field]:
                return jsonify({"success": False, "message": f"Missing required field: {field}"}), 400
        
        conn = get_db_connection()
        cur = conn.cursor()
        
        # First, check if table exists, if not create it
        cur.execute("""
            CREATE TABLE IF NOT EXISTS mechanical_inspection_report (
                report_id SERIAL PRIMARY KEY,
                project_name TEXT,
                report_ref_no VARCHAR(100),
                memo_ref_no VARCHAR(100),
                lru_name TEXT,
                inspection_stage TEXT,
                test_venue TEXT,
                sl_nos TEXT,
                dp_name TEXT,
                dated1 DATE,
                dated2 DATE,
                sru_name TEXT,
                part_no VARCHAR(100),
                quantity INT,
                start_date DATE,
                end_date DATE,
                dim1_dimension TEXT, dim1_tolerance TEXT, dim1_observed_value TEXT, dim1_instrument_used TEXT, dim1_remarks TEXT, dim1_upload TEXT,
                dim2_dimension TEXT, dim2_tolerance TEXT, dim2_observed_value TEXT, dim2_instrument_used TEXT, dim2_remarks TEXT, dim2_upload TEXT,
                dim3_dimension TEXT, dim3_tolerance TEXT, dim3_observed_value TEXT, dim3_instrument_used TEXT, dim3_remarks TEXT, dim3_upload TEXT,
                param1_name TEXT DEFAULT 'Burrs', param1_allowed TEXT, param1_yes_no VARCHAR(10), param1_expected TEXT, param1_remarks TEXT, param1_upload TEXT,
                param2_name TEXT DEFAULT 'Damages', param2_allowed TEXT, param2_yes_no VARCHAR(10), param2_expected TEXT, param2_remarks TEXT, param2_upload TEXT,
                param3_name TEXT DEFAULT 'Name Plate', param3_allowed TEXT, param3_yes_no VARCHAR(10), param3_expected TEXT, param3_remarks TEXT, param3_upload TEXT,
                param4_name TEXT DEFAULT 'Engraving', param4_allowed TEXT, param4_yes_no VARCHAR(10), param4_expected TEXT, param4_remarks TEXT, param4_upload TEXT,
                param5_name TEXT DEFAULT 'Passivation', param5_allowed TEXT, param5_yes_no VARCHAR(10), param5_expected TEXT, param5_remarks TEXT, param5_upload TEXT,
                param6_name TEXT DEFAULT 'Chromate', param6_allowed TEXT, param6_yes_no VARCHAR(10), param6_expected TEXT, param6_remarks TEXT, param6_upload TEXT,
                param7_name TEXT DEFAULT 'Electro-less Nickel plating', param7_allowed TEXT, param7_yes_no VARCHAR(10), param7_expected TEXT, param7_remarks TEXT, param7_upload TEXT,
                param8_name TEXT DEFAULT 'Fasteners', param8_allowed TEXT, param8_yes_no VARCHAR(10), param8_expected TEXT, param8_remarks TEXT, param8_upload TEXT,
                prepared_by TEXT,
                verified_by TEXT,
                approved_by TEXT,
                created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Insert new mechanical inspection report with basic fields first
        cur.execute("""
            INSERT INTO mechanical_inspection_report (
                project_name, report_ref_no, memo_ref_no, lru_name, inspection_stage,
                test_venue, sl_nos, dp_name, dated1, dated2, sru_name, part_no, quantity,
                start_date, end_date
            ) VALUES (
                %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
            ) RETURNING report_id
        """, (
            data['project_name'], 
            data['report_ref_no'], 
            data.get('memo_ref_no'), 
            data['lru_name'],
            data.get('inspection_stage'), 
            data.get('test_venue'), 
            data.get('sl_nos'), 
            data['dp_name'],
            data.get('dated1'),
            data.get('dated2'), 
            data.get('sru_name'), 
            data['part_no'], 
            data['quantity'],
            data.get('start_date'), 
            data.get('end_date')
        ))
        
        report_id = cur.fetchone()[0]
        conn.commit()
        cur.close()
        
        return jsonify({
            "success": True,
            "message": "Mechanical inspection report created successfully",
            "report_id": report_id
        })
        
    except Exception as e:
        print(f"Error creating mechanical inspection report: {str(e)}")
        return handle_database_error(get_db_connection(), f"Error creating mechanical inspection report: {str(e)}")

@mechanical_inspection_bp.route('/api/mechanical-inspection/<int:report_id>', methods=['GET'])
def get_mechanical_inspection(report_id):
    """Get a specific mechanical inspection report"""
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        
        cur.execute("SELECT * FROM mechanical_inspection_report WHERE report_id = %s", (report_id,))
        report = cur.fetchone()
        cur.close()
        
        if not report:
            return jsonify({"success": False, "message": "Report not found"}), 404
        
        # Convert to dictionary
        columns = [desc[0] for desc in cur.description] if cur.description else []
        report_data = dict(zip(columns, report))
        
        return jsonify({
            "success": True,
            "report": report_data
        })
        
    except Exception as e:
        print(f"Error fetching mechanical inspection report: {str(e)}")
        return handle_database_error(get_db_connection(), f"Error fetching mechanical inspection report: {str(e)}")

@mechanical_inspection_bp.route('/api/mechanical-inspection/<int:report_id>', methods=['PUT'])
def update_mechanical_inspection(report_id):
    """Update a mechanical inspection report"""
    try:
        data = request.json
        if not data:
            return jsonify({"success": False, "message": "No data provided"}), 400
        
        conn = get_db_connection()
        cur = conn.cursor()
        
        # Build dynamic update query
        update_fields = []
        update_values = []
        
        for key, value in data.items():
            if key != 'report_id':  # Don't update the ID
                update_fields.append(f"{key} = %s")
                update_values.append(value)
        
        if not update_fields:
            return jsonify({"success": False, "message": "No fields to update"}), 400
        
        update_values.append(report_id)
        
        cur.execute(f"""
            UPDATE mechanical_inspection_report 
            SET {', '.join(update_fields)}
            WHERE report_id = %s
        """, update_values)
        
        if cur.rowcount == 0:
            cur.close()
            return jsonify({"success": False, "message": "Report not found"}), 404
        
        conn.commit()
        cur.close()
        
        return jsonify({
            "success": True,
            "message": "Mechanical inspection report updated successfully"
        })
        
    except Exception as e:
        print(f"Error updating mechanical inspection report: {str(e)}")
        return handle_database_error(get_db_connection(), f"Error updating mechanical inspection report: {str(e)}")

@mechanical_inspection_bp.route('/api/mechanical-inspection', methods=['GET'])
def get_all_mechanical_inspections():
    """Get all mechanical inspection reports"""
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        
        cur.execute("""
            SELECT report_id, project_name, product_name, part_no, created_at, updated_at
            FROM mechanical_inspection_report
            ORDER BY created_at DESC
        """)
        
        reports = cur.fetchall()
        cur.close()
        
        report_list = []
        for report in reports:
            report_list.append({
                "report_id": report[0],
                "project_name": report[1],
                "product_name": report[2],
                "part_no": report[3],
                "created_at": report[4].isoformat() if report[4] else None,
                "updated_at": report[5].isoformat() if report[5] else None
            })
        
        return jsonify({
            "success": True,
            "reports": report_list
        })
        
    except Exception as e:
        print(f"Error fetching mechanical inspection reports: {str(e)}")
        return handle_database_error(get_db_connection(), f"Error fetching mechanical inspection reports: {str(e)}")
