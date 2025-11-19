"""
Report management routes
"""
import os
import uuid
from functools import wraps
from flask import Blueprint, request, jsonify, send_file
from config import get_db_connection, Config
from utils.helpers import handle_database_error, allowed_file, validate_file_size
from config import get_db_connection
from utils.helpers import handle_database_error

reports_bp = Blueprint('reports', __name__)

# def require_design_head_role(f):
#     """Decorator to require design head role (role_id = 4)"""
#     @wraps(f)
#     def decorated_function(*args, **kwargs):
#         user_role = request.args.get('user_role', type=int)
#         if user_role != 4:  # Design Head role
#             return jsonify({
#                 "success": False, 
#                 "message": "Access denied. Design Head role required."
#             }), 403
#         return f(*args, **kwargs)
#     return decorated_function

@reports_bp.route('/api/reports', methods=['GET'])
def get_reports():
    """Get reports with role-based filtering"""
    try:
        # Get user context from query parameters
        user_id = request.args.get('user_id', type=int)
        user_role = request.args.get('user_role', type=int)
        print("USER ROLE from REQ ARGS", user_role)
        print("USER ID from REQ ARGS", user_id)

        # Handle case where user_id or user_role is None
        if user_id is None or user_role is None:
            # If no user context provided, return empty list or all reports based on your requirement
            user_id = user_id or 0
            user_role = user_role or 0
            print("No user context provided, defaulting to user_id=0, user_role=0")

        print(f"Fetching reports for user_id={user_id}, user_role={user_role}")
        
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
                    COALESCE(r.status, 'ASSIGNED') as status,
                    r.date_of_review as created_at,
                    p.project_name,
                    l.lru_name,
                    m.wing_proj_ref_no,
                    m.lru_sru_desc,
                    m.part_number,
                    r.memo_id,
                    r.template_id
                FROM reports r
                LEFT JOIN projects p ON r.project_id = p.project_id
                LEFT JOIN lrus l ON r.lru_id = l.lru_id
                LEFT JOIN memos m ON r.memo_id = m.memo_id
                WHERE m.submitted_by = %s
                ORDER BY r.date_of_review DESC
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
                    COALESCE(r.status, 'ASSIGNED') as status,
                    r.date_of_review as created_at,
                    p.project_name,
                    l.lru_name,
                    m.wing_proj_ref_no,
                    m.lru_sru_desc,
                    m.part_number,
                    r.memo_id,
                    r.template_id
                FROM reports r
                LEFT JOIN projects p ON r.project_id = p.project_id
                LEFT JOIN lrus l ON r.lru_id = l.lru_id
                LEFT JOIN memos m ON r.memo_id = m.memo_id
                LEFT JOIN memo_approval ma ON r.memo_id = ma.memo_id
                WHERE ma.user_id = %s AND ma.status = 'accepted'
                ORDER BY r.date_of_review DESC
            """
            query_params = (user_id,)
            
               
        else:# Admin, QA Head, Design Head - show all reports
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
                    COALESCE(r.status, 'ASSIGNED') as status,
                    r.date_of_review as created_at,
                    p.project_name,
                    l.lru_name,
                    m.wing_proj_ref_no,
                    m.lru_sru_desc,
                    m.part_number,
                    r.memo_id,
                    r.template_id
                FROM reports r
                LEFT JOIN projects p ON r.project_id = p.project_id
                LEFT JOIN lrus l ON r.lru_id = l.lru_id
                LEFT JOIN memos m ON r.memo_id = m.memo_id
                ORDER BY r.date_of_review DESC
            """
            query_params = ()
        
        
        
        cur.execute(base_query, query_params)
        
        reports = cur.fetchall()
        
        
        # Also fetch conformal coating inspection reports
        # try:
        #     cur.execute("""
        #         SELECT report_id, project_name, lru_name, report_ref_no, memo_ref_no, 
        #                created_at, updated_at
        #         FROM conformal_coating_inspection_report 
        #         ORDER BY created_at DESC
        #     """)
        #     conformal_reports = cur.fetchall()
        # except Exception as e:
        #     print(f"Warning: Could not fetch conformal coating reports: {str(e)}")
        #     conformal_reports = []
        
        cur.close()

        # print("REPORTTTTTT", reports[0])

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
                "name": report[13] or f"MEMO-{report[1]}" if report[1] else "No Memo",  # Use wing_proj_ref_no or fallback
                "memo_description": report[14],
                "part_number": report[15],
                "report_type": "memo_report",
                "template_id": report[17],
            })
        
        print("PRINTTTTTTTTTTTTTTTTTTTTTT!!!!")
        
        # Add conformal coating reports
        # for report in conformal_reports:
        #     report_list.append({
        #         "id": report[0],
        #         "memo_id": report[4],  # memo_ref_no
        #         "project_id": None,
        #         "lru_id": None,
        #         "serial_id": None,
        #         "inspection_stage": None,
        #         "date_of_review": report[5].isoformat() if report[5] else None,
        #         "review_venue": None,
        #         "reference_document": None,
        #         "status": "Active",
        #         "created_at": report[5].isoformat() if report[5] else None,
        #         "project": report[1],  # project_name
        #         "lru_name": report[2],
        #         "name": report[3] or f"Conformal Coating Report {report[0]}",  # report_ref_no
        #         "memo_description": None,
        #         "part_number": None,
        #         "report_type": "conformal_coating",
        #         "report_ref_no": report[3],
        #         "memo_ref_no": report[4]
        #     })

        conformal_reports= []

        print(f"Returning {len(report_list)} reports ({len(reports)} memo reports, {len(conformal_reports)} conformal coating reports)")
        
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
        
        # Fetch report details with template information and assigned reviewer
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
                COALESCE(r.status, 'ASSIGNED') as status,
                r.date_of_review as created_at,
                r.template_id,
                p.project_name,
                l.lru_name,
                NULL as wing_proj_ref_no,
                NULL as lru_sru_desc,
                NULL as part_number,
                NULL as from_person,
                NULL as to_person,
                NULL as thru_person,
                NULL as casdic_ref_no,
                NULL as dated,
                NULL as manufacturer,
                NULL as drawing_no_rev,
                NULL as source,
                NULL as venue,
                NULL as memo_date,
                NULL as name_designation,
                NULL as test_facility,
                NULL as test_cycle_duration,
                NULL as test_start_on,
                NULL as test_complete_on,
                NULL as calibration_status,
                NULL as func_check_initial,
                NULL as perf_check_during,
                NULL as func_check_end,
                NULL as certified,
                NULL as remarks,
                rt.template_name,
                ma.user_id as assigned_reviewer_id
            FROM reports r
            LEFT JOIN projects p ON r.project_id = p.project_id
            LEFT JOIN lrus l ON r.lru_id = l.lru_id
            LEFT JOIN report_templates rt ON r.template_id = rt.template_id
            LEFT JOIN memo_approval ma ON r.memo_id = ma.memo_id AND ma.status = 'accepted'
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
            "template_name": report[38],
            "assigned_reviewer_id": report[39]
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

