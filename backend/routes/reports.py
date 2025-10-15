"""
Report management routes
"""
import os
import uuid
from functools import wraps
from flask import Blueprint, request, jsonify, send_file
from config import get_db_connection, Config
from utils.helpers import handle_database_error, allowed_file, validate_file_size
import json
from config import get_db_connection
from utils.helpers import handle_database_error

reports_bp = Blueprint('reports', __name__)

def require_design_head_role(f):
    """Decorator to require design head role (role_id = 4)"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        user_role = request.args.get('user_role', type=int)
        if user_role != 4:  # Design Head role
            return jsonify({
                "success": False, 
                "message": "Access denied. Design Head role required."
            }), 403
        return f(*args, **kwargs)
    return decorated_function

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
                    NULL as memo_id,
                    r.project_id,
                    r.lru_id,
                    r.serial_id,
                    r.inspection_stage,
                    r.date_of_review,
                    r.review_venue,
                    r.reference_document,
                    'Active' as status,
                    r.date_of_review as created_at,
                    p.project_name,
                    l.lru_name,
                    NULL as wing_proj_ref_no,
                    NULL as lru_sru_desc,
                    NULL as part_number,
                    NULL as memo_id
                FROM reports r
                LEFT JOIN projects p ON r.project_id = p.project_id
                LEFT JOIN lrus l ON r.lru_id = l.lru_id
                WHERE r.project_id IN (
                    SELECT project_id FROM projects WHERE created_by = %s
                )
                ORDER BY r.date_of_review DESC
            """
            query_params = (user_id,)
            
        elif user_role == 3:  # QA Reviewer role
            # For QA reviewers, show only reports for memos assigned to them
            base_query = """
                SELECT 
                    r.report_id,
                    NULL as memo_id,
                    r.project_id,
                    r.lru_id,
                    r.serial_id,
                    r.inspection_stage,
                    r.date_of_review,
                    r.review_venue,
                    r.reference_document,
                    'Active' as status,
                    r.date_of_review as created_at,
                    p.project_name,
                    l.lru_name,
                    NULL as wing_proj_ref_no,
                    NULL as lru_sru_desc,
                    NULL as part_number,
                    NULL as memo_id
                FROM reports r
                LEFT JOIN projects p ON r.project_id = p.project_id
                LEFT JOIN lrus l ON r.lru_id = l.lru_id
                ORDER BY r.date_of_review DESC
            """
            query_params = ()
            
        else:  # Admin, QA Head, Design Head - show all reports
            base_query = """
                SELECT 
                    r.report_id,
                    NULL as memo_id,
                    r.project_id,
                    r.lru_id,
                    r.serial_id,
                    r.inspection_stage,
                    r.date_of_review,
                    r.review_venue,
                    r.reference_document,
                    'Active' as status,
                    r.date_of_review as created_at,
                    p.project_name,
                    l.lru_name,
                    NULL as wing_proj_ref_no,
                    NULL as lru_sru_desc,
                    NULL as part_number,
                    NULL as memo_id
                FROM reports r
                LEFT JOIN projects p ON r.project_id = p.project_id
                LEFT JOIN lrus l ON r.lru_id = l.lru_id
                ORDER BY r.date_of_review DESC
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
            RETURNING report_id
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
        
        report_id = cur.fetchone()[0]
        
        # Log report generation activity
        from utils.activity_logger import log_activity
        log_activity(
            project_id=data['project_id'],
            activity_performed="Report Generated",
            performed_by=data.get('created_by', 1002),  # Default to admin if not provided
            additional_info=f"ID:{report_id}|Name:Report {report_id}|Report {report_id} was generated for memo {data['memo_id']}"
        )
        
        conn.commit()
        cur.close()
        
        return jsonify({
            "success": True,
            "message": "Report created successfully",
            "report_id": report_id
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
        
        # Fetch report details with memo and template information
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
                r.template_id,
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
                m.remarks,
                rt.template_name
            FROM reports r
            LEFT JOIN projects p ON r.project_id = p.project_id
            LEFT JOIN lrus l ON r.lru_id = l.lru_id
            LEFT JOIN memos m ON r.memo_id = m.memo_id
            LEFT JOIN report_templates rt ON r.template_id = rt.template_id
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
            "template_id": report[11],
            "project_name": report[12],
            "lru_name": report[13],
            "wing_proj_ref_no": report[14],
            "lru_sru_desc": report[15],
            "part_number": report[16],
            "from_person": report[17],
            "to_person": report[18],
            "thru_person": report[19],
            "casdic_ref_no": report[20],
            "dated": report[21].isoformat() if report[21] else None,
            "manufacturer": report[22],
            "drawing_no_rev": report[23],
            "source": report[24],
            "venue": report[25],
            "memo_date": report[26].isoformat() if report[26] else None,
            "name_designation": report[27],
            "test_facility": report[28],
            "test_cycle_duration": report[29],
            "test_start_on": report[30].isoformat() if report[30] else None,
            "test_complete_on": report[31].isoformat() if report[31] else None,
            "calibration_status": report[32],
            "func_check_initial": report[33].isoformat() if report[33] else None,
            "perf_check_during": report[34].isoformat() if report[34] else None,
            "func_check_end": report[35].isoformat() if report[35] else None,
            "certified": report[36],
            "remarks": report[37],
            "template_name": report[38]
        }
        
        return jsonify({
            "success": True,
            "report": report_data
        })
        
    except Exception as e:
        print(f"Error fetching report details: {str(e)}")
        return handle_database_error(get_db_connection(), f"Error fetching report details: {str(e)}")

@reports_bp.route('/api/reports/<int:report_id>/template', methods=['PUT'])
def update_report_template(report_id):
    """Update report template"""
    try:
        data = request.json
        if not data or 'template_id' not in data:
            return jsonify({"success": False, "message": "Template ID is required"}), 400
        
        template_id = data['template_id']
        
        conn = get_db_connection()
        cur = conn.cursor()
        
        # Verify template exists
        cur.execute("SELECT template_id FROM report_templates WHERE template_id = %s", (template_id,))
        if not cur.fetchone():
            cur.close()
            return jsonify({"success": False, "message": "Invalid template ID"}), 400
        
        # Update report with template_id
        cur.execute("""
            UPDATE reports 
            SET template_id = %s 
            WHERE report_id = %s
        """, (template_id, report_id))
        
        if cur.rowcount == 0:
            cur.close()
            return jsonify({"success": False, "message": "Report not found"}), 404
        
        conn.commit()
        cur.close()
        
        return jsonify({
            "success": True,
            "message": "Report template updated successfully"
        })
        
    except Exception as e:
        print(f"Error updating report template: {str(e)}")
        return handle_database_error(get_db_connection(), f"Error updating report template: {str(e)}")

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

# Assembled Board Inspection Report Routes

@reports_bp.route('/api/reports/assembled-board', methods=['POST'])
@require_design_head_role
def create_assembled_board_report():
    """Create a new assembled board inspection report"""
    try:
        print("🚀 ASSEMBLED BOARD REPORT ENDPOINT CALLED!")
        print(f"   Method: {request.method}")
        print(f"   Headers: {dict(request.headers)}")
        print(f"   User Role: {request.args.get('user_role')}")
        
        data = request.json
        if not data:
            print("❌ NO DATA PROVIDED IN REQUEST")
            return jsonify({"success": False, "message": "No data provided"}), 400
        
        # Validate the data
        validation_errors = validate_assembled_board_data(data)
        if validation_errors:
            return jsonify({
                "success": False, 
                "message": "Validation errors", 
                "errors": validation_errors
            }), 400
        
        print(f"🔍 RECEIVED DATA FROM FRONTEND:")
        print(f"   Project Name: {data.get('project_name')}")
        print(f"   Report Ref: {data.get('report_ref_no')}")
        print(f"   LRU Name: {data.get('lru_name')}")
        print(f"   Part No: {data.get('part_no')}")
        print(f"   obs1: {data.get('obs1')}")
        print(f"   rem1: {data.get('rem1')}")
        print(f"   upload1: {data.get('upload1')}")
        print(f"   obs2: {data.get('obs2')}")
        print(f"   rem2: {data.get('rem2')}")
        print(f"   upload2: {data.get('upload2')}")
        print(f"   prepared_by: {data.get('prepared_by')}")
        print(f"   verified_by: {data.get('verified_by')}")
        print(f"   approved_by: {data.get('approved_by')}")
        print(f"🔍 END OF RECEIVED DATA")
        
        conn = get_db_connection()
        cur = conn.cursor()
        
        # Check if table exists first
        cur.execute("""
            SELECT EXISTS (
                SELECT FROM information_schema.tables 
                WHERE table_name = 'assembled_board_inspection_report'
            );
        """)
        table_exists = cur.fetchone()[0]
        
        if not table_exists:
            cur.close()
            return jsonify({"success": False, "message": "Table 'assembled_board_inspection_report' does not exist"}), 500
        
        print("Table exists, proceeding with insert...")  # Debug log
        
        # Insert new assembled board inspection report
        cur.execute("""
            INSERT INTO assembled_board_inspection_report (
                project_name, report_ref_no, memo_ref_no, lru_name, sru_name, dp_name,
                part_no, inspection_stage, test_venue, quantity, sl_nos, serial_number,
                start_date, end_date, dated1, dated2,
                obs1, rem1, upload1, obs2, rem2, upload2, obs3, rem3, upload3,
                obs4, rem4, upload4, obs5, rem5, upload5, obs6, rem6, upload6,
                obs7, rem7, upload7, obs8, rem8, upload8, obs9, rem9, upload9,
                obs10, rem10, upload10, obs11, rem11, upload11, obs12, rem12, upload12,
                obs13, rem13, upload13, obs14, rem14, upload14, obs15, rem15, upload15,
                obs16, rem16, upload16, obs17, rem17, upload17, obs18, rem18, upload18,
                obs19, rem19, upload19, obs20, rem20, upload20,
                prepared_by, verified_by, approved_by
            ) VALUES (
                %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
                %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
                %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
                %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
            ) RETURNING report_id
        """, (
            data.get('project_name') or None,
            data.get('report_ref_no') or None,
            data.get('memo_ref_no') or None,
            data.get('lru_name') or None,
            data.get('sru_name') or None,
            data.get('dp_name') or None,
            data.get('part_no') or None,
            data.get('inspection_stage') or None,
            data.get('test_venue') or None,
            data.get('quantity') or None,
            data.get('sl_nos') or None,
            data.get('serial_number') or None,
            data.get('start_date') or None,
            data.get('end_date') or None,
            data.get('dated1') or None,
            data.get('dated2') or None,
            # Parameters 1-20
            data.get('obs1') or None, data.get('rem1') or None, data.get('upload1') or None,
            data.get('obs2') or None, data.get('rem2') or None, data.get('upload2') or None,
            data.get('obs3') or None, data.get('rem3') or None, data.get('upload3') or None,
            data.get('obs4') or None, data.get('rem4') or None, data.get('upload4') or None,
            data.get('obs5') or None, data.get('rem5') or None, data.get('upload5') or None,
            data.get('obs6') or None, data.get('rem6') or None, data.get('upload6') or None,
            data.get('obs7') or None, data.get('rem7') or None, data.get('upload7') or None,
            data.get('obs8') or None, data.get('rem8') or None, data.get('upload8') or None,
            data.get('obs9') or None, data.get('rem9') or None, data.get('upload9') or None,
            data.get('obs10') or None, data.get('rem10') or None, data.get('upload10') or None,
            data.get('obs11') or None, data.get('rem11') or None, data.get('upload11') or None,
            data.get('obs12') or None, data.get('rem12') or None, data.get('upload12') or None,
            data.get('obs13') or None, data.get('rem13') or None, data.get('upload13') or None,
            data.get('obs14') or None, data.get('rem14') or None, data.get('upload14') or None,
            data.get('obs15') or None, data.get('rem15') or None, data.get('upload15') or None,
            data.get('obs16') or None, data.get('rem16') or None, data.get('upload16') or None,
            data.get('obs17') or None, data.get('rem17') or None, data.get('upload17') or None,
            data.get('obs18') or None, data.get('rem18') or None, data.get('upload18') or None,
            data.get('obs19') or None, data.get('rem19') or None, data.get('upload19') or None,
            data.get('obs20') or None, data.get('rem20') or None, data.get('upload20') or None,
            # Signatories
            data.get('prepared_by') or None,
            data.get('verified_by') or None,
            data.get('approved_by') or None
        ))
        
        print("Insert query executed successfully")  # Debug log
        
        # Get the inserted report ID from RETURNING clause
        report_id = cur.fetchone()[0]
        
        # Log assembled board report submission activity
        from utils.activity_logger import log_activity
        report_name = data.get('report_ref_no') or f"Assembled Board Report {report_id}"
        log_activity(
            project_id=None,  # Report operations don't have project_id in this context
            activity_performed="Report Submitted",
            performed_by=data.get('prepared_by', 1002),  # Default to admin if not provided
            additional_info=f"ID:{report_id}|Name:{report_name}|Assembled Board Report '{report_name}' (ID: {report_id}) was submitted"
        )
        
        conn.commit()
        cur.close()
        
        print(f"Report created with ID: {report_id}")  # Debug log
        
        return jsonify({
            "success": True,
            "message": "Assembled board inspection report created successfully",
            "report_id": report_id
        })
        
    except Exception as e:
        print(f"Error creating assembled board inspection report: {str(e)}")
        import traceback
        traceback.print_exc()  # Print full traceback for debugging
        return handle_database_error(get_db_connection(), f"Error creating assembled board inspection report: {str(e)}")

@reports_bp.route('/api/reports/assembled-board/<int:report_id>', methods=['GET'])
def get_assembled_board_report(report_id):
    """Get assembled board inspection report by ID"""
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        
        cur.execute("""
            SELECT 
                report_id, project_name, report_ref_no, memo_ref_no, lru_name, sru_name, dp_name,
                part_no, inspection_stage, test_venue, quantity, sl_nos, serial_number,
                start_date, end_date, dated1, dated2,
                obs1, rem1, upload1, obs2, rem2, upload2, obs3, rem3, upload3,
                obs4, rem4, upload4, obs5, rem5, upload5, obs6, rem6, upload6,
                obs7, rem7, upload7, obs8, rem8, upload8, obs9, rem9, upload9,
                obs10, rem10, upload10, obs11, rem11, upload11, obs12, rem12, upload12,
                obs13, rem13, upload13, obs14, rem14, upload14, obs15, rem15, upload15,
                obs16, rem16, upload16, obs17, rem17, upload17, obs18, rem18, upload18,
                obs19, rem19, upload19, obs20, rem20, upload20,
                prepared_by, verified_by, approved_by, created_at, updated_at
            FROM assembled_board_inspection_report 
            WHERE report_id = %s
        """, (report_id,))
        
        report = cur.fetchone()
        cur.close()
        
        if not report:
            return jsonify({"success": False, "message": "Report not found"}), 404
        
        # Convert to dictionary
        report_data = {
            "report_id": report[0],
            "project_name": report[1],
            "report_ref_no": report[2],
            "memo_ref_no": report[3],
            "lru_name": report[4],
            "sru_name": report[5],
            "dp_name": report[6],
            "part_no": report[7],
            "inspection_stage": report[8],
            "test_venue": report[9],
            "quantity": report[10],
            "sl_nos": report[11],
            "serial_number": report[12],
            "start_date": report[13].isoformat() if report[13] else None,
            "end_date": report[14].isoformat() if report[14] else None,
            "dated1": report[15].isoformat() if report[15] else None,
            "dated2": report[16].isoformat() if report[16] else None,
            # Parameters 1-20
            "obs1": report[17], "rem1": report[18], "upload1": report[19],
            "obs2": report[20], "rem2": report[21], "upload2": report[22],
            "obs3": report[23], "rem3": report[24], "upload3": report[25],
            "obs4": report[26], "rem4": report[27], "upload4": report[28],
            "obs5": report[29], "rem5": report[30], "upload5": report[31],
            "obs6": report[32], "rem6": report[33], "upload6": report[34],
            "obs7": report[35], "rem7": report[36], "upload7": report[37],
            "obs8": report[38], "rem8": report[39], "upload8": report[40],
            "obs9": report[41], "rem9": report[42], "upload9": report[43],
            "obs10": report[44], "rem10": report[45], "upload10": report[46],
            "obs11": report[47], "rem11": report[48], "upload11": report[49],
            "obs12": report[50], "rem12": report[51], "upload12": report[52],
            "obs13": report[53], "rem13": report[54], "upload13": report[55],
            "obs14": report[56], "rem14": report[57], "upload14": report[58],
            "obs15": report[59], "rem15": report[60], "upload15": report[61],
            "obs16": report[62], "rem16": report[63], "upload16": report[64],
            "obs17": report[65], "rem17": report[66], "upload17": report[67],
            "obs18": report[68], "rem18": report[69], "upload18": report[70],
            "obs19": report[71], "rem19": report[72], "upload19": report[73],
            "obs20": report[74], "rem20": report[75], "upload20": report[76],
            # Signatories
            "prepared_by": report[77],
            "verified_by": report[78],
            "approved_by": report[79],
            "created_at": report[80].isoformat() if report[80] else None,
            "updated_at": report[81].isoformat() if report[81] else None
        }
        
        return jsonify({
            "success": True,
            "report": report_data
        })
        
    except Exception as e:
        print(f"Error fetching assembled board inspection report: {str(e)}")
        return handle_database_error(get_db_connection(), f"Error fetching assembled board inspection report: {str(e)}")

@reports_bp.route('/api/reports/assembled-board/<int:report_id>', methods=['PUT'])
@require_design_head_role
def update_assembled_board_report(report_id):
    """Update assembled board inspection report"""
    try:
        data = request.json
        if not data:
            return jsonify({"success": False, "message": "No data provided"}), 400
        
        # Validate the data
        validation_errors = validate_assembled_board_data(data)
        if validation_errors:
            return jsonify({
                "success": False, 
                "message": "Validation errors", 
                "errors": validation_errors
            }), 400
        
        conn = get_db_connection()
        cur = conn.cursor()
        
        # Build dynamic update query based on provided fields
        update_fields = []
        update_values = []
        
        # Header fields
        header_fields = [
            'project_name', 'report_ref_no', 'memo_ref_no', 'lru_name', 'sru_name', 'dp_name',
            'part_no', 'inspection_stage', 'test_venue', 'quantity', 'sl_nos', 'serial_number',
            'start_date', 'end_date', 'dated1', 'dated2'
        ]
        
        for field in header_fields:
            if field in data:
                update_fields.append(f"{field} = %s")
                update_values.append(data[field] or None)
        
        # Parameter fields (obs1-20, rem1-20, upload1-20)
        for i in range(1, 21):
            for prefix in ['obs', 'rem', 'upload']:
                field = f"{prefix}{i}"
                if field in data:
                    update_fields.append(f"{field} = %s")
                    update_values.append(data[field] or None)
        
        # Signatory fields
        signatory_fields = ['prepared_by', 'verified_by', 'approved_by']
        for field in signatory_fields:
            if field in data:
                update_fields.append(f"{field} = %s")
                update_values.append(data[field] or None)
        
        if not update_fields:
            cur.close()
            return jsonify({"success": False, "message": "No fields to update"}), 400
        
        # Add updated_at timestamp
        update_fields.append("updated_at = CURRENT_TIMESTAMP")
        
        # Execute update
        update_query = f"UPDATE assembled_board_inspection_report SET {', '.join(update_fields)} WHERE report_id = %s"
        update_values.append(report_id)
        
        cur.execute(update_query, update_values)
        
        if cur.rowcount == 0:
            cur.close()
            return jsonify({"success": False, "message": "Report not found"}), 404
        
        conn.commit()
        cur.close()
        
        return jsonify({
            "success": True,
            "message": "Assembled board inspection report updated successfully"
        })
        
    except Exception as e:
        print(f"Error updating assembled board inspection report: {str(e)}")
        return handle_database_error(get_db_connection(), f"Error updating assembled board inspection report: {str(e)}")

@reports_bp.route('/api/reports/assembled-board', methods=['GET'])
def get_all_assembled_board_reports():
    """Get all assembled board inspection reports with optional filtering"""
    try:
        # Get query parameters for filtering
        project_name = request.args.get('project_name')
        report_ref_no = request.args.get('report_ref_no')
        lru_name = request.args.get('lru_name')
        inspection_stage = request.args.get('inspection_stage')
        limit = request.args.get('limit', type=int, default=50)
        offset = request.args.get('offset', type=int, default=0)
        
        conn = get_db_connection()
        cur = conn.cursor()
        
        # Build query with optional filters
        base_query = """
            SELECT 
                report_id, project_name, report_ref_no, memo_ref_no, lru_name, sru_name, dp_name,
                part_no, inspection_stage, test_venue, quantity, sl_nos, serial_number,
                start_date, end_date, dated1, dated2,
                prepared_by, verified_by, approved_by, created_at, updated_at
            FROM assembled_board_inspection_report
        """
        
        where_conditions = []
        query_params = []
        
        if project_name:
            where_conditions.append("project_name ILIKE %s")
            query_params.append(f"%{project_name}%")
        
        if report_ref_no:
            where_conditions.append("report_ref_no ILIKE %s")
            query_params.append(f"%{report_ref_no}%")
        
        if lru_name:
            where_conditions.append("lru_name ILIKE %s")
            query_params.append(f"%{lru_name}%")
        
        if inspection_stage:
            where_conditions.append("inspection_stage ILIKE %s")
            query_params.append(f"%{inspection_stage}%")
        
        if where_conditions:
            base_query += " WHERE " + " AND ".join(where_conditions)
        
        base_query += " ORDER BY created_at DESC LIMIT %s OFFSET %s"
        query_params.extend([limit, offset])
        
        cur.execute(base_query, query_params)
        reports = cur.fetchall()
        
        # Get total count for pagination
        count_query = "SELECT COUNT(*) FROM assembled_board_inspection_report"
        if where_conditions:
            count_query += " WHERE " + " AND ".join(where_conditions)
        
        cur.execute(count_query, query_params[:-2])  # Exclude limit and offset
        total_count = cur.fetchone()[0]
        
        cur.close()
        
        # Convert to list of dictionaries
        report_list = []
        for report in reports:
            report_list.append({
                "report_id": report[0],
                "project_name": report[1],
                "report_ref_no": report[2],
                "memo_ref_no": report[3],
                "lru_name": report[4],
                "sru_name": report[5],
                "dp_name": report[6],
                "part_no": report[7],
                "inspection_stage": report[8],
                "test_venue": report[9],
                "quantity": report[10],
                "sl_nos": report[11],
                "serial_number": report[12],
                "start_date": report[13].isoformat() if report[13] else None,
                "end_date": report[14].isoformat() if report[14] else None,
                "dated1": report[15].isoformat() if report[15] else None,
                "dated2": report[16].isoformat() if report[16] else None,
                "prepared_by": report[17],
                "verified_by": report[18],
                "approved_by": report[19],
                "created_at": report[20].isoformat() if report[20] else None,
                "updated_at": report[21].isoformat() if report[21] else None
            })
        
        return jsonify({
            "success": True,
            "reports": report_list,
            "total_count": total_count,
            "limit": limit,
            "offset": offset
        })
        
    except Exception as e:
        print(f"Error fetching assembled board inspection reports: {str(e)}")
        return handle_database_error(get_db_connection(), f"Error fetching assembled board inspection reports: {str(e)}")

@reports_bp.route('/api/reports/assembled-board/count', methods=['GET'])
def get_assembled_board_report_count():
    """Get count of assembled board inspection reports"""
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        
        cur.execute("SELECT COUNT(*) FROM assembled_board_inspection_report")
        count = cur.fetchone()[0]
        
        cur.close()
        
        return jsonify({
            "success": True,
            "count": count,
            "message": f"Found {count} assembled board inspection reports"
        })
        
    except Exception as e:
        print(f"Error getting report count: {str(e)}")
        return handle_database_error(get_db_connection(), f"Error getting report count: {str(e)}")

@reports_bp.route('/api/reports/assembled-board/upload', methods=['POST'])
@require_design_head_role
def upload_assembled_board_file():
    """Upload file for assembled board inspection report"""
    try:
        if 'file' not in request.files:
            return jsonify({"success": False, "message": "No file provided"}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({"success": False, "message": "No file selected"}), 400
        
        # Get the upload field name (upload1, upload2, etc.)
        upload_field = request.form.get('upload_field')
        if not upload_field or not upload_field.startswith('upload'):
            return jsonify({"success": False, "message": "Invalid upload field specified"}), 400
        
        # Validate file type
        if not allowed_file(file.filename):
            return jsonify({"success": False, "message": "File type not allowed. Allowed types: PDF, DOC, DOCX, TXT, XLSX, XLS"}), 400
        
        # Check file size
        if not validate_file_size(file, Config.MAX_FILE_SIZE):
            return jsonify({"success": False, "message": f"File too large. Maximum size is {Config.MAX_FILE_SIZE // (1024*1024)}MB"}), 400
        
        # Create upload directory if it doesn't exist
        upload_dir = os.path.join(Config.UPLOAD_FOLDER, 'assembled_board_reports')
        os.makedirs(upload_dir, exist_ok=True)
        
        # Generate unique filename
        file_extension = file.filename.rsplit('.', 1)[1].lower()
        unique_filename = f"{upload_field}_{uuid.uuid4().hex}.{file_extension}"
        file_path = os.path.join(upload_dir, unique_filename)
        
        # Save file
        file.save(file_path)
        
        # Return the relative path for database storage
        relative_path = f"assembled_board_reports/{unique_filename}"
        
        return jsonify({
            "success": True,
            "message": "File uploaded successfully",
            "file_path": relative_path,
            "upload_field": upload_field
        })
        
    except Exception as e:
        print(f"Error uploading file: {str(e)}")
        return jsonify({"success": False, "message": f"Upload error: {str(e)}"}), 500

@reports_bp.route('/api/reports/assembled-board/files/<path:filename>', methods=['GET'])
def serve_assembled_board_file(filename):
    """Serve uploaded files for assembled board inspection reports"""
    try:
        # Clean the filename - remove any path separators
        clean_filename = os.path.basename(filename)
        file_path = os.path.join(Config.UPLOAD_FOLDER, 'assembled_board_reports', clean_filename)
        
        # Security check - ensure file is within upload directory
        abs_upload_folder = os.path.abspath(os.path.join(Config.UPLOAD_FOLDER, 'assembled_board_reports'))
        abs_file_path = os.path.abspath(file_path)
        
        if not abs_file_path.startswith(abs_upload_folder):
            return jsonify({"success": False, "message": "Invalid file path"}), 403
        
        if not os.path.exists(file_path):
            return jsonify({"success": False, "message": f"File not found: {clean_filename}"}), 404
        
        from flask import send_file
        return send_file(file_path, as_attachment=True)
        
    except Exception as e:
        print(f"Error serving file: {str(e)}")
        return jsonify({"success": False, "message": f"Error serving file: {str(e)}"}), 500

def validate_assembled_board_data(data):
    """Validate assembled board inspection report data"""
    errors = []
    
    # Validate remarks fields (rem1-rem20) - should be 'OK' or 'NOT OK' only if provided
    for i in range(1, 21):
        rem_field = f"rem{i}"
        if rem_field in data and data[rem_field] and data[rem_field].strip():
            if data[rem_field] not in ['OK', 'NOT OK']:
                errors.append(f"{rem_field} must be either 'OK' or 'NOT OK'")
    
    # Validate required header fields (only if provided)
    required_fields = ['project_name', 'report_ref_no', 'lru_name', 'part_no']
    for field in required_fields:
        if field in data and data[field] and not data[field].strip():
            errors.append(f"{field} cannot be empty if provided")
    
    # Validate dates (only if provided)
    date_fields = ['start_date', 'end_date', 'dated1', 'dated2']
    for field in date_fields:
        if field in data and data[field] and data[field].strip():
            try:
                from datetime import datetime
                datetime.strptime(data[field], '%Y-%m-%d')
            except ValueError:
                errors.append(f"{field} must be in YYYY-MM-DD format")
    
    # Validate quantity (only if provided)
    if 'quantity' in data and data['quantity'] is not None and str(data['quantity']).strip():
        try:
            quantity = int(data['quantity'])
            if quantity < 0:
                errors.append("quantity must be a positive number")
        except (ValueError, TypeError):
            errors.append("quantity must be a valid number")
    
    return errors

def validate_cot_screening_data(data):
    """Validate COT screening inspection report data"""
    errors = []
    
    # Validate remarks fields (rem1-rem3) - should be 'OK' or 'NOT OK' only if provided
    for i in range(1, 4):
        rem_field = f"rem{i}"
        if rem_field in data and data[rem_field] and data[rem_field].strip():
            if data[rem_field] not in ['OK', 'NOT OK']:
                errors.append(f"{rem_field} must be either 'OK' or 'NOT OK'")
    
    # Validate required header fields (only if provided)
    required_fields = ['project_name', 'report_ref_no', 'lru_name', 'part_no']
    for field in required_fields:
        if field in data and data[field] and not data[field].strip():
            errors.append(f"{field} cannot be empty if provided")
    
    # Validate dates (only if provided)
    date_fields = ['start_date', 'end_date', 'dated1', 'dated2']
    for field in date_fields:
        if field in data and data[field] and data[field].strip():
            try:
                from datetime import datetime
                datetime.strptime(data[field], '%Y-%m-%d')
            except ValueError:
                errors.append(f"{field} must be in YYYY-MM-DD format")
    
    # Validate quantity (only if provided)
    if 'quantity' in data and data['quantity'] is not None and str(data['quantity']).strip():
        try:
            quantity = int(data['quantity'])
            if quantity < 0:
                errors.append("quantity must be a positive number")
        except (ValueError, TypeError):
            errors.append("quantity must be a valid number")
    
    return errors

# COT Screening Inspection Report Routes

@reports_bp.route('/api/reports/cot-screening', methods=['POST'])
@require_design_head_role
def create_cot_screening_report():
    """Create a new COT screening inspection report"""
    try:
        print("🚀 COT SCREENING REPORT ENDPOINT CALLED!")
        print(f"   Method: {request.method}")
        print(f"   Headers: {dict(request.headers)}")
        print(f"   User Role: {request.args.get('user_role')}")
        
        data = request.json
        if not data:
            print("❌ NO DATA PROVIDED IN REQUEST")
            return jsonify({"success": False, "message": "No data provided"}), 400
        
        # Validate the data
        validation_errors = validate_cot_screening_data(data)
        if validation_errors:
            return jsonify({
                "success": False, 
                "message": "Validation errors", 
                "errors": validation_errors
            }), 400
        
        print(f"🔍 RECEIVED COT SCREENING DATA FROM FRONTEND:")
        print(f"   Project Name: {data.get('project_name')}")
        print(f"   Report Ref: {data.get('report_ref_no')}")
        print(f"   LRU Name: {data.get('lru_name')}")
        print(f"   Part No: {data.get('part_no')}")
        print(f"   rem1: {data.get('rem1')}")
        print(f"   upload1: {data.get('upload1')}")
        print(f"   rem2: {data.get('rem2')}")
        print(f"   upload2: {data.get('upload2')}")
        print(f"   rem3: {data.get('rem3')}")
        print(f"   upload3: {data.get('upload3')}")
        print(f"   prepared_by: {data.get('prepared_by')}")
        print(f"   verified_by: {data.get('verified_by')}")
        print(f"   approved_by: {data.get('approved_by')}")
        print(f"🔍 END OF RECEIVED DATA")
        
        conn = get_db_connection()
        cur = conn.cursor()
        
        # Check if table exists first
        cur.execute("""
            SELECT EXISTS (
                SELECT FROM information_schema.tables 
                WHERE table_name = 'cot_screening_inspection_report'
            );
        """)
        
        table_exists = cur.fetchone()[0]
        if not table_exists:
            print("❌ COT screening table does not exist!")
            cur.close()
            conn.close()
            return jsonify({"success": False, "message": "COT screening table does not exist"}), 500
        
        print("Table exists, proceeding with insert...")
        
        # Insert the report data
        cur.execute("""
            INSERT INTO cot_screening_inspection_report (
                project_name, report_ref_no, memo_ref_no, lru_name, sru_name, dp_name,
                part_no, inspection_stage, test_venue, quantity, sl_nos, serial_number,
                start_date, end_date, dated1, dated2,
                test_nature1, test_nature2, test_nature3,
                rem1, upload1, rem2, upload2, rem3, upload3,
                prepared_by, verified_by, approved_by
            ) VALUES (
                %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
                %s, %s, %s,
                %s, %s, %s, %s, %s, %s,
                %s, %s, %s
            ) RETURNING report_id
        """, (
            data.get('project_name') or None,
            data.get('report_ref_no') or None,
            data.get('memo_ref_no') or None,
            data.get('lru_name') or None,
            data.get('sru_name') or None,
            data.get('dp_name') or None,
            data.get('part_no') or None,
            data.get('inspection_stage') or None,
            data.get('test_venue') or None,
            data.get('quantity') or None,
            data.get('sl_nos') or None,
            data.get('serial_number') or None,
            data.get('start_date') or None,
            data.get('end_date') or None,
            data.get('dated1') or None,
            data.get('dated2') or None,
            # Test nature fields
            data.get('test_nature1') or None,
            data.get('test_nature2') or None,
            data.get('test_nature3') or None,
            # Checklist parameters
            data.get('rem1') or None,
            data.get('upload1') or None,
            data.get('rem2') or None,
            data.get('upload2') or None,
            data.get('rem3') or None,
            data.get('upload3') or None,
            # Signatories
            data.get('prepared_by') or None,
            data.get('verified_by') or None,
            data.get('approved_by') or None
        ))
        
        report_id = cur.fetchone()[0]
        
        # Log COT screening report submission activity
        from utils.activity_logger import log_activity
        report_name = data.get('report_ref_no') or f"COT Screening Report {report_id}"
        log_activity(
            project_id=None,  # Report operations don't have project_id in this context
            activity_performed="Report Submitted",
            performed_by=data.get('prepared_by', 1002),  # Default to admin if not provided
            additional_info=f"ID:{report_id}|Name:{report_name}|COT Screening Report '{report_name}' (ID: {report_id}) was submitted"
        )
        
        conn.commit()
        
        print(f"Insert query executed successfully")
        print(f"Report created with ID: {report_id}")
        
        cur.close()
        conn.close()
        
        return jsonify({
            "success": True,
            "message": "COT screening inspection report created successfully",
            "report_id": report_id
        }), 201
        
    except Exception as e:
        print(f"Error creating COT screening report: {str(e)}")
        return handle_database_error(get_db_connection(), f"Error creating COT screening report: {str(e)}")

@reports_bp.route('/api/reports/cot-screening/<int:report_id>', methods=['GET'])
def get_cot_screening_report(report_id):
    """Get a specific COT screening inspection report by ID"""
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        
        cur.execute("""
            SELECT 
                report_id, project_name, report_ref_no, memo_ref_no, lru_name, sru_name, dp_name,
                part_no, inspection_stage, test_venue, quantity, sl_nos, serial_number,
                start_date, end_date, dated1, dated2,
                test_nature1, test_nature2, test_nature3,
                rem1, upload1, rem2, upload2, rem3, upload3,
                prepared_by, verified_by, approved_by,
                created_at, updated_at
            FROM cot_screening_inspection_report 
            WHERE report_id = %s
        """, (report_id,))
        
        report = cur.fetchone()
        
        if not report:
            cur.close()
            conn.close()
            return jsonify({"success": False, "message": "Report not found"}), 404
        
        # Convert to dictionary
        report_data = {
            "report_id": report[0],
            "project_name": report[1],
            "report_ref_no": report[2],
            "memo_ref_no": report[3],
            "lru_name": report[4],
            "sru_name": report[5],
            "dp_name": report[6],
            "part_no": report[7],
            "inspection_stage": report[8],
            "test_venue": report[9],
            "quantity": report[10],
            "sl_nos": report[11],
            "serial_number": report[12],
            "start_date": report[13].isoformat() if report[13] else None,
            "end_date": report[14].isoformat() if report[14] else None,
            "dated1": report[15].isoformat() if report[15] else None,
            "dated2": report[16].isoformat() if report[16] else None,
            "test_nature1": report[17],
            "test_nature2": report[18],
            "test_nature3": report[19],
            "rem1": report[20],
            "upload1": report[21],
            "rem2": report[22],
            "upload2": report[23],
            "rem3": report[24],
            "upload3": report[25],
            "prepared_by": report[26],
            "verified_by": report[27],
            "approved_by": report[28],
            "created_at": report[29].isoformat() if report[29] else None,
            "updated_at": report[30].isoformat() if report[30] else None
        }
        
        cur.close()
        conn.close()
        
        return jsonify({
            "success": True,
            "report": report_data
        })
        
    except Exception as e:
        print(f"Error fetching COT screening report: {str(e)}")
        return handle_database_error(get_db_connection(), f"Error fetching COT screening report: {str(e)}")

@reports_bp.route('/api/reports/cot-screening/<int:report_id>', methods=['PUT'])
@require_design_head_role
def update_cot_screening_report(report_id):
    """Update a COT screening inspection report"""
    try:
        data = request.json
        if not data:
            return jsonify({"success": False, "message": "No data provided"}), 400
        
        # Validate the data
        validation_errors = validate_cot_screening_data(data)
        if validation_errors:
            return jsonify({
                "success": False, 
                "message": "Validation errors", 
                "errors": validation_errors
            }), 400
        
        conn = get_db_connection()
        cur = conn.cursor()
        
        # Build dynamic update query based on provided fields
        update_fields = []
        update_values = []
        
        # Header fields
        header_fields = [
            'project_name', 'report_ref_no', 'memo_ref_no', 'lru_name', 'sru_name', 'dp_name',
            'part_no', 'inspection_stage', 'test_venue', 'quantity', 'sl_nos', 'serial_number',
            'start_date', 'end_date', 'dated1', 'dated2'
        ]
        
        for field in header_fields:
            if field in data:
                update_fields.append(f"{field} = %s")
                update_values.append(data[field] or None)
        
        # Test nature fields
        test_nature_fields = ['test_nature1', 'test_nature2', 'test_nature3']
        for field in test_nature_fields:
            if field in data:
                update_fields.append(f"{field} = %s")
                update_values.append(data[field] or None)
        
        # Parameter fields (rem1-3, upload1-3)
        for i in range(1, 4):
            for prefix in ['rem', 'upload']:
                field = f"{prefix}{i}"
                if field in data:
                    update_fields.append(f"{field} = %s")
                    update_values.append(data[field] or None)
        
        # Signatory fields
        signatory_fields = ['prepared_by', 'verified_by', 'approved_by']
        for field in signatory_fields:
            if field in data:
                update_fields.append(f"{field} = %s")
                update_values.append(data[field] or None)
        
        if not update_fields:
            cur.close()
            conn.close()
            return jsonify({"success": False, "message": "No fields to update"}), 400
        
        # Add report_id to the values
        update_values.append(report_id)
        
        # Execute update
        update_query = f"""
            UPDATE cot_screening_inspection_report 
            SET {', '.join(update_fields)}
            WHERE report_id = %s
        """
        
        cur.execute(update_query, update_values)
        
        if cur.rowcount == 0:
            cur.close()
            conn.close()
            return jsonify({"success": False, "message": "Report not found"}), 404
        
        conn.commit()
        cur.close()
        conn.close()
        
        return jsonify({
            "success": True,
            "message": "COT screening inspection report updated successfully"
        })
        
    except Exception as e:
        print(f"Error updating COT screening report: {str(e)}")
        return handle_database_error(get_db_connection(), f"Error updating COT screening report: {str(e)}")

@reports_bp.route('/api/reports/cot-screening', methods=['GET'])
def get_all_cot_screening_reports():
    """Get all COT screening inspection reports with optional filtering"""
    try:
        # Get query parameters
        project_name = request.args.get('project_name')
        status = request.args.get('status')
        limit = request.args.get('limit', type=int)
        offset = request.args.get('offset', type=int, default=0)
        
        conn = get_db_connection()
        cur = conn.cursor()
        
        # Build query with filters
        where_conditions = []
        query_params = []
        
        if project_name:
            where_conditions.append("project_name ILIKE %s")
            query_params.append(f"%{project_name}%")
        
        where_clause = ""
        if where_conditions:
            where_clause = "WHERE " + " AND ".join(where_conditions)
        
        # Add pagination
        limit_clause = ""
        if limit:
            limit_clause = f"LIMIT {limit} OFFSET {offset}"
        
        query = f"""
            SELECT 
                report_id, project_name, report_ref_no, lru_name, part_no,
                inspection_stage, test_venue, quantity, created_at
            FROM cot_screening_inspection_report 
            {where_clause}
            ORDER BY created_at DESC
            {limit_clause}
        """
        
        cur.execute(query, query_params)
        reports = cur.fetchall()
        
        # Convert to list of dictionaries
        report_list = []
        for report in reports:
            report_list.append({
                "report_id": report[0],
                "project_name": report[1],
                "report_ref_no": report[2],
                "lru_name": report[3],
                "part_no": report[4],
                "inspection_stage": report[5],
                "test_venue": report[6],
                "quantity": report[7],
                "created_at": report[8].isoformat() if report[8] else None
            })
        
        cur.close()
        conn.close()
        
        return jsonify({
            "success": True,
            "reports": report_list,
            "count": len(report_list)
        })
        
    except Exception as e:
        print(f"Error fetching COT screening reports: {str(e)}")
        return handle_database_error(get_db_connection(), f"Error fetching COT screening reports: {str(e)}")

@reports_bp.route('/api/reports/cot-screening/count', methods=['GET'])
def get_cot_screening_report_count():
    """Get count of COT screening inspection reports"""
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        
        cur.execute("SELECT COUNT(*) FROM cot_screening_inspection_report")
        count = cur.fetchone()[0]
        
        cur.close()
        conn.close()
        
        return jsonify({
            "success": True,
            "count": count
        })
        
    except Exception as e:
        print(f"Error getting COT screening report count: {str(e)}")
        return handle_database_error(get_db_connection(), f"Error getting COT screening report count: {str(e)}")

@reports_bp.route('/api/reports/cot-screening/<int:report_id>/upload', methods=['POST'])
@require_design_head_role
def upload_cot_screening_file(report_id):
    """Upload file for COT screening inspection report"""
    try:
        if 'file' not in request.files:
            return jsonify({"success": False, "message": "No file provided"}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({"success": False, "message": "No file selected"}), 400
        
        if not allowed_file(file.filename):
            return jsonify({"success": False, "message": "File type not allowed"}), 400
        
        # Validate file size
        file.seek(0, 2)  # Seek to end
        file_size = file.tell()
        file.seek(0)  # Reset to beginning
        
        if not validate_file_size(file_size):
            return jsonify({"success": False, "message": "File too large"}), 400
        
        # Generate unique filename
        file_extension = os.path.splitext(file.filename)[1]
        unique_filename = f"cot_screening_{report_id}_{uuid.uuid4().hex}{file_extension}"
        
        # Create upload directory if it doesn't exist
        upload_dir = os.path.join(Config.UPLOAD_FOLDER, 'cot_screening')
        os.makedirs(upload_dir, exist_ok=True)
        
        # Save file
        file_path = os.path.join(upload_dir, unique_filename)
        file.save(file_path)
        
        # Update database with file path
        conn = get_db_connection()
        cur = conn.cursor()
        
        # Determine which upload field to update based on the field parameter
        upload_field = request.form.get('field', 'upload1')
        if upload_field not in ['upload1', 'upload2', 'upload3']:
            upload_field = 'upload1'
        
        cur.execute(f"""
            UPDATE cot_screening_inspection_report 
            SET {upload_field} = %s 
            WHERE report_id = %s
        """, (file_path, report_id))
        
        if cur.rowcount == 0:
            cur.close()
            conn.close()
            os.remove(file_path)  # Clean up file
            return jsonify({"success": False, "message": "Report not found"}), 404
        
        conn.commit()
        cur.close()
        conn.close()
        
        return jsonify({
            "success": True,
            "message": "File uploaded successfully",
            "file_path": file_path,
            "field": upload_field
        })
        
    except Exception as e:
        print(f"Error uploading COT screening file: {str(e)}")
        return jsonify({"success": False, "message": f"Error uploading file: {str(e)}"}), 500

@reports_bp.route('/api/reports/cot-screening/files/<path:filename>', methods=['GET'])
def serve_cot_screening_file(filename):
    """Serve uploaded COT screening files"""
    try:
        file_path = os.path.join(Config.UPLOAD_FOLDER, 'cot_screening', filename)
        
        if not os.path.exists(file_path):
            return jsonify({"success": False, "message": "File not found"}), 404
        
        return send_file(file_path)
        
    except Exception as e:
        print(f"Error serving file: {str(e)}")
        return jsonify({"success": False, "message": f"Error serving file: {str(e)}"}), 500

@reports_bp.route('/api/reports/bare-pcb-inspection', methods=['POST'])
def create_bare_pcb_inspection_report():
    """Create a new bare PCB inspection report"""
    try:
        data = request.json
        if not data:
            return jsonify({"success": False, "message": "No data provided"}), 400
        
        # Validate required fields
        required_fields = ['project_name', 'report_ref_no', 'memo_ref_no', 'lru_name', 'dp_name', 'sru_name', 'part_no']
        for field in required_fields:
            if field not in data or not data[field]:
                return jsonify({"success": False, "message": f"Missing required field: {field}"}), 400
        
        conn = get_db_connection()
        cur = conn.cursor()
        
        # Insert bare PCB inspection report
        cur.execute("""
            INSERT INTO bare_pcb_inspection_report (
                project_name, report_ref_no, memo_ref_no, lru_name, sru_name, dp_name, 
                part_no, inspection_stage, test_venue, quantity, sl_nos, serial_number, 
                inspection_count, start_date, end_date, dated1, dated2,
                obs1, rem1, upload1, obs2, rem2, upload2, obs3, rem3, upload3,
                obs4, rem4, upload4, obs5, rem5, upload5, obs6, rem6, upload6,
                obs7, rem7, upload7, obs8, rem8, upload8, obs9, rem9, upload9,
                obs10, rem10, upload10, obs11, rem11, upload11, obs12, rem12, upload12,
                overall_status, quality_rating, recommendations,
                prepared_by, verified_by, approved_by, created_at, updated_at
            ) VALUES (
                %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
                %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
                %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
                %s, %s, %s, %s, %s, %s, NOW(), NOW()
            ) RETURNING report_id
        """, (
            data['project_name'],
            data['report_ref_no'],
            data['memo_ref_no'],
            data['lru_name'],
            data['sru_name'],
            data['dp_name'],
            data['part_no'],
            data.get('inspection_stage'),
            data.get('test_venue'),
            data.get('quantity'),
            data.get('sl_nos'),
            data.get('serial_number'),
            data.get('inspection_count'),
            data.get('start_date'),
            data.get('end_date'),
            data.get('dated1'),
            data.get('dated2'),
            # Visual Inspection (10 items)
            data.get('visual_inspection', [{}])[0].get('observation', ''),
            data.get('visual_inspection', [{}])[0].get('remarks', ''),
            data.get('visual_inspection', [{}])[0].get('upload', ''),
            data.get('visual_inspection', [{}])[1].get('observation', ''),
            data.get('visual_inspection', [{}])[1].get('remarks', ''),
            data.get('visual_inspection', [{}])[1].get('upload', ''),
            data.get('visual_inspection', [{}])[2].get('observation', ''),
            data.get('visual_inspection', [{}])[2].get('remarks', ''),
            data.get('visual_inspection', [{}])[2].get('upload', ''),
            data.get('visual_inspection', [{}])[3].get('observation', ''),
            data.get('visual_inspection', [{}])[3].get('remarks', ''),
            data.get('visual_inspection', [{}])[3].get('upload', ''),
            data.get('visual_inspection', [{}])[4].get('observation', ''),
            data.get('visual_inspection', [{}])[4].get('remarks', ''),
            data.get('visual_inspection', [{}])[4].get('upload', ''),
            data.get('visual_inspection', [{}])[5].get('observation', ''),
            data.get('visual_inspection', [{}])[5].get('remarks', ''),
            data.get('visual_inspection', [{}])[5].get('upload', ''),
            data.get('visual_inspection', [{}])[6].get('observation', ''),
            data.get('visual_inspection', [{}])[6].get('remarks', ''),
            data.get('visual_inspection', [{}])[6].get('upload', ''),
            data.get('visual_inspection', [{}])[7].get('observation', ''),
            data.get('visual_inspection', [{}])[7].get('remarks', ''),
            data.get('visual_inspection', [{}])[7].get('upload', ''),
            data.get('visual_inspection', [{}])[8].get('observation', ''),
            data.get('visual_inspection', [{}])[8].get('remarks', ''),
            data.get('visual_inspection', [{}])[8].get('upload', ''),
            data.get('visual_inspection', [{}])[9].get('observation', ''),
            data.get('visual_inspection', [{}])[9].get('remarks', ''),
            data.get('visual_inspection', [{}])[9].get('upload', ''),
            # Continuity Check (1 item)
            data.get('continuity_check', [{}])[0].get('observation', ''),
            data.get('continuity_check', [{}])[0].get('remarks', ''),
            data.get('continuity_check', [{}])[0].get('upload', ''),
            # Fabricator Report (1 item)
            data.get('fabricator_report', {}).get('observation', ''),
            data.get('fabricator_report', {}).get('remarks', ''),
            data.get('fabricator_report', {}).get('upload', ''),
            # Summary fields
            data.get('overall_status'),
            data.get('quality_rating'),
            data.get('recommendations'),
            # Signatures
            data.get('prepared_by'),
            data.get('verified_by'),
            data.get('approved_by')
        ))
        
        report_id = cur.fetchone()[0]
        
        # Log bare PCB report submission activity
        from utils.activity_logger import log_activity
        report_name = data.get('report_ref_no') or f"Bare PCB Report {report_id}"
        log_activity(
            project_id=None,  # Report operations don't have project_id in this context
            activity_performed="Report Submitted",
            performed_by=data.get('prepared_by', 1002),  # Default to admin if not provided
            additional_info=f"ID:{report_id}|Name:{report_name}|Bare PCB Report '{report_name}' (ID: {report_id}) was submitted"
        )
        
        conn.commit()
        cur.close()
        
        return jsonify({
            "success": True,
            "message": "Bare PCB inspection report created successfully",
            "report_id": report_id
        })
        
    except Exception as e:
        print(f"Error creating bare PCB inspection report: {str(e)}")
        return handle_database_error(get_db_connection(), f"Error creating bare PCB inspection report: {str(e)}")

@reports_bp.route('/api/reports/bare-pcb-inspection/<int:report_id>', methods=['GET'])
def get_bare_pcb_inspection_report(report_id):
    """Get bare PCB inspection report details"""
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        
        cur.execute("""
            SELECT * FROM bare_pcb_inspection_report WHERE report_id = %s
        """, (report_id,))
        
        report = cur.fetchone()
        cur.close()
        
        if not report:
            return jsonify({"success": False, "message": "Report not found"}), 404
        
        # Convert to dictionary
        columns = [desc[0] for desc in cur.description] if cur.description else []
        report_data = dict(zip(columns, report))
        
        # Convert datetime objects to strings
        for key, value in report_data.items():
            if hasattr(value, 'isoformat'):
                report_data[key] = value.isoformat()
        
        return jsonify({
            "success": True,
            "report": report_data
        })
        
    except Exception as e:
        print(f"Error fetching bare PCB inspection report: {str(e)}")
        return handle_database_error(get_db_connection(), f"Error fetching bare PCB inspection report: {str(e)}")

@reports_bp.route('/api/reports/bare-pcb-inspection', methods=['GET'])
def get_bare_pcb_inspection_reports():
    """Get all bare PCB inspection reports"""
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        
        cur.execute("""
            SELECT report_id, project_name, lru_name, report_ref_no, memo_ref_no, 
                   created_at, updated_at
            FROM bare_pcb_inspection_report 
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
                "report_ref_no": report[3],
                "memo_ref_no": report[4],
                "created_at": report[5].isoformat() if report[5] else None,
                "updated_at": report[6].isoformat() if report[6] else None
            })
        
        return jsonify({
            "success": True,
            "reports": report_list
        })
        
    except Exception as e:
        print(f"Error fetching bare PCB inspection reports: {str(e)}")
        return handle_database_error(get_db_connection(), f"Error fetching bare PCB inspection reports: {str(e)}")

