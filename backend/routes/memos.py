"""
Memo management routes
"""
from datetime import datetime
from flask import Blueprint, request, jsonify, send_file
from config import get_db_connection
from utils.helpers import handle_database_error
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.units import inch
import io

memos_bp = Blueprint('memos', __name__)

@memos_bp.route('/api/memos', methods=['POST'])
def submit_memo():
    """Submit a new memo and store in memos and memo_references tables"""
    try:
        data = request.json
        if not data:
            return jsonify({"success": False, "message": "No data provided"}), 400

        # Validate required fields
        required_fields = ['from_person', 'to_person', 'submitted_by']
        for field in required_fields:
            if field not in data or not data[field]:
                return jsonify({"success": False, "message": f"Missing required field: {field}"}), 400

        conn = get_db_connection()
        cur = conn.cursor()

        # Extract form data
        form_data = data.get('formData', {})
        
        # Debug: Print form data to see what's being received
        print("=== DEBUG: Form data received ===")
        print(f"slNo array: {form_data.get('slNo')}")
        print(f"slNo type: {type(form_data.get('slNo'))}")
        print(f"unitIdentification: {form_data.get('unitIdentification')}")
        print(f"unitIdentification type: {type(form_data.get('unitIdentification'))}")
        print("=== END DEBUG ===")
        
        # Get serial numbers array directly from frontend
        slno_units = form_data.get('slNo', [])
        
        # Ensure we have a proper list for PostgreSQL
        if not isinstance(slno_units, list):
            slno_units = []
        
        print(f"=== DEBUG: Processed slno_units: {slno_units} ===")
        print(f"=== DEBUG: qty_offered will be: {len(slno_units)} ===")
        print(f"=== DEBUG: slno_units type: {type(slno_units)} ===")
        print(f"=== DEBUG: slno_units length: {len(slno_units) if slno_units else 0} ===")

        # Prepare unit identification array
        unit_identification = form_data.get('unitIdentification', [])
        
        # Ensure it's a list and all elements are strings
        if not isinstance(unit_identification, list):
            unit_identification = []
        else:
            # Convert all elements to strings to ensure consistent formatting
            unit_identification = [str(item) if item is not None else "" for item in unit_identification]
        
        print(f"=== DEBUG: Processed unit_identification: {unit_identification} ===")
        print(f"=== DEBUG: unit_identification type: {type(unit_identification)} ===")

        # Prepare certified array from checkboxes
        certified = []
        if form_data.get('certifiedA'): certified.append('a')
        if form_data.get('certifiedB'): certified.append('b')
        if form_data.get('certifiedC'): certified.append('c')
        if form_data.get('certifiedD'): certified.append('d')
        if form_data.get('certifiedE'): certified.append('e')
        if form_data.get('certifiedF'): certified.append('f')
        
        # Convert to empty array if empty for PostgreSQL
        certified = certified if certified else []

        # Convert date strings to proper date format
        def parse_date(date_str):
            if not date_str:
                return None
            try:
                return datetime.strptime(date_str, '%Y-%m-%d').date()
            except:
                return None

        def parse_timestamp(timestamp_str):
            if not timestamp_str:
                return None
            try:
                return datetime.strptime(timestamp_str, '%Y-%m-%dT%H:%M')
            except:
                return None

        # Insert memo into memos table
        try:
            print("Attempting to insert memo with data:")
            print(f"from_person: {data.get('from_person')}")
            print(f"to_person: {data.get('to_person')}")
            print(f"submitted_by: {data.get('submitted_by')}")
            print(f"slno_units: {slno_units}")
            print(f"slno_units type: {type(slno_units)}")
            print(f"qty_offered: {len(slno_units) if slno_units else 0}")
            print(f"unit_identification: {unit_identification}")
            print(f"certified: {certified}")
            
            cur.execute("""
                INSERT INTO memos (
                    from_person, to_person, thru_person, casdic_ref_no, dated,
                    wing_proj_ref_no, lru_sru_desc, part_number, slno_units, qty_offered,
                    manufacturer, drawing_no_rev, source, unit_identification, mechanical_inspn,
                    inspn_test_stage_offered, stte_status, test_stage_cleared, venue,
                    memo_date, name_designation, coordinator, test_facility, test_cycle_duration,
                    test_start_on, test_complete_on, calibration_status, func_check_initial,
                    perf_check_during, func_check_end, certified, remarks,
                    submitted_at, submitted_by, memo_status
                ) VALUES (
                    %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
                    %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
                    %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
                    %s, %s, %s, %s, %s
                ) RETURNING memo_id
            """, (
                data.get('from_person'),
                data.get('to_person'),
                data.get('thru_person'),
                form_data.get('casdicRef'),
                parse_date(form_data.get('dated')),
                form_data.get('wingProjRef'),
                form_data.get('lruSruDesc'),
                form_data.get('partNo'),
                slno_units,
                len(slno_units) if slno_units else 0,  # qty_offered is count of selected serial numbers
                form_data.get('manufacturer'),
                form_data.get('drawingNoRev'),
                form_data.get('source'),
                unit_identification,
                form_data.get('mechanicalInsp'),
                form_data.get('inspnTestStageOffered'),
                form_data.get('stteStatus'),
                form_data.get('testStageCleared'),
                form_data.get('venue'),
                parse_date(form_data.get('memoDate')),
                form_data.get('nameDesignation'),
                form_data.get('coordinator'),
                form_data.get('testFacility'),
                form_data.get('testCycleDuration'),
                parse_timestamp(form_data.get('testStartOn')),
                parse_timestamp(form_data.get('testCompleteOn')),
                form_data.get('calibrationStatus'),
                parse_timestamp(form_data.get('funcCheckInitial')),
                parse_timestamp(form_data.get('perfCheckDuring')),
                parse_timestamp(form_data.get('funcCheckEnd')),
                certified,
                form_data.get('remarks'),
                datetime.now(),
                data.get('submitted_by'),
                'not_assigned'  # Initial memo_status
            ))
        except Exception as e:
            print(f"Database insertion error: {str(e)}")
            print(f"Error type: {type(e).__name__}")
            print(f"Error details: {repr(e)}")
            # Log the SQL query parameters for debugging
            print("SQL Parameters being used:")
            print(f"from_person: {data.get('from_person')}")
            print(f"to_person: {data.get('to_person')}")
            print(f"submitted_by: {data.get('submitted_by')}")
            print(f"slno_units: {slno_units}")
            print(f"unit_identification: {unit_identification}")
            print(f"certified: {certified}")
            raise e

        memo_id = cur.fetchone()[0]

        # Insert reference documents into memo_references table
        references = []
        
        # Reference 1
        if form_data.get('refDoc') or form_data.get('refNo'):
            references.append({
                'ref_doc': form_data.get('refDoc'),
                'ref_no': form_data.get('refNo'),
                'ver': float(form_data.get('version', 0)) if form_data.get('version') and form_data.get('version').strip() else None,
                'rev': float(form_data.get('revision', 0)) if form_data.get('revision') and form_data.get('revision').strip() else None
            })

        # Reference 2
        if form_data.get('refDoc2') or form_data.get('refNo2'):
            references.append({
                'ref_doc': form_data.get('refDoc2'),
                'ref_no': form_data.get('refNo2'),
                'ver': float(form_data.get('version2', 0)) if form_data.get('version2') and form_data.get('version2').strip() else None,
                'rev': float(form_data.get('revision2', 0)) if form_data.get('revision2') and form_data.get('revision2').strip() else None
            })

        # Reference 3
        if form_data.get('refDoc3') or form_data.get('refNo3'):
            references.append({
                'ref_doc': form_data.get('refDoc3'),
                'ref_no': form_data.get('refNo3'),
                'ver': float(form_data.get('version3', 0)) if form_data.get('version3') and form_data.get('version3').strip() else None,
                'rev': float(form_data.get('revision3', 0)) if form_data.get('revision3') and form_data.get('revision3').strip() else None
            })

        # Reference 4
        if form_data.get('refDoc4') or form_data.get('refNo4'):
            references.append({
                'ref_doc': form_data.get('refDoc4'),
                'ref_no': form_data.get('refNo4'),
                'ver': float(form_data.get('version4', 0)) if form_data.get('version4') and form_data.get('version4').strip() else None,
                'rev': float(form_data.get('revision4', 0)) if form_data.get('revision4') and form_data.get('revision4').strip() else None
            })

        # Reference 5
        if form_data.get('refDoc5') or form_data.get('refNo5'):
            references.append({
                'ref_doc': form_data.get('refDoc5'),
                'ref_no': form_data.get('refNo5'),
                'ver': float(form_data.get('version5', 0)) if form_data.get('version5') and form_data.get('version5').strip() else None,
                'rev': float(form_data.get('revision5', 0)) if form_data.get('revision5') and form_data.get('revision5').strip() else None
            })

        # Reference 6
        if form_data.get('refDoc6') or form_data.get('refNo6'):
            references.append({
                'ref_doc': form_data.get('refDoc6'),
                'ref_no': form_data.get('refNo6'),
                'ver': float(form_data.get('version6', 0)) if form_data.get('version6') and form_data.get('version6').strip() else None,
                'rev': float(form_data.get('revision6', 0)) if form_data.get('revision6') and form_data.get('revision6').strip() else None
            })

        # Insert references
        for ref in references:
            cur.execute("""
                INSERT INTO memo_references (memo_id, ref_doc, ref_no, ver, rev)
                VALUES (%s, %s, %s, %s, %s)
            """, (memo_id, ref['ref_doc'], ref['ref_no'], ref['ver'], ref['rev']))

        # Commit the transaction BEFORE calling utility functions that create their own connections
        conn.commit()
        cur.close()
        conn.close()

        # Log memo submission activity and notify QA Head(s) when submitted by Designer or Design Head
        # These functions will create their own connections, so call them AFTER committing the main transaction
        from utils.activity_logger import log_activity, log_notification, get_users_by_role
        log_activity(
            project_id=None,  # Memo operations don't have project_id
            activity_performed="Memo Submitted",
            performed_by=data.get('submitted_by'),
            additional_info=f"ID:{memo_id}|Name:{form_data.get('lruSruDesc', 'Memo')}|Memo '{form_data.get('lruSruDesc', 'Memo')}' (ID: {memo_id}) was submitted"
        )

        # Notify QA Heads (role_id = 2) when a Designer (role_id = 5) or Design Head (role_id = 4) submits a memo
        try:
            submitted_by_id = data.get('submitted_by')
            if submitted_by_id:
                # Get a new connection to check user roles
                conn2 = get_db_connection()
                cur2 = conn2.cursor()
                cur2.execute("SELECT role_id FROM user_roles WHERE user_id = %s", (submitted_by_id,))
                user_roles = [r[0] for r in cur2.fetchall()]
                cur2.close()
                conn2.close()

                if any(role in (4, 5) for role in user_roles):
                    qa_heads = get_users_by_role(2)
                    for qa_head in qa_heads:
                        log_notification(
                            project_id=None,
                            activity_performed="New Memo Submitted",
                            performed_by=submitted_by_id,
                            notified_user_id=qa_head['user_id'],
                            notification_type="memo_submitted",
                            additional_info=f"Memo ID {memo_id} submitted by user ID {submitted_by_id}. Please review."
                        )
        except Exception as notify_err:
            print(f"Error sending memo notifications: {notify_err}")

        return jsonify({
            "success": True,
            "message": "Memo submitted successfully",
            "memo_id": memo_id
        })

    except Exception as e:
        if 'conn' in locals():
            conn.rollback()
        return handle_database_error(get_db_connection(), f"Error submitting memo: {str(e)}")