@reports_bp.route('/api/report-templates', methods=['GET'])
def get_report_templates():
    """Get all available report templates"""
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        
        # Fetch all report templates
        cur.execute("""
            SELECT template_id, template_name
            FROM report_templates
            ORDER BY template_name
        """)
        
        templates = cur.fetchall()
        cur.close()
        
        # Convert to list of dictionaries
        template_list = []
        for template in templates:
            template_list.append({
                "template_id": template[0],
                "name": template[1],
                "displayName": template[1].title(),
                "description": f"Template for {template[1]}",
                "component": template[1].replace(" ", "").replace("_", "")
            })
        
        return jsonify({
            "success": True,
            "templates": template_list
        })
        
    except Exception as e:
        print(f"Error fetching report templates: {str(e)}")
        return handle_database_error(get_db_connection(), f"Error fetching report templates: {str(e)}")

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

# ------------------ Bare PCB Inspection Report Routes ------------------ #

@reports_bp.route('/api/reports/bare-pcb-inspection', methods=['POST'])
def create_bare_pcb_inspection_report():
    """Create or update a bare PCB inspection report"""
    try:
        data = request.json
        if not data:
            return jsonify({"success": False, "message": "No data provided"}), 400
        
        conn = get_db_connection()
        cur = conn.cursor()
        
        # Check if table exists first
        cur.execute("""
            SELECT EXISTS (
                SELECT FROM information_schema.tables 
                WHERE table_name = 'bare_pcb_inspection_report'
            );
        """)
        table_exists = cur.fetchone()[0]
        
        if not table_exists:
            cur.close()
            return jsonify({"success": False, "message": "Table 'bare_pcb_inspection_report' does not exist"}), 500
        
        # Check if report_card_id column exists, add if missing
        report_card_id = data.get('report_card_id')
        cur.execute("""
            SELECT column_name 
            FROM information_schema.columns 
            WHERE table_name = 'bare_pcb_inspection_report' 
            AND column_name = 'report_card_id'
        """)
        has_report_card_id = cur.fetchone() is not None
        
        if not has_report_card_id and report_card_id:
            try:
                cur.execute("ALTER TABLE bare_pcb_inspection_report ADD COLUMN report_card_id INTEGER")
                conn.commit()
                has_report_card_id = True
                print("Added report_card_id column to bare_pcb_inspection_report table")
            except Exception as e:
                print(f"Note: Could not add report_card_id column (may already exist): {str(e)}")
                conn.rollback()
        
        # Check if report already exists for this report_card_id
        existing_report_id = None
        if report_card_id and has_report_card_id:
            cur.execute("""
                SELECT report_id FROM bare_pcb_inspection_report 
                WHERE report_card_id = %s
            """, (report_card_id,))
            existing = cur.fetchone()
            if existing:
                existing_report_id = existing[0]
        
        # Get user ID from request or data
        user_id = request.args.get('user_id', type=int) or data.get('user_id') or 1002
        
        # Prepare data for visual inspection (10 items)
        visual_inspection = data.get('visual_inspection', [])
        while len(visual_inspection) < 10:
            visual_inspection.append({'observation': '', 'remarks': '', 'fileName': None})
        
        # Prepare data for continuity check (1 item)
        continuity_check = data.get('continuity_check', [])
        if len(continuity_check) == 0:
            continuity_check.append({'observation': '', 'remarks': '', 'fileName': None})
        
        # Prepare fabricator report data
        fabricator_report = data.get('fabricator_report', {})
        
        if existing_report_id:
            # Update existing report
            cur.execute("""
                UPDATE bare_pcb_inspection_report SET
                    project_name = %s, report_ref_no = %s, memo_ref_no = %s, lru_name = %s, 
                    sru_name = %s, dp_name = %s, part_no = %s, inspection_stage = %s, 
                    test_venue = %s, quantity = %s, sl_nos = %s, serial_number = %s,
                    inspection_count = %s, start_date = %s, end_date = %s, dated1 = %s, dated2 = %s,
                    obs1 = %s, rem1 = %s, upload1 = %s, obs2 = %s, rem2 = %s, upload2 = %s,
                    obs3 = %s, rem3 = %s, upload3 = %s, obs4 = %s, rem4 = %s, upload4 = %s,
                    obs5 = %s, rem5 = %s, upload5 = %s, obs6 = %s, rem6 = %s, upload6 = %s,
                    obs7 = %s, rem7 = %s, upload7 = %s, obs8 = %s, rem8 = %s, upload8 = %s,
                    obs9 = %s, rem9 = %s, upload9 = %s, obs10 = %s, rem10 = %s, upload10 = %s,
                    obs11 = %s, rem11 = %s, upload11 = %s,
                    obs12 = %s, rem12 = %s, upload12 = %s,
                    prepared_by = %s, verified_by = %s, approved_by = %s,
                    updated_at = CURRENT_TIMESTAMP
                WHERE report_id = %s
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
                data.get('inspection_count') or None,
                data.get('start_date') or None,
                data.get('end_date') or None,
                data.get('dated1') or None,
                data.get('dated2') or None,
                # Visual Inspection (10 items = obs1-obs10, rem1-rem10, upload1-upload10)
                visual_inspection[0].get('observation') or None, visual_inspection[0].get('remarks') or None, visual_inspection[0].get('fileName') or None,
                visual_inspection[1].get('observation') or None, visual_inspection[1].get('remarks') or None, visual_inspection[1].get('fileName') or None,
                visual_inspection[2].get('observation') or None, visual_inspection[2].get('remarks') or None, visual_inspection[2].get('fileName') or None,
                visual_inspection[3].get('observation') or None, visual_inspection[3].get('remarks') or None, visual_inspection[3].get('fileName') or None,
                visual_inspection[4].get('observation') or None, visual_inspection[4].get('remarks') or None, visual_inspection[4].get('fileName') or None,
                visual_inspection[5].get('observation') or None, visual_inspection[5].get('remarks') or None, visual_inspection[5].get('fileName') or None,
                visual_inspection[6].get('observation') or None, visual_inspection[6].get('remarks') or None, visual_inspection[6].get('fileName') or None,
                visual_inspection[7].get('observation') or None, visual_inspection[7].get('remarks') or None, visual_inspection[7].get('fileName') or None,
                visual_inspection[8].get('observation') or None, visual_inspection[8].get('remarks') or None, visual_inspection[8].get('fileName') or None,
                visual_inspection[9].get('observation') or None, visual_inspection[9].get('remarks') or None, visual_inspection[9].get('fileName') or None,
                # Continuity Check (1 item = obs11, rem11, upload11)
                continuity_check[0].get('observation') or None, continuity_check[0].get('remarks') or None, continuity_check[0].get('fileName') or None,
                # Fabricator Report (1 item = obs12, rem12, upload12)
                fabricator_report.get('observation') or None, fabricator_report.get('remarks') or None, fabricator_report.get('fileName') or None,
                data.get('prepared_by') or None,
                data.get('verified_by') or None,
                data.get('approved_by') or None,
                existing_report_id
            ))
            report_id = existing_report_id
        else:
            # Insert new report
            columns = [
                'project_name', 'report_ref_no', 'memo_ref_no', 'lru_name', 'sru_name', 'dp_name',
                'part_no', 'inspection_stage', 'test_venue', 'quantity', 'sl_nos', 'serial_number',
                'inspection_count', 'start_date', 'end_date', 'dated1', 'dated2',
                'obs1', 'rem1', 'upload1', 'obs2', 'rem2', 'upload2', 'obs3', 'rem3', 'upload3',
                'obs4', 'rem4', 'upload4', 'obs5', 'rem5', 'upload5', 'obs6', 'rem6', 'upload6',
                'obs7', 'rem7', 'upload7', 'obs8', 'rem8', 'upload8', 'obs9', 'rem9', 'upload9',
                'obs10', 'rem10', 'upload10', 'obs11', 'rem11', 'upload11', 'obs12', 'rem12', 'upload12',
                'prepared_by', 'verified_by', 'approved_by'
            ]
            
            values = [
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
                data.get('inspection_count') or None,
                data.get('start_date') or None,
                data.get('end_date') or None,
                data.get('dated1') or None,
                data.get('dated2') or None,
                # Visual Inspection (10 items)
                visual_inspection[0].get('observation') or None, visual_inspection[0].get('remarks') or None, visual_inspection[0].get('fileName') or None,
                visual_inspection[1].get('observation') or None, visual_inspection[1].get('remarks') or None, visual_inspection[1].get('fileName') or None,
                visual_inspection[2].get('observation') or None, visual_inspection[2].get('remarks') or None, visual_inspection[2].get('fileName') or None,
                visual_inspection[3].get('observation') or None, visual_inspection[3].get('remarks') or None, visual_inspection[3].get('fileName') or None,
                visual_inspection[4].get('observation') or None, visual_inspection[4].get('remarks') or None, visual_inspection[4].get('fileName') or None,
                visual_inspection[5].get('observation') or None, visual_inspection[5].get('remarks') or None, visual_inspection[5].get('fileName') or None,
                visual_inspection[6].get('observation') or None, visual_inspection[6].get('remarks') or None, visual_inspection[6].get('fileName') or None,
                visual_inspection[7].get('observation') or None, visual_inspection[7].get('remarks') or None, visual_inspection[7].get('fileName') or None,
                visual_inspection[8].get('observation') or None, visual_inspection[8].get('remarks') or None, visual_inspection[8].get('fileName') or None,
                visual_inspection[9].get('observation') or None, visual_inspection[9].get('remarks') or None, visual_inspection[9].get('fileName') or None,
                # Continuity Check (1 item)
                continuity_check[0].get('observation') or None, continuity_check[0].get('remarks') or None, continuity_check[0].get('fileName') or None,
                # Fabricator Report (1 item)
                fabricator_report.get('observation') or None, fabricator_report.get('remarks') or None, fabricator_report.get('fileName') or None,
                data.get('prepared_by') or None,
                data.get('verified_by') or None,
                data.get('approved_by') or None
            ]
            
            if report_card_id and has_report_card_id:
                columns.append('report_card_id')
                values.append(report_card_id)
            
            placeholders = ', '.join(['%s'] * len(values))
            column_names = ', '.join(columns)
            
            cur.execute(f"""
                INSERT INTO bare_pcb_inspection_report ({column_names})
                VALUES ({placeholders})
                RETURNING report_id
            """, values)
            
            report_id = cur.fetchone()[0]
        
        # Commit the transaction FIRST before logging activity
        conn.commit()
        cur.close()
        
        # Log bare PCB report submission activity (after commit to avoid rollback)
        try:
            from utils.activity_logger import log_activity
            report_name = data.get('report_ref_no') or f"Bare PCB Report {report_id}"
            
            # Ensure performed_by is an integer, not a signature URL
            performed_by = user_id
            if not performed_by or performed_by == '':
                performed_by = 1002  # Default to admin if not provided or empty
            elif isinstance(performed_by, str):
                try:
                    performed_by = int(performed_by)
                except (ValueError, TypeError):
                    performed_by = 1002
            
            log_activity(
                project_id=None,
                activity_performed="Report Submitted",
                performed_by=performed_by,
                additional_info=f"ID:{report_id}|Name:{report_name}|Bare PCB Report '{report_name}' (ID: {report_id}) was submitted"
            )
        except Exception as e:
            print(f"Error logging activity: {str(e)}")
            # Continue even if activity logging fails
        
        # Send notifications after successful submission (only when all signatures are present)
        if report_card_id and data.get('prepared_by') and data.get('verified_by') and data.get('approved_by'):
            try:
                from utils.activity_logger import log_notification, get_users_by_role
                
                conn = get_db_connection()
                cur = conn.cursor()
                cur.execute("""
                    SELECT r.project_id, m.submitted_by
                    FROM reports r
                    LEFT JOIN memos m ON r.memo_id = m.memo_id
                    WHERE r.report_id = %s
                """, (report_card_id,))
                report_info = cur.fetchone()
                cur.close()
                
                if report_info and len(report_info) >= 2:
                    project_id = report_info[0]
                    performed_by = report_info[1] or user_id
                    
                    for role_id in [4, 2]:  # Design Heads = 4, QA Heads = 2
                        try:
                            users = get_users_by_role(role_id)
                            for user in users:
                                user_id_notify = user.get('user_id') if isinstance(user, dict) else (user[0] if hasattr(user, '__getitem__') else None)
                                if user_id_notify:
                                    log_notification(
                                        project_id=project_id,
                                        activity_performed="Bare PCB Inspection Report Completed",
                                        performed_by=performed_by,
                                        notified_user_id=user_id_notify,
                                        notification_type="report_completed",
                                        additional_info=f"Bare PCB Inspection Report (ID: {report_id}) for Report Card {report_card_id} has been completed with all signatures."
                                    )
                        except Exception as e:
                            print(f"Error sending notification to role {role_id}: {str(e)}")
                            pass
            except Exception as e:
                print(f"Error sending notifications: {str(e)}")
                pass
        
        return jsonify({
            "success": True,
            "message": "Bare PCB inspection report created successfully",
            "report_id": report_id
        })
        
    except Exception as e:
        print(f"Error creating bare PCB inspection report: {str(e)}")
        import traceback
        traceback.print_exc()
        return handle_database_error(get_db_connection(), f"Error creating bare PCB inspection report: {str(e)}")

@reports_bp.route('/api/reports/bare-pcb-inspection/<int:report_id>', methods=['GET'])
def get_bare_pcb_inspection_report(report_id):
    """Get bare PCB inspection report details by report_id"""
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        
        cur.execute("""
            SELECT 
                report_id, project_name, report_ref_no, memo_ref_no, lru_name, sru_name, dp_name,
                part_no, inspection_stage, test_venue, quantity, sl_nos, serial_number,
                inspection_count, start_date, end_date, dated1, dated2,
                obs1, rem1, upload1, obs2, rem2, upload2, obs3, rem3, upload3,
                obs4, rem4, upload4, obs5, rem5, upload5, obs6, rem6, upload6,
                obs7, rem7, upload7, obs8, rem8, upload8, obs9, rem9, upload9,
                obs10, rem10, upload10, obs11, rem11, upload11, obs12, rem12, upload12,
                prepared_by, verified_by, approved_by, created_at, updated_at
            FROM bare_pcb_inspection_report 
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
            "inspection_count": report[13],
            "start_date": report[14].isoformat() if report[14] else None,
            "end_date": report[15].isoformat() if report[15] else None,
            "dated1": report[16].isoformat() if report[16] else None,
            "dated2": report[17].isoformat() if report[17] else None,
            # Visual Inspection (10 items = obs1-obs10, rem1-rem10, upload1-upload10)
            "obs1": report[18], "rem1": report[19], "upload1": report[20],
            "obs2": report[21], "rem2": report[22], "upload2": report[23],
            "obs3": report[24], "rem3": report[25], "upload3": report[26],
            "obs4": report[27], "rem4": report[28], "upload4": report[29],
            "obs5": report[30], "rem5": report[31], "upload5": report[32],
            "obs6": report[33], "rem6": report[34], "upload6": report[35],
            "obs7": report[36], "rem7": report[37], "upload7": report[38],
            "obs8": report[39], "rem8": report[40], "upload8": report[41],
            "obs9": report[42], "rem9": report[43], "upload9": report[44],
            "obs10": report[45], "rem10": report[46], "upload10": report[47],
            # Continuity Check (1 item = obs11, rem11, upload11)
            "obs11": report[48], "rem11": report[49], "upload11": report[50],
            # Fabricator Report (1 item = obs12, rem12, upload12)
            "obs12": report[51], "rem12": report[52], "upload12": report[53],
            # Signatories
            "prepared_by": report[54],
            "verified_by": report[55],
            "approved_by": report[56],
            "created_at": report[57].isoformat() if report[57] else None,
            "updated_at": report[58].isoformat() if report[58] else None
        }
        
        return jsonify({
            "success": True,
            "report": report_data
        })
        
    except Exception as e:
        print(f"Error fetching bare PCB inspection report: {str(e)}")
        return handle_database_error(get_db_connection(), f"Error fetching bare PCB inspection report: {str(e)}")