# Conformal Coating Inspection Report API Endpoints

@reports_bp.route('/api/reports/conformal-coating-inspection', methods=['POST'])
def create_conformal_coating_inspection_report():
    """Create a new conformal coating inspection report"""
    try:
        data = request.json
        if not data:
            return jsonify({"success": False, "message": "No data provided"}), 400
        
        # Validate required fields
        required_fields = ['project_name', 'report_ref_no', 'dp_name', 'sru_name', 'part_no']
        for field in required_fields:
            if field not in data or not data[field]:
                return jsonify({"success": False, "message": f"Missing required field: {field}"}), 400
        
        conn = get_db_connection()
        cur = conn.cursor()
        
        # Insert conformal coating inspection report
        cur.execute("""
            INSERT INTO conformal_coating_inspection_report (
                project_name, report_ref_no, memo_ref_no, lru_name, sru_name, dp_name, 
                part_no, inspection_stage, test_venue, quantity, sl_nos, serial_number, 
                start_date, end_date, dated1, dated2,
                obs1, rem1, upload1, expected1,
                obs2, rem2, upload2, expected2,
                obs3, rem3, upload3, expected3,
                obs4, rem4, upload4, expected4,
                obs5, rem5, upload5, expected5,
                obs6, rem6, upload6, expected6,
                obs7, rem7, upload7, expected7,
                obs8, rem8, upload8, expected8,
                obs9, rem9, upload9, expected9,
                overall_status, quality_rating, recommendations,
                prepared_by, verified_by, approved_by
            ) VALUES (
                %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
                %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
                %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
                %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
            ) RETURNING report_id
        """, (
            data['project_name'],
            data['report_ref_no'],
            data.get('memo_ref_no'),
            data.get('lru_name'),
            data['sru_name'],
            data['dp_name'],
            data['part_no'],
            data.get('inspection_stage'),
            data.get('test_venue'),
            data.get('quantity'),
            data.get('sl_nos'),
            data.get('serial_number'),
            data.get('start_date'),
            data.get('end_date'),
            data.get('dated1'),
            data.get('dated2'),
            # Test cases 1-9
            data.get('tests', [{}])[0].get('observation', ''),
            data.get('tests', [{}])[0].get('remark', ''),
            data.get('tests', [{}])[0].get('upload', ''),
            data.get('tests', [{}])[0].get('expected', 'Should not be there'),
            data.get('tests', [{}])[1].get('observation', ''),
            data.get('tests', [{}])[1].get('remark', ''),
            data.get('tests', [{}])[1].get('upload', ''),
            data.get('tests', [{}])[1].get('expected', 'Should not be there'),
            data.get('tests', [{}])[2].get('observation', ''),
            data.get('tests', [{}])[2].get('remark', ''),
            data.get('tests', [{}])[2].get('upload', ''),
            data.get('tests', [{}])[2].get('expected', 'Should not be there'),
            data.get('tests', [{}])[3].get('observation', ''),
            data.get('tests', [{}])[3].get('remark', ''),
            data.get('tests', [{}])[3].get('upload', ''),
            data.get('tests', [{}])[3].get('expected', 'Should not be there'),
            data.get('tests', [{}])[4].get('observation', ''),
            data.get('tests', [{}])[4].get('remark', ''),
            data.get('tests', [{}])[4].get('upload', ''),
            data.get('tests', [{}])[4].get('expected', 'Not recommended'),
            data.get('tests', [{}])[5].get('observation', ''),
            data.get('tests', [{}])[5].get('remark', ''),
            data.get('tests', [{}])[5].get('upload', ''),
            data.get('tests', [{}])[5].get('expected', 'No Deformity'),
            data.get('tests', [{}])[6].get('observation', ''),
            data.get('tests', [{}])[6].get('remark', ''),
            data.get('tests', [{}])[6].get('upload', ''),
            data.get('tests', [{}])[6].get('expected', 'No Damages'),
            data.get('tests', [{}])[7].get('observation', ''),
            data.get('tests', [{}])[7].get('remark', ''),
            data.get('tests', [{}])[7].get('upload', ''),
            data.get('tests', [{}])[7].get('expected', 'Should have linear Coating'),
            data.get('tests', [{}])[8].get('observation', ''),
            data.get('tests', [{}])[8].get('remark', ''),
            data.get('tests', [{}])[8].get('upload', ''),
            data.get('tests', [{}])[8].get('expected', '30 to 130 microns'),
            # Summary fields
            data.get('overall_status'),
            data.get('quality_rating'),
            data.get('recommendations'),
            # Signatures
            data.get('prepared_by'),
            data.get('verified_by'),
            data.get('approved_by')
        ))
        
        report_id = cur.fetchone()[0]
        
        # Log conformal coating report submission activity
        from utils.activity_logger import log_activity
        report_name = data.get('report_ref_no') or f"Conformal Coating Report {report_id}"
        log_activity(
            project_id=None,  # Report operations don't have project_id in this context
            activity_performed="Report Submitted",
            performed_by=data.get('prepared_by', 1002),  # Default to admin if not provided
            additional_info=f"ID:{report_id}|Name:{report_name}|Conformal Coating Report '{report_name}' (ID: {report_id}) was submitted"
        )
        
        conn.commit()
        cur.close()
        
        return jsonify({
            "success": True,
            "message": "Conformal coating inspection report created successfully",
            "report_id": report_id
        })
        
    except Exception as e:
        print(f"Error creating conformal coating inspection report: {str(e)}")
        return handle_database_error(get_db_connection(), f"Error creating conformal coating inspection report: {str(e)}")