@memos_bp.route('/api/memos', methods=['GET'])
def get_memos():
    """Get all memos with pagination, filtered by assigned reviewer for QA reviewers"""
    try:
        page = request.args.get('page', 1, type=int)
        limit = request.args.get('limit', 10, type=int)
        offset = (page - 1) * limit
        
        # Get current user information from request headers or query params
        current_user_id = request.args.get('user_id', type=int)
        current_user_role = request.args.get('user_role', type=int)

        conn = get_db_connection()
        cur = conn.cursor()

        # Build query based on user role
        if current_user_role == 3:  # QA Reviewer role
            # For QA reviewers, only show memos assigned to them
            base_query = """
                SELECT 
                    m.memo_id, m.from_person, m.to_person, m.thru_person,
                    m.casdic_ref_no, m.dated, m.wing_proj_ref_no, m.lru_sru_desc,
                    m.part_number, m.manufacturer, m.qty_offered, m.venue,
                    m.memo_date, ma.approval_date as submitted_at, ma.approval_date as accepted_at,
                    u1.name as submitted_by_name,
                    u2.name as accepted_by_name,
                    m.coordinator, m.memo_status
                FROM memos m
                INNER JOIN memo_approval ma ON m.memo_id = ma.memo_id
                LEFT JOIN users u1 ON ma.approved_by = u1.user_id
                LEFT JOIN users u2 ON ma.approved_by = u2.user_id
                WHERE ma.user_id = %s AND ma.status = 'accepted'
                ORDER BY ma.approval_date DESC
            """
            
            count_query = """
                SELECT COUNT(*) 
                FROM memos m
                INNER JOIN memo_approval ma ON m.memo_id = ma.memo_id
                WHERE ma.user_id = %s AND ma.status = 'accepted'
            """
            
            # Get total count for QA reviewer
            cur.execute(count_query, (current_user_id,))
            total_count = cur.fetchone()[0]
            
            # Get memos for QA reviewer
            cur.execute(base_query + " LIMIT %s OFFSET %s", (current_user_id, limit, offset))
        elif current_user_role == 5:  # Designer role
            # For designers, show all memos (since there's no submitted_by column)
            base_query = """
                SELECT 
                    m.memo_id, m.from_person, m.to_person, m.thru_person,
                    m.casdic_ref_no, m.dated, m.wing_proj_ref_no, m.lru_sru_desc,
                    m.part_number, m.manufacturer, m.qty_offered, m.venue,
                    m.memo_date, ma.approval_date as submitted_at, ma.approval_date as accepted_at,
                    u1.name as submitted_by_name,
                    u2.name as accepted_by_name,
                    m.coordinator, m.memo_status
                FROM memos m
                LEFT JOIN memo_approval ma ON m.memo_id = ma.memo_id
                LEFT JOIN users u1 ON ma.approved_by = u1.user_id
                LEFT JOIN users u2 ON ma.approved_by = u2.user_id
                ORDER BY COALESCE(ma.approval_date, m.memo_date) DESC
            """
            
            count_query = """
                SELECT COUNT(*) 
                FROM memos m
            """
            
            # Get total count for designer
            cur.execute(count_query)
            total_count = cur.fetchone()[0]
            
            # Get memos for designer
            cur.execute(base_query + " LIMIT %s OFFSET %s", (limit, offset))
        else:
            # For all other roles, show all memos
            base_query = """
                SELECT 
                    m.memo_id, m.from_person, m.to_person, m.thru_person,
                    m.casdic_ref_no, m.dated, m.wing_proj_ref_no, m.lru_sru_desc,
                    m.part_number, m.manufacturer, m.qty_offered, m.venue,
                    m.memo_date, ma.approval_date as submitted_at, ma.approval_date as accepted_at,
                    u1.name as submitted_by_name,
                    u2.name as accepted_by_name,
                    m.coordinator, m.memo_status
                FROM memos m
                LEFT JOIN memo_approval ma ON m.memo_id = ma.memo_id
                LEFT JOIN users u1 ON ma.approved_by = u1.user_id
                LEFT JOIN users u2 ON ma.approved_by = u2.user_id
                ORDER BY COALESCE(ma.approval_date, m.memo_date) DESC
            """
            
            # Get total count for all other roles
            cur.execute("SELECT COUNT(*) FROM memos")
            total_count = cur.fetchone()[0]
            
            # Get memos for all other roles
            cur.execute(base_query + " LIMIT %s OFFSET %s", (limit, offset))

        memos = cur.fetchall()
        cur.close()

        # Helper function to safely format dates
        def safe_isoformat(date_obj):
            if not date_obj:
                return None
            if hasattr(date_obj, 'isoformat'):
                return date_obj.isoformat()
            return str(date_obj)  # If it's already a string, return as is

        memo_list = []
        for memo in memos:
            memo_list.append({
                "memo_id": memo[0],
                "from_person": memo[1],
                "to_person": memo[2],
                "thru_person": memo[3],
                "casdic_ref_no": memo[4],
                "dated": safe_isoformat(memo[5]),
                "wing_proj_ref_no": memo[6],
                "lru_sru_desc": memo[7],
                "part_number": memo[8],
                "manufacturer": memo[9],
                "qty_offered": memo[10],
                "venue": memo[11],
                "memo_date": safe_isoformat(memo[12]),
                "submitted_at": safe_isoformat(memo[13]),
                "accepted_at": safe_isoformat(memo[14]),
                "submitted_by_name": memo[15],
                "accepted_by_name": memo[16],
                "coordinator": memo[17],
                "memo_status": memo[18]
            })

        return jsonify({
            "success": True,
            "memos": memo_list,
            "total_count": total_count,
            "page": page,
            "limit": limit,
            "total_pages": (total_count + limit - 1) // limit
        })

    except Exception as e:
        return handle_database_error(get_db_connection(), f"Error fetching memos: {str(e)}")

@memos_bp.route('/api/memos/<int:memo_id>', methods=['GET'])
def get_memo_details(memo_id):
    """Get detailed memo information including references"""
    try:
        import psycopg2.extras
        conn = get_db_connection()
        cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

        # Get memo details
        cur.execute("""
            SELECT 
                m.*,
                u1.name as submitted_by_name,
                u2.name as accepted_by_name
            FROM memos m
            LEFT JOIN memo_approval ma ON m.memo_id = ma.memo_id
            LEFT JOIN users u1 ON ma.approved_by = u1.user_id
            LEFT JOIN users u2 ON ma.approved_by = u2.user_id
            WHERE m.memo_id = %s
        """, (memo_id,))

        memo = cur.fetchone()
        if not memo:
            cur.close()
            return jsonify({"success": False, "message": "Memo not found"}), 404

        # Get memo references
        cur.execute("""
            SELECT ref_id, ref_doc, ref_no, ver, rev
            FROM memo_references
            WHERE memo_id = %s
            ORDER BY ref_id
        """, (memo_id,))

        references = cur.fetchall()
        cur.close()

        # Helper function to safely format dates
        def safe_isoformat(date_obj):
            if not date_obj:
                return None
            if hasattr(date_obj, 'isoformat'):
                return date_obj.isoformat()
            return str(date_obj)  # If it's already a string, return as is

        # Convert memo to dictionary (using RealDictCursor, so memo is already a dict)
        memo_dict = {
            "memo_id": memo.get("memo_id"),
            "from_person": memo.get("from_person"),
            "to_person": memo.get("to_person"),
            "thru_person": memo.get("thru_person"),
            "casdic_ref_no": memo.get("casdic_ref_no"),
            "dated": safe_isoformat(memo.get("dated")),
            "wing_proj_ref_no": memo.get("wing_proj_ref_no"),
            "lru_sru_desc": memo.get("lru_sru_desc"),
            "part_number": memo.get("part_number"),
            "slno_units": memo.get("slno_units"),
            "qty_offered": memo.get("qty_offered"),
            "manufacturer": memo.get("manufacturer"),
            "drawing_no_rev": memo.get("drawing_no_rev"),
            "source": memo.get("source"),
            "unit_identification": memo.get("unit_identification"),
            "mechanical_inspn": memo.get("mechanical_inspn"),
            "inspn_test_stage_offered": memo.get("inspn_test_stage_offered"),
            "stte_status": memo.get("stte_status"),
            "test_stage_cleared": memo.get("test_stage_cleared"),
            "venue": memo.get("venue"),
            "memo_date": safe_isoformat(memo.get("memo_date")),
            "name_designation": memo.get("name_designation"),
            "test_facility": memo.get("test_facility"),
            "test_cycle_duration": memo.get("test_cycle_duration"),
            "test_start_on": safe_isoformat(memo.get("test_start_on")),
            "test_complete_on": safe_isoformat(memo.get("test_complete_on")),
            "calibration_status": memo.get("calibration_status"),
            "func_check_initial": safe_isoformat(memo.get("func_check_initial")),
            "perf_check_during": safe_isoformat(memo.get("perf_check_during")),
            "func_check_end": safe_isoformat(memo.get("func_check_end")),
            "certified": memo.get("certified"),
            "remarks": memo.get("remarks"),
            "submitted_at": memo.get("submitted_at"),
            "submitted_by": memo.get("submitted_by"),
            "accepted_at": memo.get("accepted_at"),
            "accepted_by": memo.get("accepted_by"),
            "coordinator": memo.get("coordinator"),
            "memo_status": memo.get("memo_status"),
            "qa_remarks": memo.get("qa_remarks"),
            "submitted_by_name": memo.get("submitted_by_name"),
            "accepted_by_name": memo.get("accepted_by_name")
        }

        # Convert references to list (using RealDictCursor, so ref is already a dict)
        reference_list = []
        for ref in references:
            reference_list.append({
                "ref_id": ref.get("ref_id"),
                "ref_doc": ref.get("ref_doc"),
                "ref_no": ref.get("ref_no"),
                "ver": ref.get("ver"),
                "rev": ref.get("rev")
            })

        return jsonify({
            "success": True,
            "memo": memo_dict,
            "references": reference_list
        })

    except Exception as e:
        return handle_database_error(get_db_connection(), f"Error fetching memo details: {str(e)}")