@reports_bp.route('/api/reports/bare-pcb-inspection/by-report-card/<int:report_card_id>', methods=['GET'])
def get_bare_pcb_inspection_report_by_report_card(report_card_id):
    """Get bare PCB inspection report by report card ID"""
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        
        # Check if report_card_id column exists
        cur.execute("""
            SELECT column_name 
            FROM information_schema.columns 
            WHERE table_name = 'bare_pcb_inspection_report' 
            AND column_name = 'report_card_id'
        """)
        has_report_card_id = cur.fetchone() is not None
        
        if not has_report_card_id:
            cur.close()
            return jsonify({"success": False, "message": "Report not found"}), 404
        
        cur.execute("""
            SELECT 
                report_id, project_name, report_ref_no, memo_ref_no, lru_name, sru_name, dp_name,
                part_no, inspection_stage, test_venue, quantity, sl_nos, serial_number,
                inspection_count, start_date, end_date, dated1, dated2,
                obs1, rem1, upload1, obs2, rem2, upload2, obs3, rem3, upload3,
                obs4, rem4, upload4, obs5, rem5, upload5, obs6, rem6, upload6,
                obs7, rem7, upload7, obs8, rem8, upload8, obs9, rem9, upload9,
                obs10, rem10, upload10, obs11, rem11, upload11, obs12, rem12, upload12,
                prepared_by, verified_by, approved_by, created_at, updated_at
            FROM bare_pcb_inspection_report 
            WHERE report_card_id = %s
        """, (report_card_id,))
        
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
            "inspection_count": report[13],
            "start_date": report[14].isoformat() if report[14] else None,
            "end_date": report[15].isoformat() if report[15] else None,
            "dated1": report[16].isoformat() if report[16] else None,
            "dated2": report[17].isoformat() if report[17] else None,
            # Visual Inspection (10 items = obs1-obs10, rem1-rem10, upload1-upload10)
            "obs1": report[18], "rem1": report[19], "upload1": report[20],
            "obs2": report[21], "rem2": report[22], "upload2": report[23],
            "obs3": report[24], "rem3": report[25], "upload3": report[26],
            "obs4": report[27], "rem4": report[28], "upload4": report[29],
            "obs5": report[30], "rem5": report[31], "upload5": report[32],
            "obs6": report[33], "rem6": report[34], "upload6": report[35],
            "obs7": report[36], "rem7": report[37], "upload7": report[38],
            "obs8": report[39], "rem8": report[40], "upload8": report[41],
            "obs9": report[42], "rem9": report[43], "upload9": report[44],
            "obs10": report[45], "rem10": report[46], "upload10": report[47],
            # Continuity Check (1 item = obs11, rem11, upload11)
            "obs11": report[48], "rem11": report[49], "upload11": report[50],
            # Fabricator Report (1 item = obs12, rem12, upload12)
            "obs12": report[51], "rem12": report[52], "upload12": report[53],
            # Signatories
            "prepared_by": report[54],
            "verified_by": report[55],
            "approved_by": report[56],
            "created_at": report[57].isoformat() if report[57] else None,
            "updated_at": report[58].isoformat() if report[58] else None
        }
        
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


