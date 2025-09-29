"""
Report management routes
"""
from flask import Blueprint, request, jsonify
from config import get_db_connection
from utils.helpers import handle_database_error

reports_bp = Blueprint('reports', __name__)

@reports_bp.route('/api/reports', methods=['GET'])
def get_reports():
    """Get reports with role-based filtering"""
    try:
        # Get user context from query parameters
        user_id = request.args.get('user_id', type=int)
        user_role = request.args.get('user_role', type=int)
        
        conn = get_db_connection()
        cur = conn.cursor()
        
        # Build query based on user role
        if user_role == 5:  # Designer role
            # For designers, show only reports for memos they submitted
            base_query = """
                SELECT 
                    r.report_id,
                    r.memo_id,
                    r.project_id,
                    r.lru_id,
                    r.serial_id,
                    r.inspection_stage,
                    r.date_of_review,
                    r.review_venue,
                    r.reference_document,
                    r.status,
                    r.created_at,
                    p.project_name,
                    l.lru_name,
                    m.wing_proj_ref_no,
                    m.lru_sru_desc,
                    m.part_number,
                    m.memo_id
                FROM reports r
                LEFT JOIN projects p ON r.project_id = p.project_id
                LEFT JOIN lrus l ON r.lru_id = l.lru_id
                LEFT JOIN memos m ON r.memo_id = m.memo_id
                WHERE m.submitted_by = %s
                ORDER BY r.created_at DESC
            """
            query_params = (user_id,)
            
        elif user_role == 3:  # QA Reviewer role
            # For QA reviewers, show only reports for memos assigned to them
            base_query = """
                SELECT 
                    r.report_id,
                    r.memo_id,
                    r.project_id,
                    r.lru_id,
                    r.serial_id,
                    r.inspection_stage,
                    r.date_of_review,
                    r.review_venue,
                    r.reference_document,
                    r.status,
                    r.created_at,
                    p.project_name,
                    l.lru_name,
                    m.wing_proj_ref_no,
                    m.lru_sru_desc,
                    m.part_number,
                    m.memo_id
                FROM reports r
                LEFT JOIN projects p ON r.project_id = p.project_id
                LEFT JOIN lrus l ON r.lru_id = l.lru_id
                LEFT JOIN memos m ON r.memo_id = m.memo_id
                LEFT JOIN memo_approval ma ON m.memo_id = ma.memo_id
                WHERE ma.user_id = %s AND ma.status = 'accepted'
                ORDER BY r.created_at DESC
            """
            query_params = (user_id,)
            
        else:  # Admin, QA Head, Design Head - show all reports
            base_query = """
                SELECT 
                    r.report_id,
                    r.memo_id,
                    r.project_id,
                    r.lru_id,
                    r.serial_id,
                    r.inspection_stage,
                    r.date_of_review,
                    r.review_venue,
                    r.reference_document,
                    r.status,
                    r.created_at,
                    p.project_name,
                    l.lru_name,
                    m.wing_proj_ref_no,
                    m.lru_sru_desc,
                    m.part_number,
                    m.memo_id
                FROM reports r
                LEFT JOIN projects p ON r.project_id = p.project_id
                LEFT JOIN lrus l ON r.lru_id = l.lru_id
                LEFT JOIN memos m ON r.memo_id = m.memo_id
                ORDER BY r.created_at DESC
            """
            query_params = ()
        
        cur.execute(base_query, query_params)
        reports = cur.fetchall()
        cur.close()
        
        # Convert to list of dictionaries
        report_list = []
        for report in reports:
            report_list.append({
                "id": report[0],
                "memo_id": report[1],
                "project_id": report[2],
                "lru_id": report[3],
                "serial_id": report[4],
                "inspection_stage": report[5],
                "date_of_review": report[6].isoformat() if report[6] else None,
                "review_venue": report[7],
                "reference_document": report[8],
                "status": report[9],
                "created_at": report[10].isoformat() if report[10] else None,
                "project": report[11],
                "lru_name": report[12],
                "name": report[13] or f"MEMO-{report[1]}",  # Use wing_proj_ref_no or fallback to MEMO-{id}
                "memo_description": report[14],
                "part_number": report[15]
            })
        
        return jsonify({
            "success": True,
            "reports": report_list,
            "user_role": user_role,
            "user_id": user_id
        })
        
    except Exception as e:
        print(f"Error fetching reports: {str(e)}")
        return handle_database_error(get_db_connection(), f"Error fetching reports: {str(e)}")