@reports_bp.route('/api/reports/conformal-coating-inspection/<int:report_id>', methods=['GET'])
def get_conformal_coating_inspection_report(report_id):
    """Get conformal coating inspection report details"""
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        
        cur.execute("""
            SELECT * FROM conformal_coating_inspection_report WHERE report_id = %s
        """, (report_id,))
        
        report = cur.fetchone()
        cur.close()
        
        if not report:
            return jsonify({"success": False, "message": "Report not found"}), 404
        
        # Convert to dictionary
        columns = [desc[0] for desc in cur.description] if cur.description else []
        report_data = dict(zip(columns, report))
        
        # Convert datetime objects to strings
        for key, value in report_data.items():
            if hasattr(value, 'isoformat'):
                report_data[key] = value.isoformat()
        
        return jsonify({
            "success": True,
            "report": report_data
        })
        
    except Exception as e:
        print(f"Error fetching conformal coating inspection report: {str(e)}")
        return handle_database_error(get_db_connection(), f"Error fetching conformal coating inspection report: {str(e)}")

@reports_bp.route('/api/reports/conformal-coating-inspection', methods=['GET'])
def get_conformal_coating_inspection_reports():
    """Get all conformal coating inspection reports"""
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        
        cur.execute("""
            SELECT report_id, project_name, lru_name, report_ref_no, memo_ref_no, 
                   created_at, updated_at
            FROM conformal_coating_inspection_report 
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
                "report_ref_no": report[3],
                "memo_ref_no": report[4],
                "created_at": report[5].isoformat() if report[5] else None,
                "updated_at": report[6].isoformat() if report[6] else None
            })
        
        return jsonify({
            "success": True,
            "reports": report_list
        })
        
    except Exception as e:
        print(f"Error fetching conformal coating inspection reports: {str(e)}")
        return handle_database_error(get_db_connection(), f"Error fetching conformal coating inspection reports: {str(e)}")

# Raw Material Inspection Report API Endpoints

@reports_bp.route('/api/reports/raw-material-inspection', methods=['POST'])
def create_raw_material_inspection_report():
    """Create a new raw material inspection report"""
    try:
        data = request.json
        if not data:
            return jsonify({"success": False, "message": "No data provided"}), 400
        
        # Validate required fields
        required_fields = ['project_name', 'report_ref_no', 'memo_ref_no', 'lru_name', 'dp_name', 'sru_name', 'part_no']
        for field in required_fields:
            if field not in data or not data[field]:
                return jsonify({"success": False, "message": f"Missing required field: {field}"}), 400
        
        conn = get_db_connection()
        cur = conn.cursor()
        
        # Insert raw material inspection report
        cur.execute("""
            INSERT INTO raw_material_inspection_report (
                project_name, report_ref_no, memo_ref_no, lru_name, sru_name, dp_name, 
                part_no, inspection_stage, test_venue, quantity, sl_nos, serial_number, 
                start_date, end_date, dated1, dated2,
                applicability1, compliance1, rem1, upload1,
                applicability2, compliance2, rem2, upload2,
                applicability3, compliance3, rem3, upload3,
                applicability4, compliance4, rem4, upload4,
                applicability5, compliance5, rem5, upload5,
                applicability6, compliance6, rem6, upload6,
                applicability7, compliance7, rem7, upload7,
                overall_status, quality_rating, recommendations,
                prepared_by, verified_by, approved_by
            ) VALUES (
                %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
                %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
                %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
                %s, %s
            ) RETURNING report_id
        """, (
            data['project_name'],
            data['report_ref_no'],
            data['memo_ref_no'],
            data['lru_name'],
            data['sru_name'],
            data['dp_name'],
            data['part_no'],
            data.get('inspection_stage'),
            data.get('test_venue'),
            data.get('quantity'),
            data.get('sl_nos'),
            data.get('serial_number'),
            data.get('start_date'),
            data.get('end_date'),
            data.get('dated1'),
            data.get('dated2'),
            # Check points 1-7
            data.get('checkPoints', [{}])[0].get('applicability', 'A'),
            data.get('checkPoints', [{}])[0].get('compliance', ''),
            data.get('checkPoints', [{}])[0].get('remarks', ''),
            data.get('checkPoints', [{}])[0].get('upload', ''),
            data.get('checkPoints', [{}])[1].get('applicability', 'A'),
            data.get('checkPoints', [{}])[1].get('compliance', ''),
            data.get('checkPoints', [{}])[1].get('remarks', ''),
            data.get('checkPoints', [{}])[1].get('upload', ''),
            data.get('checkPoints', [{}])[2].get('applicability', 'NA'),
            data.get('checkPoints', [{}])[2].get('compliance', ''),
            data.get('checkPoints', [{}])[2].get('remarks', ''),
            data.get('checkPoints', [{}])[2].get('upload', ''),
            data.get('checkPoints', [{}])[3].get('applicability', 'A'),
            data.get('checkPoints', [{}])[3].get('compliance', ''),
            data.get('checkPoints', [{}])[3].get('remarks', ''),
            data.get('checkPoints', [{}])[3].get('upload', ''),
            data.get('checkPoints', [{}])[4].get('applicability', 'NA'),
            data.get('checkPoints', [{}])[4].get('compliance', ''),
            data.get('checkPoints', [{}])[4].get('remarks', ''),
            data.get('checkPoints', [{}])[4].get('upload', ''),
            data.get('checkPoints', [{}])[5].get('applicability', 'A'),
            data.get('checkPoints', [{}])[5].get('compliance', ''),
            data.get('checkPoints', [{}])[5].get('remarks', ''),
            data.get('checkPoints', [{}])[5].get('upload', ''),
            data.get('checkPoints', [{}])[6].get('applicability', 'NIL'),
            data.get('checkPoints', [{}])[6].get('compliance', ''),
            data.get('checkPoints', [{}])[6].get('remarks', ''),
            data.get('checkPoints', [{}])[6].get('upload', ''),
            # Summary fields
            data.get('overall_status'),
            data.get('quality_rating'),
            data.get('recommendations'),
            # Signatures
            data.get('prepared_by'),
            data.get('verified_by'),
            data.get('approved_by')
        ))
        
        report_id = cur.fetchone()[0]
        
        # Log raw material report submission activity
        from utils.activity_logger import log_activity
        report_name = data.get('report_ref_no') or f"Raw Material Report {report_id}"
        log_activity(
            project_id=None,  # Report operations don't have project_id in this context
            activity_performed="Report Submitted",
            performed_by=data.get('prepared_by', 1002),  # Default to admin if not provided
            additional_info=f"ID:{report_id}|Name:{report_name}|Raw Material Report '{report_name}' (ID: {report_id}) was submitted"
        )
        
        conn.commit()
        cur.close()
        
        return jsonify({
            "success": True,
            "message": "Raw material inspection report created successfully",
            "report_id": report_id
        })
        
    except Exception as e:
        print(f"Error creating raw material inspection report: {str(e)}")
        return handle_database_error(get_db_connection(), f"Error creating raw material inspection report: {str(e)}")

@reports_bp.route('/api/reports/raw-material-inspection/<int:report_id>', methods=['GET'])
def get_raw_material_inspection_report(report_id):
    """Get raw material inspection report details"""
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        
        cur.execute("""
            SELECT * FROM raw_material_inspection_report WHERE report_id = %s
        """, (report_id,))
        
        report = cur.fetchone()
        cur.close()
        
        if not report:
            return jsonify({"success": False, "message": "Report not found"}), 404
        
        # Convert to dictionary
        columns = [desc[0] for desc in cur.description] if cur.description else []
        report_data = dict(zip(columns, report))
        
        # Convert datetime objects to strings
        for key, value in report_data.items():
            if hasattr(value, 'isoformat'):
                report_data[key] = value.isoformat()
        
        return jsonify({
            "success": True,
            "report": report_data
        })
        
    except Exception as e:
        print(f"Error fetching raw material inspection report: {str(e)}")
        return handle_database_error(get_db_connection(), f"Error fetching raw material inspection report: {str(e)}")

@reports_bp.route('/api/reports/raw-material-inspection', methods=['GET'])
def get_raw_material_inspection_reports():
    """Get all raw material inspection reports"""
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        
        cur.execute("""
            SELECT report_id, project_name, lru_name, report_ref_no, memo_ref_no, 
                   created_at, updated_at
            FROM raw_material_inspection_report 
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
                "report_ref_no": report[3],
                "memo_ref_no": report[4],
                "created_at": report[5].isoformat() if report[5] else None,
                "updated_at": report[6].isoformat() if report[6] else None
            })
        
        return jsonify({
            "success": True,
            "reports": report_list
        })
        
    except Exception as e:
        print(f"Error fetching raw material inspection reports: {str(e)}")
        return handle_database_error(get_db_connection(), f"Error fetching raw material inspection reports: {str(e)}")

