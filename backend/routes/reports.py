"""
Report management routes
"""
from flask import Blueprint, request, jsonify
import json
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
            )
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
        
        conn.commit()
        report_id = cur.lastrowid
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
            )
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
        
        conn.commit()
        report_id = cur.lastrowid
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
            )
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
        
        conn.commit()
        report_id = cur.lastrowid
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