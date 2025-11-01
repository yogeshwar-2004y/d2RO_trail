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
                dim4_dimension TEXT, dim4_tolerance TEXT, dim4_observed_value TEXT, dim4_instrument_used TEXT, dim4_remarks TEXT, dim4_upload TEXT,
                param1_name TEXT DEFAULT 'Burrs', param1_compliance_observation TEXT, param1_expected TEXT DEFAULT 'Not Expected (NO)', param1_remarks TEXT, param1_upload TEXT,
                param2_name TEXT DEFAULT 'Damages', param2_compliance_observation TEXT, param2_expected TEXT DEFAULT 'Not Expected (NO)', param2_remarks TEXT, param2_upload TEXT,
                param3_name TEXT DEFAULT 'Name Plate', param3_compliance_observation TEXT, param3_expected TEXT DEFAULT 'As per Drawing (YES)', param3_remarks TEXT, param3_upload TEXT,
                param4_name TEXT DEFAULT 'Engraving', param4_compliance_observation TEXT, param4_expected TEXT DEFAULT 'As per Drawing (YES)', param4_remarks TEXT, param4_upload TEXT,
                param5_name TEXT DEFAULT 'Passivation', param5_compliance_observation TEXT, param5_expected TEXT DEFAULT 'As per Drawing (YES)', param5_remarks TEXT, param5_upload TEXT,
                param6_name TEXT DEFAULT 'Chromate', param6_compliance_observation TEXT, param6_expected TEXT DEFAULT 'As per Drawing (YES)', param6_remarks TEXT, param6_upload TEXT,
                param7_name TEXT DEFAULT 'Electro-less Nickel plating', param7_compliance_observation TEXT, param7_expected TEXT DEFAULT 'As per Drawing (YES)', param7_remarks TEXT, param7_upload TEXT,
                param8_name TEXT DEFAULT 'Fasteners', param8_compliance_observation TEXT, param8_expected TEXT DEFAULT 'As per Drawing (YES)', param8_remarks TEXT, param8_upload TEXT,
                prepared_by TEXT,
                verified_by TEXT,
                approved_by TEXT,
                created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Insert new mechanical inspection report with all fields
        cur.execute("""
            INSERT INTO mechanical_inspection_report (
                project_name, report_ref_no, memo_ref_no, lru_name, inspection_stage,
                test_venue, sl_nos, dp_name, dated1, dated2, sru_name, part_no, quantity,
                start_date, end_date,
                dim1_dimension, dim1_tolerance, dim1_observed_value, dim1_instrument_used, dim1_remarks, dim1_upload,
                dim2_dimension, dim2_tolerance, dim2_observed_value, dim2_instrument_used, dim2_remarks, dim2_upload,
                dim3_dimension, dim3_tolerance, dim3_observed_value, dim3_instrument_used, dim3_remarks, dim3_upload,
                dim4_dimension, dim4_tolerance, dim4_observed_value, dim4_instrument_used, dim4_remarks, dim4_upload,
                param1_compliance_observation, param1_expected, param1_remarks, param1_upload,
                param2_compliance_observation, param2_expected, param2_remarks, param2_upload,
                param3_compliance_observation, param3_expected, param3_remarks, param3_upload,
                param4_compliance_observation, param4_expected, param4_remarks, param4_upload,
                param5_compliance_observation, param5_expected, param5_remarks, param5_upload,
                param6_compliance_observation, param6_expected, param6_remarks, param6_upload,
                param7_compliance_observation, param7_expected, param7_remarks, param7_upload,
                param8_compliance_observation, param8_expected, param8_remarks, param8_upload,
                prepared_by, verified_by, approved_by
            ) VALUES (
                %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
                %s, %s, %s, %s, %s, %s,
                %s, %s, %s, %s, %s, %s,
                %s, %s, %s, %s, %s, %s,
                %s, %s, %s, %s, %s, %s,
                %s, %s, %s, %s,
                %s, %s, %s, %s,
                %s, %s, %s, %s,
                %s, %s, %s, %s,
                %s, %s, %s, %s,
                %s, %s, %s, %s,
                %s, %s, %s, %s,
                %s, %s, %s, %s,
                %s, %s, %s
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
            data.get('end_date'),
            # Dimension 1
            data.get('dim1_dimension'),
            data.get('dim1_tolerance'),
            data.get('dim1_observed_value'),
            data.get('dim1_instrument_used'),
            data.get('dim1_remarks'),
            data.get('dim1_upload'),
            # Dimension 2
            data.get('dim2_dimension'),
            data.get('dim2_tolerance'),
            data.get('dim2_observed_value'),
            data.get('dim2_instrument_used'),
            data.get('dim2_remarks'),
            data.get('dim2_upload'),
            # Dimension 3
            data.get('dim3_dimension'),
            data.get('dim3_tolerance'),
            data.get('dim3_observed_value'),
            data.get('dim3_instrument_used'),
            data.get('dim3_remarks'),
            data.get('dim3_upload'),
            # Dimension 4
            data.get('dim4_dimension'),
            data.get('dim4_tolerance'),
            data.get('dim4_observed_value'),
            data.get('dim4_instrument_used'),
            data.get('dim4_remarks'),
            data.get('dim4_upload'),
            # Parameter 1
            data.get('param1_compliance_observation'),
            data.get('param1_expected'),
            data.get('param1_remarks'),
            data.get('param1_upload'),
            # Parameter 2
            data.get('param2_compliance_observation'),
            data.get('param2_expected'),
            data.get('param2_remarks'),
            data.get('param2_upload'),
            # Parameter 3
            data.get('param3_compliance_observation'),
            data.get('param3_expected'),
            data.get('param3_remarks'),
            data.get('param3_upload'),
            # Parameter 4
            data.get('param4_compliance_observation'),
            data.get('param4_expected'),
            data.get('param4_remarks'),
            data.get('param4_upload'),
            # Parameter 5
            data.get('param5_compliance_observation'),
            data.get('param5_expected'),
            data.get('param5_remarks'),
            data.get('param5_upload'),
            # Parameter 6
            data.get('param6_compliance_observation'),
            data.get('param6_expected'),
            data.get('param6_remarks'),
            data.get('param6_upload'),
            # Parameter 7
            data.get('param7_compliance_observation'),
            data.get('param7_expected'),
            data.get('param7_remarks'),
            data.get('param7_upload'),
            # Parameter 8
            data.get('param8_compliance_observation'),
            data.get('param8_expected'),
            data.get('param8_remarks'),
            data.get('param8_upload'),
            # Signatures
            data.get('prepared_by'),
            data.get('verified_by'),
            data.get('approved_by')
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