@reports_bp.route('/api/reports', methods=['POST'])
def create_report():
    """Create a new report for an assigned memo"""
    try:
        data = request.json
        if not data:
            return jsonify({"success": False, "message": "No data provided"}), 400
        
        # Validate required fields
        required_fields = ['memo_id', 'project_id', 'lru_id', 'serial_id']
        for field in required_fields:
            if field not in data:
                return jsonify({"success": False, "message": f"Missing required field: {field}"}), 400
        
        conn = get_db_connection()
        cur = conn.cursor()
        
        # Check if report already exists for this memo
        cur.execute("SELECT report_id FROM reports WHERE memo_id = %s", (data['memo_id'],))
        if cur.fetchone():
            cur.close()
            return jsonify({"success": False, "message": "Report already exists for this memo"}), 400
        
        # Insert new report
        cur.execute("""
            INSERT INTO reports (memo_id, project_id, lru_id, serial_id, inspection_stage, 
                               date_of_review, review_venue, reference_document, status, created_at)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, NOW())
        """, (
            data['memo_id'],
            data['project_id'],
            data['lru_id'],
            data['serial_id'],
            data.get('inspection_stage'),
            data.get('date_of_review'),
            data.get('review_venue'),
            data.get('reference_document'),
            data.get('status', 'ASSIGNED')
        ))
        
        conn.commit()
        cur.close()
        
        return jsonify({
            "success": True,
            "message": "Report created successfully"
        })
        
    except Exception as e:
        print(f"Error creating report: {str(e)}")
        return handle_database_error(get_db_connection(), f"Error creating report: {str(e)}")

@reports_bp.route('/api/reports/<int:report_id>', methods=['GET'])
def get_report_details(report_id):
    """Get detailed information for a specific report"""
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        
        # Fetch report details with memo information
        cur.execute("""
            SELECT 
                r.report_id,
                r.memo_id,
                r.project_id,
                r.lru_id,
                r.serial_id,
                r.inspection_stage,
                r.date_of_review,
                r.review_venue,
                r.reference_document,
                r.status,
                r.created_at,
                p.project_name,
                l.lru_name,
                m.wing_proj_ref_no,
                m.lru_sru_desc,
                m.part_number,
                m.from_person,
                m.to_person,
                m.thru_person,
                m.casdic_ref_no,
                m.dated,
                m.manufacturer,
                m.drawing_no_rev,
                m.source,
                m.venue,
                m.memo_date,
                m.name_designation,
                m.test_facility,
                m.test_cycle_duration,
                m.test_start_on,
                m.test_complete_on,
                m.calibration_status,
                m.func_check_initial,
                m.perf_check_during,
                m.func_check_end,
                m.certified,
                m.remarks
            FROM reports r
            LEFT JOIN projects p ON r.project_id = p.project_id
            LEFT JOIN lrus l ON r.lru_id = l.lru_id
            LEFT JOIN memos m ON r.memo_id = m.memo_id
            WHERE r.report_id = %s
        """, (report_id,))
        
        report = cur.fetchone()
        cur.close()
        
        if not report:
            return jsonify({"success": False, "message": "Report not found"}), 404
        
        # Convert to dictionary
        report_data = {
            "id": report[0],
            "memo_id": report[1],
            "project_id": report[2],
            "lru_id": report[3],
            "serial_id": report[4],
            "inspection_stage": report[5],
            "date_of_review": report[6].isoformat() if report[6] else None,
            "review_venue": report[7],
            "reference_document": report[8],
            "status": report[9],
            "created_at": report[10].isoformat() if report[10] else None,
            "project_name": report[11],
            "lru_name": report[12],
            "wing_proj_ref_no": report[13],
            "lru_sru_desc": report[14],
            "part_number": report[15],
            "from_person": report[16],
            "to_person": report[17],
            "thru_person": report[18],
            "casdic_ref_no": report[19],
            "dated": report[20].isoformat() if report[20] else None,
            "manufacturer": report[21],
            "drawing_no_rev": report[22],
            "source": report[23],
            "venue": report[24],
            "memo_date": report[25].isoformat() if report[25] else None,
            "name_designation": report[26],
            "test_facility": report[27],
            "test_cycle_duration": report[28],
            "test_start_on": report[29].isoformat() if report[29] else None,
            "test_complete_on": report[30].isoformat() if report[30] else None,
            "calibration_status": report[31],
            "func_check_initial": report[32].isoformat() if report[32] else None,
            "perf_check_during": report[33].isoformat() if report[33] else None,
            "func_check_end": report[34].isoformat() if report[34] else None,
            "certified": report[35],
            "remarks": report[36]
        }
        
        return jsonify({
            "success": True,
            "report": report_data
        })
        
    except Exception as e:
        print(f"Error fetching report details: {str(e)}")
        return handle_database_error(get_db_connection(), f"Error fetching report details: {str(e)}")

@reports_bp.route('/api/reports/<int:report_id>', methods=['PUT'])
def update_report_status(report_id):
    """Update report status"""
    try:
        data = request.json
        if not data or 'status' not in data:
            return jsonify({"success": False, "message": "Status is required"}), 400
        
        conn = get_db_connection()
        cur = conn.cursor()
        
        # Update report status
        cur.execute("""
            UPDATE reports 
            SET status = %s, date_of_review = %s
            WHERE report_id = %s
        """, (data['status'], data.get('date_of_review'), report_id))
        
        if cur.rowcount == 0:
            cur.close()
            return jsonify({"success": False, "message": "Report not found"}), 404
        
        conn.commit()
        cur.close()
        
        return jsonify({
            "success": True,
            "message": "Report status updated successfully"
        })
        
    except Exception as e:
        print(f"Error updating report status: {str(e)}")
        return handle_database_error(get_db_connection(), f"Error updating report status: {str(e)}")