@reports_bp.route('/api/reports/create-tables', methods=['POST'])
def create_inspection_tables():
    """Create inspection report tables if they don't exist"""
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        
        # Create conformal coating inspection report table
        cur.execute("""
            CREATE TABLE IF NOT EXISTS conformal_coating_inspection_report (
                report_id SERIAL PRIMARY KEY,
                project_name TEXT,
                report_ref_no VARCHAR(100),
                memo_ref_no VARCHAR(100),
                lru_name TEXT,
                sru_name TEXT,
                dp_name TEXT,
                part_no VARCHAR(100),
                inspection_stage TEXT,
                test_venue TEXT,
                quantity INT,
                sl_nos TEXT,
                serial_number VARCHAR(100),
                start_date DATE,
                end_date DATE,
                dated1 DATE,
                dated2 DATE,
                obs1 TEXT, rem1 VARCHAR(20), upload1 TEXT, expected1 TEXT DEFAULT 'Should not be there',
                obs2 TEXT, rem2 VARCHAR(20), upload2 TEXT, expected2 TEXT DEFAULT 'Should not be there',
                obs3 TEXT, rem3 VARCHAR(20), upload3 TEXT, expected3 TEXT DEFAULT 'Should not be there',
                obs4 TEXT, rem4 VARCHAR(20), upload4 TEXT, expected4 TEXT DEFAULT 'Should not be there',
                obs5 TEXT, rem5 VARCHAR(20), upload5 TEXT, expected5 TEXT DEFAULT 'Not recommended',
                obs6 TEXT, rem6 VARCHAR(20), upload6 TEXT, expected6 TEXT DEFAULT 'No Deformity',
                obs7 TEXT, rem7 VARCHAR(20), upload7 TEXT, expected7 TEXT DEFAULT 'No Damages',
                obs8 TEXT, rem8 VARCHAR(20), upload8 TEXT, expected8 TEXT DEFAULT 'Should have linear Coating',
                obs9 TEXT, rem9 VARCHAR(20), upload9 TEXT, expected9 TEXT DEFAULT '30 to 130 microns',
                overall_status TEXT,
                quality_rating INT,
                recommendations TEXT,
                prepared_by TEXT,
                verified_by TEXT,
                approved_by TEXT,
                created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
            );
        """)
        
        # Create raw material inspection report table
        cur.execute("""
            CREATE TABLE IF NOT EXISTS raw_material_inspection_report (
                report_id SERIAL PRIMARY KEY,
                project_name TEXT,
                report_ref_no VARCHAR(100),
                memo_ref_no VARCHAR(100),
                lru_name TEXT,
                sru_name TEXT,
                dp_name TEXT,
                part_no VARCHAR(100),
                inspection_stage TEXT,
                test_venue TEXT,
                quantity INT,
                sl_nos TEXT,
                serial_number VARCHAR(100),
                start_date DATE,
                end_date DATE,
                dated1 DATE,
                dated2 DATE,
                applicability1 VARCHAR(10) CHECK (applicability1 IN ('A', 'NA')) DEFAULT 'A',
                compliance1 VARCHAR(10) CHECK (compliance1 IN ('YES', 'NO', 'NA')),
                rem1 VARCHAR(20) CHECK (rem1 IN ('OK', 'NOT OK', 'NA')),
                upload1 TEXT,
                applicability2 VARCHAR(10) CHECK (applicability2 IN ('A', 'NA')) DEFAULT 'A',
                compliance2 VARCHAR(10) CHECK (compliance2 IN ('YES', 'NO', 'NA')),
                rem2 VARCHAR(20) CHECK (rem2 IN ('OK', 'NOT OK', 'NA')),
                upload2 TEXT,
                applicability3 VARCHAR(10) CHECK (applicability3 IN ('A', 'NA')) DEFAULT 'NA',
                compliance3 VARCHAR(10) CHECK (compliance3 IN ('YES', 'NO', 'NA')),
                rem3 VARCHAR(20) CHECK (rem3 IN ('OK', 'NOT OK', 'NA')),
                upload3 TEXT,
                applicability4 VARCHAR(10) CHECK (applicability4 IN ('A', 'NA')) DEFAULT 'A',
                compliance4 VARCHAR(10) CHECK (compliance4 IN ('YES', 'NO', 'NA')),
                rem4 VARCHAR(20) CHECK (rem4 IN ('OK', 'NOT OK', 'NA')),
                upload4 TEXT,
                applicability5 VARCHAR(10) CHECK (applicability5 IN ('A', 'NA')) DEFAULT 'NA',
                compliance5 VARCHAR(10) CHECK (compliance5 IN ('YES', 'NO', 'NA')),
                rem5 VARCHAR(20) CHECK (rem5 IN ('OK', 'NOT OK', 'NA')),
                upload5 TEXT,
                applicability6 VARCHAR(10) CHECK (applicability6 IN ('A', 'NA')) DEFAULT 'A',
                compliance6 VARCHAR(10) CHECK (compliance6 IN ('YES', 'NO', 'NA')),
                rem6 VARCHAR(20) CHECK (rem6 IN ('OK', 'NOT OK', 'NA')),
                upload6 TEXT,
                applicability7 VARCHAR(10) CHECK (applicability7 IN ('A', 'NA')) DEFAULT 'NA',
                compliance7 VARCHAR(10) CHECK (compliance7 IN ('YES', 'NO', 'NA')),
                rem7 VARCHAR(20) CHECK (rem7 IN ('OK', 'NOT OK', 'NA')),
                upload7 TEXT,
                overall_status TEXT,
                quality_rating INT,
                recommendations TEXT,
                prepared_by TEXT,
                verified_by TEXT,
                approved_by TEXT,
                created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
            );
        """)
        
        # Create triggers
        cur.execute("""
            CREATE OR REPLACE FUNCTION update_updated_at_column()
            RETURNS TRIGGER AS $$
            BEGIN
                NEW.updated_at = CURRENT_TIMESTAMP;
                RETURN NEW;
            END;
            $$ LANGUAGE plpgsql;
        """)
        
        cur.execute("""
            DROP TRIGGER IF EXISTS trg_update_updated_at_conformal_coating ON conformal_coating_inspection_report;
            CREATE TRIGGER trg_update_updated_at_conformal_coating
            BEFORE UPDATE ON conformal_coating_inspection_report
            FOR EACH ROW
            EXECUTE FUNCTION update_updated_at_column();
        """)
        
        cur.execute("""
            DROP TRIGGER IF EXISTS trg_update_updated_at_raw_material ON raw_material_inspection_report;
            CREATE TRIGGER trg_update_updated_at_raw_material
            BEFORE UPDATE ON raw_material_inspection_report
            FOR EACH ROW
            EXECUTE FUNCTION update_updated_at_column();
        """)
        
        conn.commit()
        cur.close()
        
        return jsonify({
            "success": True,
            "message": "Inspection report tables created successfully"
        })
        
    except Exception as e:
        print(f"Error creating tables: {str(e)}")
        return handle_database_error(get_db_connection(), f"Error creating tables: {str(e)}")