# Raw Material Inspection Report API Endpoints

@reports_bp.route('/api/reports/raw-material-inspection', methods=['POST'])
def create_raw_material_inspection_report():
    """Create a new raw material inspection report"""
    conn = None
    try:
        data = request.json
        if not data:
            return jsonify({"success": False, "message": "No data provided"}), 400
        
        print(f"Received raw material inspection report data: {data}")
        
        # Validate required fields
        required_fields = ['project_name', 'report_ref_no', 'memo_ref_no', 'lru_name', 'dp_name', 'sru_name', 'part_no']
        missing_fields = []
        for field in required_fields:
            if field not in data or not data[field]:
                missing_fields.append(field)
        
        if missing_fields:
            return jsonify({
                "success": False, 
                "message": f"Missing required fields: {', '.join(missing_fields)}"
            }), 400
        
        conn = get_db_connection()
        cur = conn.cursor()
        
        # Helper function to convert empty strings to None for constraint compliance
        def safe_get_checkpoint(index, key, default=None):
            """Safely get checkpoint value, converting empty strings to None"""
            checkpoint = data.get('checkPoints', [{}])
            if index < len(checkpoint):
                value = checkpoint[index].get(key, default)
                # Convert empty strings to None for database constraints
                if value == '' or value is None:
                    return None
                return value
            return None
        
        # Convert quantity to int or None
        quantity = data.get('quantity')
        if quantity:
            try:
                quantity = int(quantity)
            except (ValueError, TypeError):
                quantity = None
        
        # Prepare checkpoints data with proper null handling
        checkpoints_data = []
        # Default applicability based on checkpoint index
        default_applicability = ['A', 'A', 'NA', 'A', 'NA', 'A', 'NA']
        for i in range(7):
            # Ensure applicability is always 'A' or 'NA', never None or empty
            applicability = safe_get_checkpoint(i, 'applicability')
            if not applicability or applicability not in ['A', 'NA']:
                applicability = default_applicability[i]
            compliance = safe_get_checkpoint(i, 'compliance')  # None if empty - allowed by constraint
            remarks = safe_get_checkpoint(i, 'remarks')  # None if empty - allowed by constraint
            upload = safe_get_checkpoint(i, 'upload')  # None if empty
            checkpoints_data.extend([applicability, compliance, remarks, upload])
        
        # Insert raw material inspection report
        insert_query = """
            INSERT INTO raw_material_inspection_report (
                report_card_id, project_name, report_ref_no, memo_ref_no, lru_name, sru_name, dp_name, 
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
                %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
                %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
                %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
                %s, %s
            ) RETURNING report_id
        """
        
        insert_values = (
            data.get('report_card_id'),  # Foreign key to reports table
            data['project_name'],
            data['report_ref_no'],
            data['memo_ref_no'],
            data['lru_name'],
            data['sru_name'],
            data['dp_name'],
            data['part_no'],
            data.get('inspection_stage') or None,
            data.get('test_venue') or None,
            quantity,
            data.get('sl_nos') or None,
            data.get('serial_number') or None,
            data.get('start_date') or None,
            data.get('end_date') or None,
            data.get('dated1') or None,
            data.get('dated2') or None,
            *checkpoints_data,  # Unpack all 28 checkpoint values (7 * 4 fields)
            data.get('overall_status') or None,
            data.get('quality_rating') or None,
            data.get('recommendations') or None,
            data.get('prepared_by') or None,
            data.get('verified_by') or None,
            data.get('approved_by') or None
        )
        
        print(f"Executing INSERT query with {len(insert_values)} values")
        cur.execute(insert_query, insert_values)
        
        report_id = cur.fetchone()[0]
        print(f"Successfully inserted raw material inspection report with ID: {report_id}")
        
        # Commit the transaction FIRST before logging activity
        conn.commit()
        print(f"Transaction committed successfully for report ID: {report_id}")
        
        # Log raw material report submission activity (separate transaction)
        from utils.activity_logger import log_activity
        report_name = data.get('report_ref_no') or f"Raw Material Report {report_id}"
        
        # Extract user_id from prepared_by_user_id if provided, otherwise try to parse from prepared_by string
        user_id_for_logging = data.get('prepared_by_user_id')
        if not user_id_for_logging:
            # Try to extract user_id from session if available
            # For now, default to a system user ID
            user_id_for_logging = 1002  # Default to admin/system user
        
        try:
            log_activity(
                project_id=None,  # Report operations don't have project_id in this context
                activity_performed="Report Submitted",
                performed_by=user_id_for_logging,  # Use user_id instead of prepared_by string
                additional_info=f"ID:{report_id}|Name:{report_name}|Raw Material Report '{report_name}' (ID: {report_id}) was submitted"
            )
        except Exception as log_error:
            print(f"Warning: Failed to log activity: {str(log_error)}")
            # Don't fail the main operation if logging fails
        cur.close()
        conn.close()
        
        return jsonify({
            "success": True,
            "message": "Raw material inspection report created successfully",
            "report_id": report_id
        })
        
    except Exception as e:
        import traceback
        error_trace = traceback.format_exc()
        print(f"Error creating raw material inspection report: {str(e)}")
        print(f"Traceback: {error_trace}")
        
        if conn:
            try:
                conn.rollback()
                conn.close()
            except:
                pass
        
        return jsonify({
            "success": False,
            "message": f"Error creating raw material inspection report: {str(e)}",
            "error": str(e)
        }), 500

