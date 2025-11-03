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

        # Get inspection items from the request
        inspection_items = data.get('inspectionItems', [])
        
        # Define default expected values for each test
        default_expected = {
            1: 'NIL',
            2: 'Verified',
            3: 'Matching',
            4: 'Matching',
            5: 'Stored in ESD',
            6: 'Fitted properly',
            7: 'NIL'
        }
        
        # Initialize test values
        test_values = {}
        for i in range(1, 8):  # We have 7 tests as per table structure
            # Find the matching inspection item for this test number
            item = next((item for item in inspection_items if item.get('slNo') == i), {})
            
            # Get expected value from request or use default if not provided
            expected_value = item.get('expected')
            if not expected_value:
                expected_value = default_expected[i]
            
            # Get observations and remarks
            observations = item.get('observations', '')
            remarks = item.get('remarks', '')
            if remarks:
                remarks = 'OK' if remarks == 'Passed' else 'NOT OK' if remarks == 'Failed' else remarks
            
            test_values.update({
                f'test{i}_expected': expected_value,
                f'test{i}_observations': observations,
                f'test{i}_remarks': remarks,
                f'test{i}_upload': item.get('upload', '')
            })

        # Insert new kit of parts inspection report
        cur.execute("""
            INSERT INTO kit_of_parts_inspection_report (
                project_name, report_ref_no, memo_ref_no, lru_name, inspection_stage,
                test_venue, sl_nos, dp_name, sru_name, part_no, quantity,
                start_date, end_date, dated1, dated2,
                test1_expected, test1_observations, test1_remarks, test1_upload,
                test2_expected, test2_observations, test2_remarks, test2_upload,
                test3_expected, test3_observations, test3_remarks, test3_upload,
                test4_expected, test4_observations, test4_remarks, test4_upload,
                test5_expected, test5_observations, test5_remarks, test5_upload,
                test6_expected, test6_observations, test6_remarks, test6_upload,
                test7_expected, test7_observations, test7_remarks, test7_upload,
                prepared_by_qa_g1, verified_by_g1h_qa_g, approved_by
            ) VALUES (
                %(project_name)s, %(report_ref_no)s, %(memo_ref_no)s, %(lru_name)s, %(inspection_stage)s,
                %(test_venue)s, %(sl_nos)s, %(dp_name)s, %(sru_name)s, %(part_no)s, %(quantity)s,
                %(start_date)s, %(end_date)s, %(dated1)s, %(dated2)s,
                %(test1_expected)s, %(test1_observations)s, %(test1_remarks)s, %(test1_upload)s,
                %(test2_expected)s, %(test2_observations)s, %(test2_remarks)s, %(test2_upload)s,
                %(test3_expected)s, %(test3_observations)s, %(test3_remarks)s, %(test3_upload)s,
                %(test4_expected)s, %(test4_observations)s, %(test4_remarks)s, %(test4_upload)s,
                %(test5_expected)s, %(test5_observations)s, %(test5_remarks)s, %(test5_upload)s,
                %(test6_expected)s, %(test6_observations)s, %(test6_remarks)s, %(test6_upload)s,
                %(test7_expected)s, %(test7_observations)s, %(test7_remarks)s, %(test7_upload)s,
                %(prepared_by_qa_g1)s, %(verified_by_g1h_qa_g)s, %(approved_by)s
            ) RETURNING report_id
        """, {
            'project_name': data['projectName'],
            'report_ref_no': data['reportRefNo'],
            'memo_ref_no': data.get('memoRefNo'),
            'lru_name': data['lruName'],
            'inspection_stage': data.get('inspectionStage'),
            'test_venue': data.get('testVenue'),
            'sl_nos': data.get('slNos'),
            'dp_name': data['dpName'],
            'sru_name': data.get('sruName'),
            'part_no': data['partNo'],
            'quantity': data['quantity'],
            'start_date': data.get('startDate'),
            'end_date': data.get('endDate'),
            'dated1': data.get('dated1'),
            'dated2': data.get('dated2'),
            'prepared_by_qa_g1': data.get('preparedBy', ''),
            'verified_by_g1h_qa_g': data.get('verifiedBy', ''),
            'approved_by': data.get('approvedBy', ''),
            **test_values
        })
        
        report_id = cur.fetchone()[0]
        conn.commit()
        
        # Debug: Log the values being stored
        print("Test values being stored:", test_values)
        
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
        
        if not report:
            return jsonify({"success": False, "message": "Report not found"}), 404
        
        # Convert to dictionary
        columns = [desc[0] for desc in cur.description]
        report_data = dict(zip(columns, report))

        # Map OK/NOT OK back to Passed/Failed for frontend
        for i in range(1, 8):
            remarks_key = f'test{i}_remarks'
            if report_data.get(remarks_key) == 'OK':
                report_data[remarks_key] = 'Passed'
            elif report_data.get(remarks_key) == 'NOT OK':
                report_data[remarks_key] = 'Failed'

        # Restructure the data for frontend format
        inspection_items = []
        for i in range(1, 8):
            inspection_items.append({
                'slNo': report_data.get(f'test{i}_sl_no', i),
                'testCase': report_data.get(f'test{i}_case', ''),
                'expected': report_data.get(f'test{i}_expected', ''),
                'observations': report_data.get(f'test{i}_observations', ''),
                'remarks': report_data.get(f'test{i}_remarks', ''),
                'upload': report_data.get(f'test{i}_upload', '')
            })

        # Format the response in frontend format
        frontend_data = {
            'projectName': report_data.get('project_name'),
            'dpName': report_data.get('dp_name'),
            'reportRefNo': report_data.get('report_ref_no'),
            'memoRefNo': report_data.get('memo_ref_no'),
            'lruName': report_data.get('lru_name'),
            'sruName': report_data.get('sru_name'),
            'partNo': report_data.get('part_no'),
            'quantity': report_data.get('quantity'),
            'slNos': report_data.get('sl_nos'),
            'testVenue': report_data.get('test_venue'),
            'inspectionStage': report_data.get('inspection_stage'),
            'startDate': report_data.get('start_date').strftime('%Y-%m-%d') if report_data.get('start_date') else None,
            'endDate': report_data.get('end_date').strftime('%Y-%m-%d') if report_data.get('end_date') else None,
            'preparedBy': report_data.get('prepared_by_qa_g1'),
            'verifiedBy': report_data.get('verified_by_g1h_qa_g'),
            'approvedBy': report_data.get('approved_by'),
            'inspectionItems': inspection_items
        }
        
        cur.close()
        
        return jsonify({
            "success": True,
            "report": frontend_data
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
