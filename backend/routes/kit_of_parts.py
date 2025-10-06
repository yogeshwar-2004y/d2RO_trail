"""
Kit of Parts Inspection Report management routes
"""
from flask import Blueprint, request, jsonify
from config import get_db_connection
from utils.helpers import handle_database_error

kit_of_parts_bp = Blueprint('kit_of_parts', __name__)

@kit_of_parts_bp.route('/api/kit-of-parts', methods=['POST'])
def create_kit_of_parts_inspection():
    """Create a new kit of parts inspection report"""
    try:
        data = request.json
        if not data:
            return jsonify({"success": False, "message": "No data provided"}), 400
        
        # Validate required fields
        required_fields = ['projectName', 'reportRefNo', 'lruName', 'dpName', 'partNo', 'quantity']
        for field in required_fields:
            if field not in data or not data[field]:
                return jsonify({"success": False, "message": f"Missing required field: {field}"}), 400
        
        conn = get_db_connection()
        cur = conn.cursor()
        
        # Insert new kit of parts inspection report
        cur.execute("""
            INSERT INTO kit_of_parts_inspection_report (
                project_name, report_ref_no, memo_ref_no, lru_name, inspection_stage,
                test_venue, sl_nos, dp_name, dated1, dated2, sru_name, part_no, quantity,
                start_date, end_date,
                test1_observations, test1_remarks, test1_upload,
                test2_observations, test2_remarks, test2_upload,
                test3_observations, test3_remarks, test3_upload,
                test4_observations, test4_remarks, test4_upload,
                test5_observations, test5_remarks, test5_upload,
                test6_observations, test6_remarks, test6_upload,
                test7_observations, test7_remarks, test7_upload,
                prepared_by_qa_g1, verified_by_g1h_qa_g, approved_by
            ) VALUES (
                %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
                %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
                %s, %s, %s, %s, %s, %s, %s, %s, %s
            ) RETURNING report_id
        """, (
            data['projectName'], 
            data['reportRefNo'], 
            data.get('memoRefNo'), 
            data['lruName'],
            data.get('inspectionStage'), 
            data.get('testVenue'), 
            data.get('slNos'), 
            data['dpName'],
            data.get('dated1'),
            data.get('dated2'), 
            data.get('sruName'), 
            data['partNo'], 
            data['quantity'],
            data.get('startDate'), 
            data.get('endDate'),
            # Test case 1
            data.get('test1Observations', ''),
            data.get('test1Remarks', ''),
            data.get('test1Upload', ''),
            # Test case 2
            data.get('test2Observations', ''),
            data.get('test2Remarks', ''),
            data.get('test2Upload', ''),
            # Test case 3
            data.get('test3Observations', ''),
            data.get('test3Remarks', ''),
            data.get('test3Upload', ''),
            # Test case 4
            data.get('test4Observations', ''),
            data.get('test4Remarks', ''),
            data.get('test4Upload', ''),
            # Test case 5
            data.get('test5Observations', ''),
            data.get('test5Remarks', ''),
            data.get('test5Upload', ''),
            # Test case 6
            data.get('test6Observations', ''),
            data.get('test6Remarks', ''),
            data.get('test6Upload', ''),
            # Test case 7
            data.get('test7Observations', ''),
            data.get('test7Remarks', ''),
            data.get('test7Upload', ''),
            # Signatories
            data.get('preparedBy', ''),
            data.get('verifiedBy', ''),
            data.get('approvedBy', '')
        ))
        
        report_id = cur.fetchone()[0]
        conn.commit()
        cur.close()
        
        return jsonify({
            "success": True,
            "message": "Kit of parts inspection report created successfully",
            "report_id": report_id
        })
        
    except Exception as e:
        print(f"Error creating kit of parts inspection report: {str(e)}")
        return handle_database_error(get_db_connection(), f"Error creating kit of parts inspection report: {str(e)}")

@kit_of_parts_bp.route('/api/kit-of-parts/<int:report_id>', methods=['GET'])
def get_kit_of_parts_inspection(report_id):
    """Get a specific kit of parts inspection report"""
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        
        cur.execute("SELECT * FROM kit_of_parts_inspection_report WHERE report_id = %s", (report_id,))
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
        print(f"Error fetching kit of parts inspection report: {str(e)}")
        return handle_database_error(get_db_connection(), f"Error fetching kit of parts inspection report: {str(e)}")

@kit_of_parts_bp.route('/api/kit-of-parts/<int:report_id>', methods=['PUT'])
def update_kit_of_parts_inspection(report_id):
    """Update a kit of parts inspection report"""
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
            UPDATE kit_of_parts_inspection_report 
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
            "message": "Kit of parts inspection report updated successfully"
        })
        
    except Exception as e:
        print(f"Error updating kit of parts inspection report: {str(e)}")
        return handle_database_error(get_db_connection(), f"Error updating kit of parts inspection report: {str(e)}")

@kit_of_parts_bp.route('/api/kit-of-parts', methods=['GET'])
def get_all_kit_of_parts_inspections():
    """Get all kit of parts inspection reports"""
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        
        cur.execute("""
            SELECT report_id, project_name, lru_name, part_no, created_at, updated_at
            FROM kit_of_parts_inspection_report
            ORDER BY created_at DESC
        """)
        
        reports = cur.fetchall()
        cur.close()
        
        report_list = []
        for report in reports:
            report_list.append({
                "report_id": report[0],
                "project_name": report[1],
                "lru_name": report[2],
                "part_no": report[3],
                "created_at": report[4].isoformat() if report[4] else None,
                "updated_at": report[5].isoformat() if report[5] else None
            })
        
        return jsonify({
            "success": True,
            "reports": report_list
        })
        
    except Exception as e:
        print(f"Error fetching kit of parts inspection reports: {str(e)}")
        return handle_database_error(get_db_connection(), f"Error fetching kit of parts inspection reports: {str(e)}")