@reports_bp.route('/api/reports/raw-material-inspection/<int:report_id>', methods=['GET'])
def get_raw_material_inspection_report(report_id):
    """Get raw material inspection report details
    report_id can be either the report_card_id (from reports table) or the inspection report's own report_id
    """
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        
        # First try to find by report_card_id (from reports table) - preferred method
        cur.execute("""
            SELECT * FROM raw_material_inspection_report 
            WHERE report_card_id = %s
        """, (report_id,))
        
        report = cur.fetchone()
        
        # If not found, try by the inspection report's own report_id
        if not report:
            cur.execute("""
                SELECT * FROM raw_material_inspection_report 
                WHERE report_id = %s
            """, (report_id,))
            report = cur.fetchone()
        
        columns = [desc[0] for desc in cur.description] if cur.description else []
        
        cur.close()
        
        if not report:
            return jsonify({"success": False, "message": "Report not found"}), 404
        
        # Convert to dictionary
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

@reports_bp.route('/api/reports/raw-material-inspection/<int:report_id>', methods=['PUT'])
def update_raw_material_inspection_report(report_id):
    """Update raw material inspection report (typically for updating signatures)"""
    conn = None
    try:
        data = request.json
        if not data:
            return jsonify({"success": False, "message": "No data provided"}), 400
        
        print(f"UPDATE request received for raw material inspection report ID: {report_id}")
        print(f"Update data: {data}")
        
        conn = get_db_connection()
        cur = conn.cursor()
        
        # First, check if the report exists
        cur.execute("""
            SELECT report_id FROM raw_material_inspection_report WHERE report_id = %s
        """, (report_id,))
        
        existing_report = cur.fetchone()
        if not existing_report:
            print(f"Report ID {report_id} not found in raw_material_inspection_report table")
            return jsonify({
                "success": False, 
                "message": f"Report not found with ID: {report_id}"
            }), 404
        
        # Build dynamic update query based on provided fields
        update_fields = []
        update_values = []
        
        # Header fields
        header_fields = [
            'project_name', 'report_ref_no', 'memo_ref_no', 'lru_name', 'sru_name', 'dp_name',
            'part_no', 'inspection_stage', 'test_venue', 'quantity', 'sl_nos', 'serial_number',
            'start_date', 'end_date', 'dated1', 'dated2', 'report_card_id'
        ]
        
        for field in header_fields:
            if field in data:
                update_fields.append(f"{field} = %s")
                # Handle quantity as integer
                if field == 'quantity' and data[field] is not None:
                    try:
                        update_values.append(int(data[field]))
                    except (ValueError, TypeError):
                        update_values.append(None)
                else:
                    update_values.append(data[field] or None)
        
        # Check points (applicability1-7, compliance1-7, rem1-7, upload1-7)
        for i in range(1, 8):
            for prefix in ['applicability', 'compliance', 'rem', 'upload']:
                field = f"{prefix}{i}"
                if field in data:
                    update_fields.append(f"{field} = %s")
                    # Validate applicability for CHECK constraint
                    if prefix == 'applicability' and data[field]:
                        applicability_value = data[field].strip().upper()
                        if applicability_value not in ['A', 'NA']:
                            print(f"Warning: Invalid applicability value '{applicability_value}' for {field}, setting to None")
                            update_values.append(None)
                        else:
                            update_values.append(applicability_value)
                    # Validate compliance for CHECK constraint
                    elif prefix == 'compliance' and data[field]:
                        compliance_value = data[field].strip().upper()
                        if compliance_value not in ['YES', 'NO', 'NA']:
                            print(f"Warning: Invalid compliance value '{compliance_value}' for {field}, setting to None")
                            update_values.append(None)
                        else:
                            update_values.append(compliance_value)
                    # Validate remarks for CHECK constraint
                    elif prefix == 'rem' and data[field]:
                        remark_value = data[field].strip().upper()
                        # Handle 'NOT OK' case properly
                        if remark_value == 'NOT OK' or remark_value == 'NOTOK':
                            update_values.append('NOT OK')
                        elif remark_value in ['OK', 'NA']:
                            update_values.append(remark_value)
                        else:
                            print(f"Warning: Invalid remark value '{remark_value}' for {field}, setting to None")
                            update_values.append(None)
                    else:
                        update_values.append(data[field] or None)
        
        # Summary fields
        summary_fields = ['overall_status', 'quality_rating', 'recommendations']
        for field in summary_fields:
            if field in data:
                update_fields.append(f"{field} = %s")
                # Handle quality_rating as integer
                if field == 'quality_rating' and data[field] is not None:
                    try:
                        update_values.append(int(data[field]))
                    except (ValueError, TypeError):
                        update_values.append(None)
                else:
                    update_values.append(data[field] or None)
        
        # Signatory fields (most common updates)
        signatory_fields = ['prepared_by', 'verified_by', 'approved_by']
        for field in signatory_fields:
            if field in data:
                update_fields.append(f"{field} = %s")
                update_values.append(data[field] or None)
        
        if not update_fields:
            cur.close()
            conn.close()
            return jsonify({"success": False, "message": "No fields to update"}), 400
        
        # Add updated_at timestamp
        update_fields.append("updated_at = CURRENT_TIMESTAMP")
        
        # Add report_id to the values for WHERE clause
        update_values.append(report_id)
        
        # Execute update
        update_query = f"""
            UPDATE raw_material_inspection_report 
            SET {', '.join(update_fields)}
            WHERE report_id = %s
        """
        
        print(f"Executing UPDATE query: {update_query}")
        print(f"With values: {update_values}")
        
        cur.execute(update_query, update_values)
        
        if cur.rowcount == 0:
            cur.close()
            conn.close()
            return jsonify({"success": False, "message": "Report not found or no changes made"}), 404
        
        conn.commit()
        cur.close()
        conn.close()
        
        print(f"Successfully updated raw material inspection report with ID: {report_id}")
        
        return jsonify({
            "success": True,
            "message": "Raw material inspection report updated successfully",
            "report_id": report_id
        })
        
    except Exception as e:
        import traceback
        error_trace = traceback.format_exc()
        print(f"Error updating raw material inspection report: {str(e)}")
        print(f"Traceback: {error_trace}")
        
        if conn:
            try:
                conn.rollback()
                conn.close()
            except:
                pass
        
        return jsonify({
            "success": False,
            "message": f"Error updating raw material inspection report: {str(e)}",
            "error": str(e)
        }), 500