@memos_bp.route('/api/memos/<int:memo_id>/approve', methods=['POST'])
def approve_memo(memo_id):
    """Approve or reject a memo with file upload support"""
    conn = None
    try:
        print(f"Starting memo approval for memo_id: {memo_id}")
        
        # Handle both JSON and form data
        if request.is_json:
            data = request.json
            print(f"Received JSON data: {data}")
        else:
            data = request.form.to_dict()
            print(f"Received form data: {data}")
        
        if not data:
            return jsonify({"success": False, "message": "No data provided"}), 400

        # Validate required fields
        status = data.get('status')
        if status not in ['accepted', 'rejected']:
            return jsonify({"success": False, "message": "Status must be 'accepted' or 'rejected'"}), 400

        # Check required fields based on status
        if status == 'accepted':
            required_fields = ['status', 'user_id', 'approved_by']
        else:  # rejected
            required_fields = ['status', 'approved_by']
            
        for field in required_fields:
            if field not in data:
                print(f"Missing required field: {field}")
                return jsonify({"success": False, "message": f"Missing required field: {field}"}), 400

        print(f"Connecting to database...")
        conn = get_db_connection()
        cur = conn.cursor()
        
        # Store connection state to check later
        connection_valid = True

        # Check if memo exists
        print(f"Checking if memo {memo_id} exists...")
        cur.execute("SELECT memo_id FROM memos WHERE memo_id = %s", (memo_id,))
        if not cur.fetchone():
            cur.close()
            conn.close()
            return jsonify({"success": False, "message": "Memo not found"}), 404

        # Handle file upload
        attachment_path = None
        if 'attachment' in request.files:
            file = request.files['attachment']
            if file and file.filename:
                print(f"Processing file upload: {file.filename}")
                # Create uploads directory if it doesn't exist
                import os
                upload_dir = os.path.join(os.getcwd(), 'memo_approval_uploads')
                os.makedirs(upload_dir, exist_ok=True)
                
                # Generate unique filename
                import uuid
                file_extension = os.path.splitext(file.filename)[1]
                unique_filename = f"{uuid.uuid4()}{file_extension}"
                attachment_path = os.path.join(upload_dir, unique_filename)
                
                # Save file
                file.save(attachment_path)
                # Store relative path for database
                attachment_path = f"memo_approval_uploads/{unique_filename}"
                print(f"File saved to: {attachment_path}")

        # Update memo approval status (only for accepted memos)
        if status == 'accepted':
            print(f"Updating memo {memo_id} with accepted status...")
            cur.execute("""
                UPDATE memos 
                SET accepted_at = %s, accepted_by = %s, memo_status = 'assigned'
                WHERE memo_id = %s
            """, (datetime.now(), data.get('approved_by'), memo_id))
            
            # Sync report status when memo is accepted and assigned
            cur.execute("""
                UPDATE reports 
                SET status = 'ASSIGNED'
                WHERE memo_id = %s
            """, (memo_id,))
            if cur.rowcount > 0:
                print(f"Updated report status to ASSIGNED for memo {memo_id}")
        elif status == 'rejected':
            print(f"Updating memo {memo_id} with disapproved status...")
            cur.execute("""
                UPDATE memos 
                SET memo_status = 'rejected'
                WHERE memo_id = %s
            """, (memo_id,))
            
            # Remove any existing report for rejected memo
            cur.execute("DELETE FROM reports WHERE memo_id = %s", (memo_id,))
            if cur.rowcount > 0:
                print(f"Removed existing report for rejected memo {memo_id}")
            
            # Send notifications for rejected memo
            # Use a separate connection for notification queries to avoid cursor conflicts
            try:
                from utils.activity_logger import log_notification, get_users_by_role

                performed_by = data.get('approved_by')
                notified_user_ids = set()

                # 1) First get submitter info and role using a separate connection
                conn_notify = get_db_connection()
                cur_notify = conn_notify.cursor()
                cur_notify.execute("""
                    SELECT m.submitted_by, u.name, ur.role_id 
                    FROM memos m 
                    LEFT JOIN users u ON m.submitted_by = u.user_id 
                    LEFT JOIN user_roles ur ON m.submitted_by = ur.user_id
                    WHERE m.memo_id = %s
                """, (memo_id,))
                
                rows = cur_notify.fetchall()
                cur_notify.close()
                conn_notify.close()
                
                submitted_by_id = rows[0][0] if rows else None
                submitted_by_name = rows[0][1] if rows and rows[0][1] else None
                submitter_roles = [r[2] for r in rows] if rows else []
                
                # Determine if submitter is a Design Head
                is_submitter_design_head = 4 in submitter_roles

                # 2) Always notify Design Heads about rejection
                try:
                    design_heads = get_users_by_role(4)
                    for dh in design_heads:
                        dh_id = dh.get('user_id')
                        if not dh_id or dh_id in notified_user_ids:
                            continue
                        
                        # Include submitter info in notification if they're not the design head
                        if submitted_by_id and dh_id != submitted_by_id:
                            submitter_label = submitted_by_name or f"User ID {submitted_by_id}"
                            info = f"Memo ID {memo_id} submitted by {submitter_label} was rejected by QA Head ID {performed_by}."
                        else:
                            info = f"Memo ID {memo_id} has been rejected by QA Head ID {performed_by}."
                        
                        log_notification(
                            project_id=None,
                            activity_performed="Memo Rejected",
                            performed_by=performed_by,
                            notified_user_id=dh_id,
                            notification_type="memo_rejected",
                            additional_info=info
                        )
                        notified_user_ids.add(dh_id)
                except Exception as e:
                    print(f"Error notifying Design Heads about memo rejection: {e}")

                # 3) If submitter is not a Design Head and has role_id = 5 (Designer), notify them about rejection
                if submitted_by_id and not is_submitter_design_head and 5 in submitter_roles:
                    try:
                        if submitted_by_id not in notified_user_ids:
                            log_notification(
                                project_id=None,
                                activity_performed="Your Memo Rejected",
                                performed_by=performed_by,
                                notified_user_id=submitted_by_id,
                                notification_type="memo_rejected",
                                additional_info=f"Your memo (ID {memo_id}) was rejected by QA Head ID {performed_by}."
                            )
                            notified_user_ids.add(submitted_by_id)
                    except Exception as e:
                        print(f"Error notifying submitting designer about memo rejection: {e}")

            except Exception as notify_err:
                print(f"Error during memo rejection notifications: {notify_err}")
        
        # Insert or update memo_approval record
        print(f"Inserting/updating memo_approval record...")
        # Store approval_date as current timestamp when approval is made
        approval_timestamp = datetime.now()
        print(f"Approval timestamp: {approval_timestamp}")

        
        
        # Parse test_date if provided
        test_date = None
        if data.get('test_date'):
            try:
                test_date = datetime.fromisoformat(data.get('test_date').replace('Z', '+00:00'))
                print(f"Test date: {test_date}")
            except ValueError as e:
                print(f"Invalid test_date format: {e}")
                test_date = None
        
        # Check if approval record already exists
        # Ensure connection and cursor are still valid before using them
        # Recreate connection/cursor if needed (after notification code may have affected them)
        try:
            # Try to use the cursor - if it fails, we'll recreate
            # First, verify connection is still open by checking its state
            try:
                # Try a simple query to test connection
                cur.execute("SELECT 1")
                cur.fetchone()
            except:
                # Connection is invalid, recreate it
                print("Connection invalid, recreating...")
                try:
                    if 'cur' in locals() and cur:
                        cur.close()
                except:
                    pass
                try:
                    if 'conn' in locals() and conn:
                        conn.close()
                except:
                    pass
                conn = get_db_connection()
                cur = conn.cursor()
                connection_valid = True
            
            cur.execute("SELECT approval_id FROM memo_approval WHERE memo_id = %s", (memo_id,))
            existing_approval = cur.fetchone()
        except (Exception, AttributeError) as cursor_err:
            # If cursor or connection is invalid, create new ones
            print(f"Cursor/connection error, recreating connection and cursor: {cursor_err}")
            try:
                if 'cur' in locals() and cur:
                    try:
                        cur.close()
                    except:
                        pass
            except:
                pass
            try:
                if 'conn' in locals() and conn:
                    try:
                        conn.close()
                    except:
                        pass
            except:
                pass
            # Create fresh connection and cursor
            conn = get_db_connection()
            cur = conn.cursor()
            connection_valid = True
            cur.execute("SELECT approval_id FROM memo_approval WHERE memo_id = %s", (memo_id,))
            existing_approval = cur.fetchone()
        # Get user_id for database operations (NULL for rejections)
        user_id_for_db = data.get('user_id') if status == 'accepted' else None
        
        if existing_approval:
            # Update existing record
            print(f"Updating existing approval record for memo {memo_id}")
            cur.execute("""
                UPDATE memo_approval 
                SET approval_date = %s, user_id = %s, comments = %s, authentication = %s, 
                    attachment_path = %s, status = %s, approved_by = %s, test_date = %s
                WHERE memo_id = %s
            """, (
                approval_timestamp,
                user_id_for_db,  # QA Reviewer ID for accepted, NULL for rejected
                data.get('comments'),
                data.get('authentication'),
                attachment_path,
                status,
                data.get('approved_by'),  # QA Head ID (person who clicked accept/reject)
                test_date,  # Test date (optional)
                memo_id
            ))
        else:
            # Insert new record
            print(f"Inserting new approval record for memo {memo_id}")
            cur.execute("""
                INSERT INTO memo_approval (memo_id, approval_date, user_id, comments, authentication, attachment_path, status, approved_by, test_date)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                memo_id,
                approval_timestamp,
                user_id_for_db,  # QA Reviewer ID for accepted, NULL for rejected
                data.get('comments'),
                data.get('authentication'),
                attachment_path,
                status,
                data.get('approved_by'),  # QA Head ID (person who clicked accept/reject)
                test_date  # Test date (optional)
            ))

        print("Committing transaction...")
        try:
            conn.commit()
            print("Transaction committed successfully")
        except Exception as commit_err:
            print(f"Error committing transaction: {commit_err}")
            # If commit fails due to connection issues, recreate and retry
            try:
                if hasattr(conn, 'closed') and conn.closed:
                    print("Connection was closed, recreating...")
                    conn = get_db_connection()
                    cur = conn.cursor()
                    # Re-execute the insert/update
                    if existing_approval:
                        cur.execute("""
                            UPDATE memo_approval 
                            SET approval_date = %s, user_id = %s, comments = %s, authentication = %s, 
                                attachment_path = %s, status = %s, approved_by = %s, test_date = %s
                            WHERE memo_id = %s
                        """, (
                            approval_timestamp,
                            user_id_for_db,
                            data.get('comments'),
                            data.get('authentication'),
                            attachment_path,
                            status,
                            data.get('approved_by'),
                            test_date,
                            memo_id
                        ))
                    else:
                        cur.execute("""
                            INSERT INTO memo_approval (memo_id, approval_date, user_id, comments, authentication, attachment_path, status, approved_by, test_date)
                            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                        """, (
                            memo_id,
                            approval_timestamp,
                            user_id_for_db,
                            data.get('comments'),
                            data.get('authentication'),
                            attachment_path,
                            status,
                            data.get('approved_by'),
                            test_date
                        ))
                    conn.commit()
                    print("Transaction committed successfully after recreating connection")
            except Exception as retry_err:
                print(f"Error retrying commit: {retry_err}")
                raise retry_err
        
        # Create report for assigned memo
        if status == 'accepted':
            print(f"Creating report for assigned memo {memo_id}...")
            try:
                # Get memo details to extract project and LRU information
                cur.execute("""
                    SELECT m.wing_proj_ref_no, m.lru_sru_desc, m.part_number, m.venue
                    FROM memos m
                    WHERE m.memo_id = %s
                """, (memo_id,))
                
                memo_details = cur.fetchone()
                if memo_details:
                    # Try to determine project_id based on wing_proj_ref_no
                    default_project_id = 1  # Default project
                    try:
                        cur.execute("""
                            SELECT project_id FROM projects 
                            WHERE LOWER(project_name) = ANY(
                                SELECT LOWER(unnest(string_to_array(%s, '/')))
                            )
                            LIMIT 1
                        """, (memo_details[0],))  # wing_proj_ref_no
                        project_result = cur.fetchone()
                        if project_result:
                            default_project_id = project_result[0]
                    except Exception as e:
                        print(f"Error determining project_id: {e}")
                    
                    # Try to determine lru_id based on lru_sru_desc
                    default_lru_id = 1  # Default LRU
                    try:
                        cur.execute("""
                            SELECT lru_id FROM lrus 
                            WHERE LOWER(lru_name) = LOWER(%s)
                            LIMIT 1
                        """, (memo_details[1],))  # lru_sru_desc
                        lru_result = cur.fetchone()
                        if lru_result:
                            default_lru_id = lru_result[0]
                    except Exception as e:
                        print(f"Error determining lru_id: {e}")
                    
                    # Find or create a serial_id for the LRU
                    default_serial_id = None
                    try:
                        # First, try to find an existing serial_id for this LRU
                        cur.execute("""
                            SELECT serial_id FROM serial_numbers 
                            WHERE lru_id = %s 
                            ORDER BY serial_id 
                            LIMIT 1
                        """, (default_lru_id,))
                        serial_result = cur.fetchone()
                        
                        if serial_result:
                            default_serial_id = serial_result[0]
                        else:
                            # Create a new serial number entry if none exists
                            cur.execute("""
                                INSERT INTO serial_numbers (lru_id, serial_number)
                                VALUES (%s, 1)
                                RETURNING serial_id
                            """, (default_lru_id,))
                            serial_result = cur.fetchone()
                            if serial_result:
                                default_serial_id = serial_result[0]
                                print(f"Created new serial number with serial_id={default_serial_id} for lru_id={default_lru_id}")
                    except Exception as e:
                        print(f"Error determining serial_id: {e}")
                        # Fallback to a safe default
                        default_serial_id = 1
                    
                    if default_serial_id is None:
                        print(f"Could not determine serial_id for memo {memo_id}, skipping report creation")
                        return jsonify({"success": False, "message": "Could not determine serial_id for report creation"}), 500
                    
                    # Check if report already exists for this memo
                    cur.execute("SELECT report_id FROM reports WHERE memo_id = %s", (memo_id,))
                    if not cur.fetchone():
                        # Create new report
                        cur.execute("""
                            INSERT INTO reports (memo_id, project_id, lru_id, serial_id, 
                                               inspection_stage, review_venue, status, created_at)
                            VALUES (%s, %s, %s, %s, %s, %s, %s, NOW())
                        """, (
                            memo_id,
                            default_project_id,
                            default_lru_id,
                            default_serial_id,
                            memo_details[1],  # lru_sru_desc as inspection_stage
                            memo_details[3],  # venue as review_venue
                            'ASSIGNED'
                        ))
                        print(f"Report created successfully for memo {memo_id} with serial_id={default_serial_id}")
                    else:
                        print(f"Report already exists for memo {memo_id}")
                
                # Commit the report creation BEFORE calling notification functions
                conn.commit()
                
                # Notify Design Heads and the submitting Designer about report creation
                # These functions will create their own connections, so call them AFTER committing
                try:
                    from utils.activity_logger import log_notification, get_users_by_role

                    notified_user_ids = set()
                    performed_by = data.get('approved_by')

                    # Fetch submitter using the same connection before closing
                    cur.execute("SELECT submitted_by FROM memos WHERE memo_id = %s", (memo_id,))
                    submit_row = cur.fetchone()
                    submitted_by_id = submit_row[0] if submit_row else None

                    # Close the connection before calling utility functions
                    cur.close()
                    conn.close()

                    # 1) Notify all Design Heads (role_id = 4)
                    try:
                        design_heads = get_users_by_role(4)
                        for dh in design_heads:
                            dh_id = dh.get('user_id')
                            if not dh_id or dh_id in notified_user_ids:
                                continue

                            info = f"A report (Serial ID {default_serial_id}) has been created for Memo ID {memo_id}."
                            log_notification(
                                project_id=None,
                                activity_performed="Report Created",
                                performed_by=performed_by,
                                notified_user_id=dh_id,
                                notification_type="report_created",
                                additional_info=info
                            )
                            notified_user_ids.add(dh_id)
                    except Exception as e:
                        print(f"Error notifying Design Heads about report creation: {e}")

                    # 2) Notify submitting Designer if they are a Designer (role_id = 5)
                    try:
                        if submitted_by_id and submitted_by_id not in notified_user_ids:
                            conn3 = get_db_connection()
                            cur3 = conn3.cursor()
                            cur3.execute("SELECT 1 FROM user_roles WHERE user_id = %s AND role_id = 5", (submitted_by_id,))
                            is_designer = cur3.fetchone()
                            cur3.close()
                            conn3.close()
                            
                            if is_designer:
                                log_notification(
                                    project_id=None,
                                    activity_performed="Your Report Created",
                                    performed_by=performed_by,
                                    notified_user_id=submitted_by_id,
                                    notification_type="report_created_submitted_by_designer",
                                    additional_info=f"A report has been created for your memo (ID {memo_id}). Serial ID {default_serial_id}."
                                )
                                notified_user_ids.add(submitted_by_id)
                    except Exception as e:
                        print(f"Error notifying submitting designer about report creation: {e}")

                except Exception as notify_err:
                    print(f"Error during report creation notifications: {notify_err}")
            except Exception as report_error:
                print(f"Error creating report for memo {memo_id}: {str(report_error)}")
                # Don't fail the entire operation if report creation fails
                try:
                    if 'conn' in locals() and conn and not conn.closed:
                        conn.rollback()
                        conn.commit()  # Re-commit the memo approval
                except Exception as rollback_err:
                    print(f"Error during rollback: {rollback_err}")
        
        # Close the main connection if it's still open
        try:
            if 'cur' in locals() and cur:
                cur.close()
            if 'conn' in locals() and conn and not conn.closed:
                conn.close()
        except Exception as close_err:
            print(f"Error closing connection: {close_err}")
        
        # Log memo assignment/rejection activity
        # This function will create its own connection
        from utils.activity_logger import log_activity
        
        # Get memo details for logging using a new connection
        conn_log = get_db_connection()
        cur_log = conn_log.cursor()
        cur_log.execute("SELECT lru_sru_desc FROM memos WHERE memo_id = %s", (memo_id,))
        memo_name = cur_log.fetchone()
        memo_name = memo_name[0] if memo_name else 'Memo'
        cur_log.close()
        conn_log.close()
        
        activity_type = "Memo Assigned" if status == 'accepted' else "Memo Rejected"
        log_activity(
            project_id=None,  # Memo operations don't have project_id
            activity_performed=activity_type,
            performed_by=data.get('approved_by'),
            additional_info=f"ID:{memo_id}|Name:{memo_name}|Memo '{memo_name}' (ID: {memo_id}) was {status}"
        )

        # Send notifications when memo is accepted
        # These functions will create their own connections, so call them AFTER all commits
        if status == 'accepted':
            try:
                from utils.activity_logger import log_notification, get_users_by_role

                performed_by = data.get('approved_by')

                # Keep track of who we've notified to avoid duplicates
                notified_user_ids = set()

                # Get a new connection to fetch submitter info
                conn_notify = get_db_connection()
                cur_notify = conn_notify.cursor()

                # 1) Notify all Design Heads (role_id = 4) — always notify them regardless of who submitted
                #    If the memo was submitted by someone else, include submitter id/name in the message.
                try:
                    # Fetch submitter info to include in Design Head notifications
                    cur_notify.execute("SELECT m.submitted_by, u.name FROM memos m LEFT JOIN users u ON m.submitted_by = u.user_id WHERE m.memo_id = %s", (memo_id,))
                    submit_row = cur_notify.fetchone()
                    submitted_by_id = submit_row[0] if submit_row else None
                    submitted_by_name = submit_row[1] if submit_row and submit_row[1] else None
                    cur_notify.close()
                    conn_notify.close()

                    design_heads = get_users_by_role(4)
                    for dh in design_heads:
                        dh_id = dh.get('user_id')
                        if not dh_id or dh_id in notified_user_ids:
                            continue

                        # If the design head is NOT the submitter, mention who submitted the memo
                        if submitted_by_id and dh_id != submitted_by_id:
                            submitter_label = submitted_by_name or f"User ID {submitted_by_id}"
                            info = f"Memo ID {memo_id} submitted by {submitter_label} was accepted by QA Head ID {performed_by}."
                        else:
                            info = f"Memo ID {memo_id} has been accepted by QA Head ID {performed_by}."

                        log_notification(
                            project_id=None,
                            activity_performed="Memo Accepted",
                            performed_by=performed_by,
                            notified_user_id=dh_id,
                            notification_type="memo_accepted",
                            additional_info=info
                        )
                        notified_user_ids.add(dh_id)
                except Exception as e:
                    print(f"Error notifying Design Heads about memo acceptance: {e}")

                # 2) Notify the submitting Designer only if the memo was submitted by a Designer (role_id = 5)
                try:
                    conn_notify2 = get_db_connection()
                    cur_notify2 = conn_notify2.cursor()
                    cur_notify2.execute("SELECT submitted_by FROM memos WHERE memo_id = %s", (memo_id,))
                    row = cur_notify2.fetchone()
                    submitted_by_id = row[0] if row else None
                    if submitted_by_id:
                        # Check if submitted_by has role_id = 5 (Designer)
                        cur_notify2.execute("SELECT 1 FROM user_roles WHERE user_id = %s AND role_id = 5", (submitted_by_id,))
                        is_designer = cur_notify2.fetchone()
                        cur_notify2.close()
                        conn_notify2.close()
                        
                        if is_designer:
                            # Only notify the submitting designer if they haven't already been notified (e.g., as a Design Head)
                            if submitted_by_id not in notified_user_ids:
                                log_notification(
                                    project_id=None,
                                    activity_performed="Your Memo Accepted",
                                    performed_by=performed_by,
                                    notified_user_id=submitted_by_id,
                                    notification_type="memo_accepted_submitted_by_designer",
                                    additional_info=f"Your memo (ID {memo_id}) was accepted by QA Head ID {performed_by}."
                                )
                                notified_user_ids.add(submitted_by_id)
                except Exception as e:
                    print(f"Error notifying submitting designer about memo acceptance: {e}")

                # 3) Notify the assigned reviewer (if provided in the approval request)
                try:
                    assigned_reviewer_id = data.get('user_id') if data else None
                    if assigned_reviewer_id:
                        # Verify reviewer exists (optional) and notify
                        conn_notify3 = get_db_connection()
                        cur_notify3 = conn_notify3.cursor()
                        cur_notify3.execute("SELECT user_id, name FROM users WHERE user_id = %s", (assigned_reviewer_id,))
                        reviewer_row = cur_notify3.fetchone()
                        cur_notify3.close()
                        conn_notify3.close()
                        
                        if reviewer_row:
                            if assigned_reviewer_id not in notified_user_ids:
                                reviewer_name = reviewer_row[1] if reviewer_row[1] else f"User ID {assigned_reviewer_id}"
                                log_notification(
                                    project_id=None,
                                    activity_performed="Memo Assigned to You",
                                    performed_by=performed_by,
                                    notified_user_id=assigned_reviewer_id,
                                    notification_type="memo_assigned",
                                    additional_info=f"You have been assigned to review Memo ID {memo_id} by QA Head ID {performed_by}."
                                )
                                notified_user_ids.add(assigned_reviewer_id)
                except Exception as e:
                    print(f"Error notifying assigned reviewer about memo assignment: {e}")

            except Exception as notify_err:
                print(f"Error during memo acceptance notifications: {notify_err}")

        return jsonify({
            "success": True,
            "message": f"Memo {status} successfully"
        })

    except Exception as e:
        print(f"Error in approve_memo: {str(e)}")
        import traceback
        traceback.print_exc()
        try:
            if 'conn' in locals() and conn and not conn.closed:
                conn.rollback()
                conn.close()
        except Exception as rollback_err:
            print(f"Error during rollback in exception handler: {rollback_err}")
        return jsonify({"success": False, "message": f"Error approving memo: {str(e)}"}), 500

@memos_bp.route('/api/memos/<int:memo_id>/approval-status', methods=['GET'])
def get_memo_approval_status(memo_id):
    """Get memo approval status and assigned reviewer information"""
    try:
        conn = get_db_connection()
        cur = conn.cursor()

        # Get memo approval status
        cur.execute("""
            SELECT approval_id, memo_id, user_id, comments, authentication, 
                   attachment_path, status, approval_date, approved_by, test_date
            FROM memo_approval 
            WHERE memo_id = %s
        """, (memo_id,))
        
        approval_record = cur.fetchone()
        
        if not approval_record:
            cur.close()
            return jsonify({"success": True, "message": "No approval record found", "approval": None}), 200

        # Get reviewer details (only if user_id is not NULL)
        reviewer_id = approval_record[2]  # user_id
        reviewer = None
        
        if reviewer_id:
            cur.execute("""
                SELECT u.user_id, u.name, u.email, r.role_name
                FROM users u
                JOIN user_roles ur ON u.user_id = ur.user_id
                JOIN roles r ON ur.role_id = r.role_id
                WHERE u.user_id = %s
            """, (reviewer_id,))
            
            reviewer = cur.fetchone()
        
        # Get approver details (person who approved/rejected the memo)
        approver_id = approval_record[8]  # approved_by
        approver = None
        
        if approver_id:
            cur.execute("""
                SELECT u.user_id, u.name, u.email, r.role_name
                FROM users u
                JOIN user_roles ur ON u.user_id = ur.user_id
                JOIN roles r ON ur.role_id = r.role_id
                WHERE u.user_id = %s
            """, (approver_id,))
            
            approver = cur.fetchone()
        
        cur.close()

        if reviewer_id and not reviewer:
            return jsonify({"success": False, "message": "Reviewer not found"}), 404

        approval_data = {
            "approval_id": approval_record[0],
            "memo_id": approval_record[1],
            "user_id": approval_record[2],
            "comments": approval_record[3],
            "authentication": approval_record[4],
            "attachment_path": approval_record[5],
            "status": approval_record[6],
            "approval_date": approval_record[7].isoformat() if approval_record[7] else None,
            "approved_by": approval_record[8],
            "test_date": approval_record[9].isoformat() if approval_record[9] else None,
            "reviewer": {
                "id": reviewer[0],
                "name": reviewer[1],
                "email": reviewer[2],
                "role": reviewer[3]
            } if reviewer else None,
            "approver": {
                "id": approver[0],
                "name": approver[1],
                "email": approver[2],
                "role": approver[3]
            } if approver else None
        }

        return jsonify({
            "success": True,
            "approval": approval_data
        })

    except Exception as e:
        print(f"Error fetching memo approval status: {str(e)}")
        return jsonify({"success": False, "message": f"Error fetching approval status: {str(e)}"}), 500

@memos_bp.route('/api/memos/share', methods=['POST'])
def share_memo():
    """Share a memo with another QA reviewer"""
    try:
        data = request.json
        if not data:
            return jsonify({"success": False, "message": "No data provided"}), 400

        # Validate required fields
        required_fields = ['memo_id', 'shared_by', 'shared_with']
        for field in required_fields:
            if field not in data:
                return jsonify({"success": False, "message": f"Missing required field: {field}"}), 400

        memo_id = data.get('memo_id')
        shared_by = data.get('shared_by')
        shared_with = data.get('shared_with')

        # Check if trying to share with self
        if shared_by == shared_with:
            return jsonify({"success": False, "message": "Cannot share memo with yourself"}), 400

        conn = get_db_connection()
        cur = conn.cursor()

        # Check if memo exists
        cur.execute("SELECT memo_id FROM memos WHERE memo_id = %s", (memo_id,))
        if not cur.fetchone():
            cur.close()
            return jsonify({"success": False, "message": "Memo not found"}), 404

        # Check if both users are QA reviewers
        cur.execute("""
            SELECT u.user_id, r.role_name
            FROM users u
            JOIN user_roles ur ON u.user_id = ur.user_id
            JOIN roles r ON ur.role_id = r.role_id
            WHERE u.user_id IN (%s, %s) AND r.role_name = 'QA Reviewer'
        """, (shared_by, shared_with))
        
        reviewers = cur.fetchall()
        if len(reviewers) != 2:
            cur.close()
            return jsonify({"success": False, "message": "Both users must be QA reviewers"}), 400

        # Insert sharing record
        cur.execute("""
            INSERT INTO shared_memos (memo_id, shared_by, shared_with)
            VALUES (%s, %s, %s)
            RETURNING share_id
        """, (memo_id, shared_by, shared_with))

        share_id = cur.fetchone()[0]
        conn.commit()
        cur.close()

        return jsonify({
            "success": True,
            "message": "Memo shared successfully",
            "share_id": share_id
        })

    except Exception as e:
        if 'conn' in locals():
            conn.rollback()
        print(f"Error sharing memo: {str(e)}")
        return jsonify({"success": False, "message": f"Error sharing memo: {str(e)}"}), 500

@memos_bp.route('/api/reviewers', methods=['GET'])
def get_qa_reviewers():
    """Get list of QA reviewers for sharing dropdown (excluding current user)"""
    try:
        # Get current user ID from query parameter
        current_user_id = request.args.get('current_user_id', type=int)
        
        conn = get_db_connection()
        cur = conn.cursor()

        if current_user_id:
            # Exclude current user from the list
            cur.execute("""
                SELECT u.user_id, u.name, u.email
                FROM users u
                JOIN user_roles ur ON u.user_id = ur.user_id
                JOIN roles r ON ur.role_id = r.role_id
                WHERE r.role_name = 'QA Reviewer' AND u.user_id != %s
                ORDER BY u.name
            """, (current_user_id,))
        else:
            # If no current user ID provided, return all QA reviewers
            cur.execute("""
                SELECT u.user_id, u.name, u.email
                FROM users u
                JOIN user_roles ur ON u.user_id = ur.user_id
                JOIN roles r ON ur.role_id = r.role_id
                WHERE r.role_name = 'QA Reviewer'
                ORDER BY u.name
            """)

        reviewers = cur.fetchall()
        cur.close()

        reviewer_list = []
        for reviewer in reviewers:
            reviewer_list.append({
                "user_id": reviewer[0],
                "name": reviewer[1],
                "email": reviewer[2]
            })

        return jsonify({
            "success": True,
            "reviewers": reviewer_list
        })

    except Exception as e:
        print(f"Error fetching QA reviewers: {str(e)}")
        return jsonify({"success": False, "message": f"Error fetching reviewers: {str(e)}"}), 500

@memos_bp.route('/api/memos/shared', methods=['GET'])
def get_shared_memos():
    """Get memos shared with the current user"""
    try:
        user_id = request.args.get('user_id', type=int)
        if not user_id:
            return jsonify({"success": False, "message": "User ID is required"}), 400

        conn = get_db_connection()
        cur = conn.cursor()

        # Get memos shared with the user
        cur.execute("""
            SELECT 
                m.memo_id, m.from_person, m.to_person, m.thru_person,
                m.casdic_ref_no, m.dated, m.wing_proj_ref_no, m.lru_sru_desc,
                m.part_number, m.manufacturer, m.qty_offered, m.venue,
                m.memo_date, ma.approval_date as submitted_at, ma.approval_date as accepted_at,
                u1.name as submitted_by_name,
                u2.name as accepted_by_name,
                m.coordinator, m.memo_status,
                sm.shared_at, u3.name as shared_by_name
            FROM shared_memos sm
            JOIN memos m ON sm.memo_id = m.memo_id
            LEFT JOIN memo_approval ma ON m.memo_id = ma.memo_id
            LEFT JOIN users u1 ON ma.approved_by = u1.user_id
            LEFT JOIN users u2 ON ma.approved_by = u2.user_id
            LEFT JOIN users u3 ON sm.shared_by = u3.user_id
            WHERE sm.shared_with = %s
            ORDER BY sm.shared_at DESC
        """, (user_id,))

        shared_memos = cur.fetchall()
        cur.close()

        # Helper function to safely format dates
        def safe_isoformat(date_obj):
            if not date_obj:
                return None
            if hasattr(date_obj, 'isoformat'):
                return date_obj.isoformat()
            return str(date_obj)

        memo_list = []
        for memo in shared_memos:
            memo_list.append({
                "memo_id": memo[0],
                "from_person": memo[1],
                "to_person": memo[2],
                "thru_person": memo[3],
                "casdic_ref_no": memo[4],
                "dated": safe_isoformat(memo[5]),
                "wing_proj_ref_no": memo[6],
                "lru_sru_desc": memo[7],
                "part_number": memo[8],
                "manufacturer": memo[9],
                "qty_offered": memo[10],
                "venue": memo[11],
                "memo_date": safe_isoformat(memo[12]),
                "submitted_at": safe_isoformat(memo[13]),
                "accepted_at": safe_isoformat(memo[14]),
                "submitted_by_name": memo[15],
                "accepted_by_name": memo[16],
                "coordinator": memo[17],
                "memo_status": memo[18],
                "shared_at": safe_isoformat(memo[19]),
                "shared_by_name": memo[20]
            })

        return jsonify({
            "success": True,
            "shared_memos": memo_list
        })

    except Exception as e:
        print(f"Error fetching shared memos: {str(e)}")
        return jsonify({"success": False, "message": f"Error fetching shared memos: {str(e)}"}), 500

@memos_bp.route('/api/memos/<int:memo_id>/status', methods=['PUT'])
def update_memo_status(memo_id):
    """Update memo status based on reviewer's test status selection"""
    try:
        data = request.json
        if not data:
            return jsonify({"success": False, "message": "No data provided"}), 400
        
        # Validate required fields
        if 'test_status' not in data:
            return jsonify({"success": False, "message": "test_status is required"}), 400
        
        if 'reviewer_comments' not in data:
            return jsonify({"success": False, "message": "reviewer_comments is required"}), 400
        
        # Map frontend test status to database memo_status
        status_mapping = {
            'Successfully completed': 'successfully_completed',
            'Test not conducted': 'test_not_conducted', 
            'Completed with observations': 'completed_with_observations',
            'Test failed': 'test_failed'
        }
        
        test_status = data['test_status']
        if test_status not in status_mapping:
            return jsonify({"success": False, "message": "Invalid test status"}), 400
        
        memo_status = status_mapping[test_status]
        
        print(f"=== DEBUG: Updating memo status ===")
        print(f"memo_id: {memo_id}")
        print(f"test_status: {test_status}")
        print(f"memo_status: {memo_status}")
        print(f"reviewer_comments: {data.get('reviewer_comments', '')}")
        print(f"=== END DEBUG ===")
        
        conn = get_db_connection()
        cur = conn.cursor()
        
        # Update memo status, reviewer comments, and certification data
        reviewer_comments = data.get('reviewer_comments', '')
        certified = data.get('certified', [])
        
        print(f"=== DEBUG: Certification data ===")
        print(f"certified: {certified}")
        print(f"=== END DEBUG ===")
        
        cur.execute("""
            UPDATE memos 
            SET memo_status = %s, qa_remarks = %s, certified = %s
            WHERE memo_id = %s
        """, (memo_status, reviewer_comments, certified, memo_id))
        
        if cur.rowcount == 0:
            cur.close()
            return jsonify({"success": False, "message": "Memo not found"}), 404
        
        # Map memo status to report status
        # Mapping: memo_status -> report status
        status_mapping = {
            'assigned': 'ASSIGNED',
            'successfully_completed': 'SUCCESSFULLY COMPLETED',
            'completed_with_observations': 'COMPLETED WITH OBSERVATIONS',
            'test_failed': 'TEST FAILED',
            'test_not_conducted': 'TEST NOT CONDUCTED'
        }
        
        # Get corresponding report status
        report_status = status_mapping.get(memo_status)
        
        if report_status:
            # Update corresponding report status (one-to-one relationship)
            cur.execute("""
                UPDATE reports 
                SET status = %s
                WHERE memo_id = %s
            """, (report_status, memo_id))
            
            if cur.rowcount > 0:
                print(f"Updated report status to {report_status} for memo {memo_id}")
            else:
                print(f"Warning: No report found for memo {memo_id} to update status")
        
        conn.commit()
        cur.close()
        
        return jsonify({
            "success": True,
            "message": f"Memo status updated to {test_status}",
            "memo_status": memo_status
        })
        
    except Exception as e:
        return handle_database_error(get_db_connection(), f"Error updating memo status: {str(e)}")

@memos_bp.route('/api/memos/<int:memo_id>/pdf', methods=['GET'])
def download_memo_pdf(memo_id):
    """Generate and download PDF for a specific memo"""
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        
        # Fetch memo details with all related information
        cur.execute("""
            SELECT 
                m.memo_id,
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
                m.qa_remarks,
                m.memo_status,
                m.wing_proj_ref_no,
                m.lru_sru_desc,
                m.part_number,
                m.qty_offered,
                m.slno_units,
                m.unit_identification,
                m.mechanical_inspn,
                m.inspn_test_stage_offered,
                m.stte_status,
                m.test_stage_cleared,
                m.remarks,
                m.submitted_at,
                m.submitted_by,
                m.accepted_at,
                m.accepted_by,
                m.qa_signature,
                m.coordinator
            FROM memos m
            WHERE m.memo_id = %s
        """, (memo_id,))
        
        memo = cur.fetchone()
        if not memo:
            cur.close()
            return jsonify({"success": False, "message": "Memo not found"}), 404
        
        # Fetch memo references
        cur.execute("""
            SELECT ref_doc, ref_no, ver, rev
            FROM memo_references
            WHERE memo_id = %s
            ORDER BY ref_doc
        """, (memo_id,))
        
        references = cur.fetchall()
        
        # Fetch memo approval status and details
        cur.execute("""
            SELECT ma.status, ma.approval_date, ma.comments, ma.authentication, 
                   ma.approved_by, u1.name as approver_name,
                   ma.user_id, u2.name as reviewer_name, ma.test_date, ma.attachment_path
            FROM memo_approval ma
            LEFT JOIN users u1 ON ma.approved_by = u1.user_id
            LEFT JOIN users u2 ON ma.user_id = u2.user_id
            WHERE ma.memo_id = %s
        """, (memo_id,))
        
        approval_data = cur.fetchone()
        cur.close()
        
        # Generate PDF
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=A4, topMargin=0.5*inch, bottomMargin=0.5*inch, leftMargin=0.5*inch, rightMargin=0.5*inch)
        
        # Define styles
        styles = getSampleStyleSheet()
        
        # Title style (matches frontend)
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=18,
            spaceAfter=20,
            alignment=1,  # Center alignment
            textColor=colors.black,
            fontName='Helvetica-Bold'
        )
        
        # Section heading style (matches frontend)
        section_style = ParagraphStyle(
            'SectionHeading',
            parent=styles['Heading2'],
            fontSize=13,
            spaceAfter=15,
            spaceBefore=15,
            textColor=colors.black,
            fontName='Helvetica-Bold'
        )
        
        # Status badge style
        status_badge_style = ParagraphStyle(
            'StatusBadge',
            parent=styles['Normal'],
            fontSize=9,
            spaceAfter=15,
            spaceBefore=10,
            alignment=1,  # Center alignment
            fontName='Helvetica-Bold',
            backColor=colors.lightgrey,
            borderWidth=1,
            borderPadding=8
        )
        
        # Test review heading style
        test_review_heading_style = ParagraphStyle(
            'TestReviewHeading',
            parent=styles['Heading3'],
            fontSize=13,
            spaceAfter=15,
            spaceBefore=10,
            textColor=colors.black,
            fontName='Helvetica-Bold'
        )
        
        # Build PDF content
        story = []
        
        # Title (matches frontend exactly)
        story.append(Paragraph("REQUISITION FOR DGAQA INSPECTION", title_style))
        story.append(Spacer(1, 10))
        
        # Requisition Details Section
        story.append(Paragraph("REQUISITION DETAILS", section_style))
        
        # Create compact requisition details table
        req_data = [
            ['From:', memo[1] or 'N/A', 'CASDIC Ref No.:', 'CASDIC/', memo[4] or 'N/A', 'Dated:', memo[5].strftime('%Y-%m-%d') if memo[5] else 'N/A'],
            ['To:', memo[2] or 'N/A', '', 'Thru: O I/c, WH', '', 'Wing/Proj Ref No.:', memo[23] or 'N/A'],
            ['', '', '', 'Name & contact No of CASDIC (Designs) coordinator:', memo[39] or 'N/A', '', '']
        ]
        
        req_table = Table(req_data, colWidths=[0.5*inch, 1.5*inch, 0.5*inch, 1.2*inch, 1.2*inch, 0.4*inch, 1.2*inch])
        req_table.setStyle(TableStyle([
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 7),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('LEFTPADDING', (0, 0), (-1, -1), 3),
            ('RIGHTPADDING', (0, 0), (-1, -1), 3),
            ('TOPPADDING', (0, 0), (-1, -1), 3),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
        ]))
        
        story.append(req_table)
        story.append(Spacer(1, 8))
        
        # LRU/SRU Details Section
        story.append(Paragraph("LRU/SRU DETAILS", section_style))
        
        # Create compact LRU/SRU table
        lru_header = [
            ['LRU/SRU DETAILS', 'LRU/SRU Desc', 'Ref. Docnt', '', '', ''],
            ['', '', 'Ref Doc', 'Ref No of Document', 'ver', 'rev']
        ]
        
        lru_data = [
            ['Part No:', memo[25] or 'N/A', '', '', '', ''],
            ['Manufacturer:', memo[6] or 'N/A', memo[7] or 'N/A', memo[4] or 'N/A', '1.0', 'A']
        ]
        
        # Add additional reference rows (up to 5 more)
        for i in range(5):
            lru_data.append(['', '', '', '', '', ''])
        
        lru_table_data = lru_header + lru_data
        lru_table = Table(lru_table_data, colWidths=[1.5*inch, 1.8*inch, 1*inch, 1.2*inch, 0.6*inch, 0.6*inch])
        lru_table.setStyle(TableStyle([
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 7),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('LEFTPADDING', (0, 0), (-1, -1), 3),
            ('RIGHTPADDING', (0, 0), (-1, -1), 3),
            ('TOPPADDING', (0, 0), (-1, -1), 3),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
            ('BACKGROUND', (0, 0), (-1, 1), colors.lightgrey),
            ('FONTNAME', (0, 0), (-1, 1), 'Helvetica-Bold'),
        ]))
        
        story.append(lru_table)
        story.append(Spacer(1, 8))
        
        # Additional Details Section
        story.append(Paragraph("ADDITIONAL DETAILS", section_style))
        
        # Create compact additional details table
        add_details_data = [
            ['Drawing no/Rev:', memo[7] or 'N/A', 'source:', memo[8] or 'N/A', 'Sl.No of units:', ', '.join(memo[27]) if memo[27] and isinstance(memo[27], list) else str(memo[27]) if memo[27] else 'N/A'],
            ['Qty Offered:', str(memo[26]) if memo[26] else 'N/A', 'UNIT IDENTIFICATION:', ', '.join(memo[28]) if memo[28] and isinstance(memo[28], list) else str(memo[28]) if memo[28] else 'N/A', '', ''],
            ['MECHANICAL INSPECTION:', memo[29] or 'N/A', 'INSPECTION /TEST STAGE OFFERED NOW:', memo[30] or 'N/A', '', ''],
            ['Test stage cleared:', memo[32] or 'N/A', 'STTE Status:', memo[31] or 'N/A', '', '']
        ]
        
        add_table = Table(add_details_data, colWidths=[1.2*inch, 1.8*inch, 1.2*inch, 1.8*inch, 0.5*inch, 0.5*inch])
        add_table.setStyle(TableStyle([
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 7),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('LEFTPADDING', (0, 0), (-1, -1), 3),
            ('RIGHTPADDING', (0, 0), (-1, -1), 3),
            ('TOPPADDING', (0, 0), (-1, -1), 3),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
        ]))
        
        story.append(add_table)
        story.append(Spacer(1, 8))
        
        # Testing Details Section
        story.append(Paragraph("TESTING DETAILS", section_style))
        
        # Create compact testing details table
        testing_data = [
            ['Above Unit is ready for Testing at venue, dated onwards.', memo[9] or 'N/A', 'memo date:', memo[10].strftime('%Y-%m-%d') if memo[10] else 'N/A'],
            ['Name / designation:', memo[11] or 'N/A', '', ''],
            ['Test facility to be used:', memo[12] or 'N/A', 'Test cycle / Duration:', memo[13] or 'N/A'],
            ['Test Start on:', memo[14].strftime('%Y-%m-%d %H:%M') if memo[14] else 'N/A', 'Test complete on:', memo[15].strftime('%Y-%m-%d %H:%M') if memo[15] else 'N/A'],
            ['Calibration status OK/Due on:', memo[16] or 'N/A', '', ''],
            ['Func. Check(Initial):', memo[17].strftime('%Y-%m-%d %H:%M') if memo[17] else 'N/A', 'Perf. check (during):', memo[18].strftime('%Y-%m-%d %H:%M') if memo[18] else 'N/A'],
            ['Func Check (End):', memo[19].strftime('%Y-%m-%d %H:%M') if memo[19] else 'N/A', '', '']
        ]
        
        testing_table = Table(testing_data, colWidths=[1.5*inch, 2*inch, 1*inch, 2*inch])
        testing_table.setStyle(TableStyle([
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 7),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('LEFTPADDING', (0, 0), (-1, -1), 3),
            ('RIGHTPADDING', (0, 0), (-1, -1), 3),
            ('TOPPADDING', (0, 0), (-1, -1), 3),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
        ]))
        
        story.append(testing_table)
        story.append(Spacer(1, 8))
        
        # Certification Section
        story.append(Paragraph("CERTIFICATION", section_style))
        story.append(Paragraph("It is certified that:", ParagraphStyle('CertTitle', parent=styles['Normal'], fontSize=8, spaceAfter=6, fontName='Helvetica-Bold')))
        
        # Handle certified array properly
        certified_items = []
        if memo[20] and isinstance(memo[20], list):
            certified_items = memo[20]
        elif memo[20]:
            certified_items = [memo[20]]
        
        certifications = [
            "Mechanical Quality Records verified thoroughly",
            "CoC for SRU, fasteners & standard parts verified", 
            "Sl no of the SRUs noted in log book",
            "No Defect investigation pending",
            "All previous test stages cleared",
            "CASCIC QA has physically inspected and accepted"
        ]
        
        cert_data = []
        for i, cert in enumerate(certifications):
            checkbox = "☑" if (i < len(certified_items) and certified_items[i]) else "☐"
            cert_data.append([checkbox, cert])
        
        cert_table = Table(cert_data, colWidths=[0.25*inch, 6.5*inch])
        cert_table.setStyle(TableStyle([
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 7),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('LEFTPADDING', (0, 0), (-1, -1), 3),
            ('RIGHTPADDING', (0, 0), (-1, -1), 3),
            ('TOPPADDING', (0, 0), (-1, -1), 2),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 2),
        ]))
        
        story.append(cert_table)
        story.append(Spacer(1, 8))
        
        # Remarks Section
        story.append(Paragraph("REMARKS", section_style))
        remarks_text = memo[33] or 'No remarks provided'
        story.append(Paragraph(remarks_text, ParagraphStyle('Remarks', parent=styles['Normal'], fontSize=7, spaceAfter=6, fontName='Helvetica')))
        
        story.append(Spacer(1, 10))
        
        # Approval/Rejection Status Section (only if memo has been processed)
        if approval_data:
            status = approval_data[0]  # ma.status
            
            # Status badge (matches frontend exactly)
            if status == 'accepted':
                status_text = "✓ APPROVED AND ASSIGNED REVIEWER"
                status_color = colors.green
                section_bg_color = colors.Color(0.94, 0.98, 0.94)  # #f0f9f0
                section_border_color = colors.green
            elif status == 'rejected':
                status_text = "✗ REJECTED"
                status_color = colors.red
                section_bg_color = colors.Color(0.99, 0.95, 0.95)  # #fdf2f2
                section_border_color = colors.red
            
            # Add section background and border (simulated with table)
            section_table_data = [['']]
            section_table = Table(section_table_data, colWidths=[7*inch], rowHeights=[0.1*inch])
            section_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, -1), section_bg_color),
                ('LINEBELOW', (0, 0), (-1, -1), 2, section_border_color),
                ('LINEABOVE', (0, 0), (-1, -1), 2, section_border_color),
                ('LINELEFT', (0, 0), (-1, -1), 2, section_border_color),
                ('LINERIGHT', (0, 0), (-1, -1), 2, section_border_color),
            ]))
            story.append(section_table)
            
            # Status badge
            status_style = ParagraphStyle(
                'StatusBadge',
                parent=styles['Normal'],
                fontSize=9,
                spaceAfter=15,
                spaceBefore=10,
                alignment=1,  # Center alignment
                textColor=status_color,
                fontName='Helvetica-Bold',
                backColor=colors.lightgrey,
                borderWidth=1,
                borderPadding=8
            )
            story.append(Paragraph(status_text, status_style))
            
            # Test or Review Details heading
            story.append(Paragraph("Test or Review Details", test_review_heading_style))
            
            # Create test review details table (matches frontend layout exactly)
            test_review_data = []
            
            # Row 1: Date and Comments
            approval_date = approval_data[1]  # ma.approval_date
            comments = approval_data[2]  # ma.comments
            
            date_str = approval_date.strftime('%d/%m/%Y, %H:%M') if approval_date else 'N/A'
            comments_str = comments or 'No comments provided'
            
            test_review_data.append([
                f'Date of Test or Review :\n{date_str}',
                f'Comments :\n{comments_str}'
            ])
            
            # Row 2: Tester ID and Name
            if status == 'accepted':
                reviewer_name = approval_data[7]  # reviewer_name
                reviewer_id = approval_data[6]  # ma.user_id
                test_review_data.append([
                    f'Internal Tester ID:\n{reviewer_id or "N/A"}',
                    f'Internal Tester Name :\n{reviewer_name or "N/A"}'
                ])
            else:  # rejected
                approver_id = approval_data[4]  # ma.approved_by
                test_review_data.append([
                    f'Internal Tester ID:\n{approver_id or "N/A"}',
                    f'Internal Tester Name :\nQA Head'
                ])
            
            # Row 3: Authentication and Attachments
            authentication = approval_data[3]  # ma.authentication
            attachment_path = approval_data[9]  # ma.attachment_path
            
            # For now, show authentication status in table
            auth_str = 'Signature provided' if authentication else 'Not provided'
            attachment_str = 'File attached' if attachment_path else 'No attachments'
            
            test_review_data.append([
                f'Authentication\n{auth_str}',
                f'Attachments\n{attachment_str}'
            ])
            
            # Create test review table
            test_review_table = Table(test_review_data, colWidths=[3.5*inch, 3.5*inch])
            test_review_table.setStyle(TableStyle([
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
                ('FONTSIZE', (0, 0), (-1, -1), 9),
                ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                ('LEFTPADDING', (0, 0), (-1, -1), 12),
                ('RIGHTPADDING', (0, 0), (-1, -1), 12),
                ('TOPPADDING', (0, 0), (-1, -1), 12),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
                ('BACKGROUND', (0, 0), (-1, -1), colors.white),
            ]))
            
            story.append(test_review_table)
            
            # Add signature image if available (access directly from file path)
            if authentication:
                try:
                    from reportlab.lib.utils import ImageReader
                    import os
                    
                    # Handle signature path - try different path formats
                    signature_path = None
                    
                    # Check if it's already a full file path
                    if os.path.exists(authentication):
                        signature_path = authentication
                    # Check if it's a relative path from project root
                    elif os.path.exists(os.path.join(os.getcwd(), authentication)):
                        signature_path = os.path.join(os.getcwd(), authentication)
                    # Check if it's a relative path from backend directory
                    elif os.path.exists(os.path.join(os.getcwd(), 'backend', authentication)):
                        signature_path = os.path.join(os.getcwd(), 'backend', authentication)
                    # Check if it's a URL that needs to be downloaded
                    elif authentication.startswith('http') or "/api/users/signature/" in authentication:
                        # Handle URL-based signatures
                        if authentication.startswith('http'):
                            signature_url = authentication
                        else:
                            signature_url = f"http://localhost:5000{authentication}"
                        
                        import requests
                        response = requests.get(signature_url, timeout=10)
                        if response.status_code == 200:
                            img_data = io.BytesIO(response.content)
                            img = ImageReader(img_data)
                            print(f"Successfully loaded signature from URL: {signature_url}")
                        else:
                            print(f"Failed to load signature from URL: {signature_url}")
                            img = None
                    else:
                        print(f"Signature path not found: {authentication}")
                        img = None
                    
                    # If we found a local file path, load the image
                    if signature_path and not authentication.startswith('http'):
                        img = ImageReader(signature_path)
                        print(f"Successfully loaded signature from file: {signature_path}")
                    
                    # Display the signature image
                    if img:
                        # Resize image to fit in PDF (good size for signature)
                        img_width, img_height = img.getSize()
                        max_width = 2.5 * inch  # Good size for signature visibility
                        max_height = 1.0 * inch
                        
                        # Calculate scaling to maintain aspect ratio
                        scale_x = max_width / img_width
                        scale_y = max_height / img_height
                        scale = min(scale_x, scale_y)
                        
                        scaled_width = img_width * scale
                        scaled_height = img_height * scale
                        
                        # Add signature label
                        story.append(Spacer(1, 10))
                        story.append(Paragraph("Signature:", ParagraphStyle('SignatureLabel', parent=styles['Normal'], fontSize=9, fontName='Helvetica-Bold')))
                        
                        # Add signature image
                        story.append(Spacer(1, 5))
                        from reportlab.platypus import Image
                        signature_img = Image(img, scaled_width, scaled_height)
                        story.append(signature_img)
                        
                        print(f"Signature image added to PDF - Size: {scaled_width:.2f}x{scaled_height:.2f} inches")
                    else:
                        print(f"Could not load signature image from: {authentication}")
                        
                except Exception as e:
                    # If image loading fails, just continue without the image
                    print(f"Error loading signature image: {str(e)}")
                    pass
            
            story.append(Spacer(1, 15))
        
        # References section
        if references:
            story.append(Paragraph("REFERENCES", section_style))
            ref_data = [['Reference Document', 'Reference Number', 'Version', 'Revision']]
            for ref in references:
                ref_data.append([
                    ref[0] or 'N/A', 
                    ref[1] or 'N/A', 
                    str(ref[2]) if ref[2] is not None else 'N/A',
                    str(ref[3]) if ref[3] is not None else 'N/A'
                ])
            
            ref_table = Table(ref_data, colWidths=[1.5*inch, 2.5*inch, 0.8*inch, 0.8*inch])
            ref_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 7),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 4),
                ('BACKGROUND', (0, 1), (-1, -1), colors.white),
                ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
                ('FONTSIZE', (0, 1), (-1, -1), 7),
                ('LEFTPADDING', (0, 0), (-1, -1), 3),
                ('RIGHTPADDING', (0, 0), (-1, -1), 3),
                ('TOPPADDING', (0, 0), (-1, -1), 3),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
            ]))
            
            story.append(ref_table)
            story.append(Spacer(1, 10))
        
        # Footer
        story.append(Paragraph(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", 
                              ParagraphStyle('Footer', parent=styles['Normal'], fontSize=6, alignment=2, textColor=colors.grey)))
        
        # Build PDF
        doc.build(story)
        
        # Prepare response
        buffer.seek(0)
        
        return send_file(
            buffer,
            as_attachment=True,
            download_name=f'memo_{memo_id}_{datetime.now().strftime("%Y%m%d_%H%M%S")}.pdf',
            mimetype='application/pdf'
        )
        
    except Exception as e:
        print(f"Error generating memo PDF: {str(e)}")
        return jsonify({"success": False, "message": f"Error generating PDF: {str(e)}"}), 500