@reports_bp.route('/api/reports/raw-material-inspection', methods=['GET'])
def get_raw_material_inspection_reports():
    """Get all raw material inspection reports"""
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        
        cur.execute("""
            SELECT report_id, project_name, lru_name, report_ref_no, memo_ref_no, 
                   created_at, updated_at, report_card_id
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
                "updated_at": report[6].isoformat() if report[6] else None,
                "report_card_id": report[7] if report[7] else None
            })
        
        return jsonify({
            "success": True,
            "reports": report_list
        })
        
    except Exception as e:
        print(f"Error fetching raw material inspection reports: {str(e)}")
        return handle_database_error(get_db_connection(), f"Error fetching raw material inspection reports: {str(e)}")

@reports_bp.route('/api/iqa-observation-reports', methods=['POST'])
def create_iqa_observation_report():
    """Create a new IQA observation report"""
    try:
        data = request.json
        if not data:
            return jsonify({"success": False, "message": "No data provided"}), 400
        
        # Validate required fields
        required_fields = ['project_id', 'lru_id', 'document_id', 'created_by']
        missing_fields = [field for field in required_fields if field not in data]
        if missing_fields:
            return jsonify({
                "success": False,
                "message": f"Missing required fields: {', '.join(missing_fields)}"
            }), 400
        
        conn = get_db_connection()
        cur = conn.cursor()
        
        # Verify document exists and get its info
        cur.execute("""
            SELECT pd.document_number, pd.version, pd.revision, pd.doc_ver,
                   l.lru_name, p.project_name, p.project_id
            FROM plan_documents pd
            JOIN lrus l ON pd.lru_id = l.lru_id
            JOIN projects p ON l.project_id = p.project_id
            WHERE pd.document_id = %s
        """, (data['document_id'],))
        
        doc_info = cur.fetchone()
        if not doc_info:
            cur.close()
            return jsonify({"success": False, "message": "Document not found"}), 404
        
        # Get observation count from document_comments (auto-fetched)
        cur.execute("""
            SELECT COUNT(*) FROM document_comments
            WHERE document_id = %s
        """, (data['document_id'],))
        
        observation_count = cur.fetchone()[0]
        
        # Insert IQA observation report
        cur.execute("""
            INSERT INTO iqa_observation_reports (
                project_id, lru_id, document_id,
                observation_count, report_date, current_year,
                lru_part_number, serial_number, inspection_stage,
                doc_review_date, review_venue, reference_document,
                reviewed_by_user_id, reviewed_by_signature_path, reviewed_by_verified_name,
                approved_by_user_id, approved_by_signature_path, approved_by_verified_name,
                created_by
            ) VALUES (
                %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
                %s, %s, %s, %s, %s, %s, %s
            ) RETURNING report_id
        """, (
            data['project_id'],
            data['lru_id'],
            data['document_id'],
            data.get('observation_count'),
            data.get('report_date'),
            data.get('current_year'),
            data.get('lru_part_number'),
            data.get('serial_number'),
            data.get('inspection_stage'),
            data.get('doc_review_date'),
            data.get('review_venue'),
            data.get('reference_document'),
            data.get('reviewed_by_user_id'),
            data.get('reviewed_by_signature_path'),
            data.get('reviewed_by_verified_name'),
            data.get('approved_by_user_id'),
            data.get('approved_by_signature_path'),
            data.get('approved_by_verified_name'),
            data['created_by']
        ))
        
        report_id = cur.fetchone()[0]
        
        document_info = f"{doc_info[0]} v{doc_info[1]}" if doc_info else "Unknown"
        
        # Log activity
        from utils.activity_logger import log_activity
        log_activity(
            project_id=data['project_id'],
            activity_performed="IQA Observation Report Submitted",
            performed_by=data['created_by'],
            additional_info=f"ID:{report_id}|LRU:{doc_info[4] if doc_info else 'Unknown'}|Document:{document_info}|Observations:{observation_count}"
        )
        
        conn.commit()
        cur.close()
        
        return jsonify({
            "success": True,
            "message": "IQA observation report created successfully",
            "report_id": report_id,
            "observation_count": observation_count,
            "document_version": {
                "document_number": doc_info[0] if doc_info else None,
                "version": doc_info[1] if doc_info else None,
                "revision": doc_info[2] if doc_info else None,
                "doc_ver": doc_info[3] if doc_info else None
            }
        })
        
    except Exception as e:
        print(f"Error creating IQA observation report: {str(e)}")
        return handle_database_error(get_db_connection(), f"Error creating IQA observation report: {str(e)}")

@reports_bp.route('/api/iqa-observation-reports', methods=['GET'])
def get_iqa_observation_reports():
    """Get IQA observation reports with optional filtering"""
    try:
        # Get filter parameters from query string
        project_name = request.args.get('project_name')
        lru_name = request.args.get('lru_name')
        document_id = request.args.get('document_id', type=int)
        lru_id = request.args.get('lru_id', type=int)
        project_id = request.args.get('project_id', type=int)
        
        conn = get_db_connection()
        cur = conn.cursor()
        
        # Build query with optional filters
        query = """
            SELECT 
                ior.report_id,
                ior.project_id,
                ior.lru_id,
                ior.document_id,
                ior.observation_count,
                ior.report_date,
                ior.current_year,
                ior.lru_part_number,
                ior.serial_number,
                ior.inspection_stage,
                ior.doc_review_date,
                ior.review_venue,
                ior.reference_document,
                ior.reviewed_by_user_id,
                ior.reviewed_by_signature_path,
                ior.reviewed_by_verified_name,
                ior.approved_by_user_id,
                ior.approved_by_signature_path,
                ior.approved_by_verified_name,
                ior.created_by,
                ior.created_at,
                ior.updated_at,
                p.project_name,
                l.lru_name,
                pd.document_number,
                pd.version,
                pd.revision,
                pd.doc_ver,
                u_creator.name as created_by_name,
                u_reviewer.name as reviewed_by_name,
                u_approver.name as approved_by_name
            FROM iqa_observation_reports ior
            JOIN projects p ON ior.project_id = p.project_id
            JOIN lrus l ON ior.lru_id = l.lru_id
            LEFT JOIN plan_documents pd ON ior.document_id = pd.document_id
            LEFT JOIN users u_creator ON ior.created_by = u_creator.user_id
            LEFT JOIN users u_reviewer ON ior.reviewed_by_user_id = u_reviewer.user_id
            LEFT JOIN users u_approver ON ior.approved_by_user_id = u_approver.user_id
            WHERE 1=1
        """
        
        params = []
        
        # Add filters
        if project_name:
            query += " AND p.project_name = %s"
            params.append(project_name)
        
        if lru_name:
            query += " AND l.lru_name = %s"
            params.append(lru_name)
        
        if document_id:
            query += " AND ior.document_id = %s"
            params.append(document_id)
        
        if lru_id:
            query += " AND ior.lru_id = %s"
            params.append(lru_id)
        
        if project_id:
            query += " AND ior.project_id = %s"
            params.append(project_id)
        
        query += " ORDER BY ior.created_at DESC"
        
        cur.execute(query, params)
        reports = cur.fetchall()
        
        # Get observation count for each report
        report_list = []
        for report in reports:
            # Get observation count from document_comments
            if report[3]:  # document_id
                cur.execute("""
                    SELECT COUNT(*) FROM document_comments
                    WHERE document_id = %s
                """, (report[3],))
                obs_count = cur.fetchone()[0]
            else:
                obs_count = 0
            
            report_list.append({
                "report_id": report[0],
                "project_id": report[1],
                "lru_id": report[2],
                "document_id": report[3],
                "observation_count": report[4],
                "report_date": report[5].isoformat() if report[5] else None,
                "current_year": report[6],
                "lru_part_number": report[7],
                "serial_number": report[8],
                "inspection_stage": report[9],
                "doc_review_date": report[10].isoformat() if report[10] else None,
                "review_venue": report[11],
                "reference_document": report[12],
                "reviewed_by_user_id": report[13],
                "reviewed_by_signature_path": report[14],
                "reviewed_by_verified_name": report[15],
                "approved_by_user_id": report[16],
                "approved_by_signature_path": report[17],
                "approved_by_verified_name": report[18],
                "created_by": report[19],
                "created_at": report[20].isoformat() if report[20] else None,
                "updated_at": report[21].isoformat() if report[21] else None,
                "project_name": report[22],
                "lru_name": report[23],
                "document_number": report[24],
                "document_version": report[25],
                "document_revision": report[26],
                "document_doc_ver": report[27],
                "created_by_name": report[28],
                "reviewed_by_name": report[29],
                "approved_by_name": report[30],
                "actual_observation_count": obs_count
            })
        
        cur.close()
        
        return jsonify({
            "success": True,
            "reports": report_list,
            "count": len(report_list)
        })
        
    except Exception as e:
        print(f"Error fetching IQA observation reports: {str(e)}")
        return handle_database_error(get_db_connection(), f"Error fetching IQA observation reports: {str(e)}")

