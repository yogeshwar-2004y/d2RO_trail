"""
Memo management routes
"""
from datetime import datetime
from flask import Blueprint, request, jsonify
from config import get_db_connection
from utils.helpers import handle_database_error

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
        unit_identification = []
        if form_data.get('unitIdentification'):
            unit_identification.append(form_data.get('unitIdentification'))
        
        # Convert to empty array if empty for PostgreSQL
        unit_identification = unit_identification if unit_identification else []

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

        conn.commit()
        cur.close()

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
        conn = get_db_connection()
        cur = conn.cursor()

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

        # Convert memo to dictionary
        # Database column order: memo_id, from_person, to_person, thru_person, casdic_ref_no, dated, wing_proj_ref_no, lru_sru_desc, part_number, slno_units, qty_offered, manufacturer, drawing_no_rev, source, unit_identification, mechanical_inspn, inspn_test_stage_offered, stte_status, test_stage_cleared, venue, memo_date, name_designation, test_facility, test_cycle_duration, test_start_on, test_complete_on, calibration_status, func_check_initial, perf_check_during, func_check_end, certified, remarks, memo_status, submitted_by_name, accepted_by_name
        memo_dict = {
            "memo_id": memo[0],
            "from_person": memo[1],
            "to_person": memo[2],
            "thru_person": memo[3],
            "casdic_ref_no": memo[4],
            "dated": safe_isoformat(memo[5]),
            "wing_proj_ref_no": memo[6],
            "lru_sru_desc": memo[7],
            "part_number": memo[8],
            "slno_units": memo[9],
            "qty_offered": memo[10],
            "manufacturer": memo[11],
            "drawing_no_rev": memo[12],
            "source": memo[13],
            "unit_identification": memo[14],
            "mechanical_inspn": memo[15],
            "inspn_test_stage_offered": memo[16],
            "stte_status": memo[17],
            "test_stage_cleared": memo[18],
            "venue": memo[19],
            "memo_date": safe_isoformat(memo[20]),
            "name_designation": memo[21],
            "test_facility": memo[22],
            "test_cycle_duration": memo[23],
            "test_start_on": safe_isoformat(memo[24]),
            "test_complete_on": safe_isoformat(memo[25]),
            "calibration_status": memo[26],
            "func_check_initial": safe_isoformat(memo[27]),
            "perf_check_during": safe_isoformat(memo[28]),
            "func_check_end": safe_isoformat(memo[29]),
            "certified": memo[30],
            "remarks": memo[31],
            "submitted_at": None,  # Not available in current schema
            "submitted_by": None,  # Not available in current schema
            "accepted_at": None,   # Not available in current schema
            "accepted_by": None,   # Not available in current schema
            "coordinator": memo[32],
            "memo_status": memo[33],
            "submitted_by_name": memo[34],
            "accepted_by_name": memo[35]
        }

        # Convert references to list
        reference_list = []
        for ref in references:
            reference_list.append({
                "ref_id": ref[0],
                "ref_doc": ref[1],
                "ref_no": ref[2],
                "ver": ref[3],
                "rev": ref[4]
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

        # Check if memo exists
        print(f"Checking if memo {memo_id} exists...")
        cur.execute("SELECT memo_id FROM memos WHERE memo_id = %s", (memo_id,))
        if not cur.fetchone():
            cur.close()
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
        elif status == 'rejected':
            print(f"Updating memo {memo_id} with rejected status...")
            cur.execute("""
                UPDATE memos 
                SET memo_status = 'rejected'
                WHERE memo_id = %s
            """, (memo_id,))
            
            # Remove any existing report for rejected memo
            cur.execute("DELETE FROM reports WHERE memo_id = %s", (memo_id,))
            if cur.rowcount > 0:
                print(f"Removed existing report for rejected memo {memo_id}")
        
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
        conn.commit()
        
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
                    # For now, we'll use default values for project_id, lru_id, and serial_id
                    # In a real implementation, these would be derived from the memo data
                    # or provided by the user during memo submission
                    default_project_id = 1  # Default project
                    default_lru_id = 1       # Default LRU
                    default_serial_id = 1   # Default serial
                    
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
                        print(f"Report created successfully for memo {memo_id}")
                    else:
                        print(f"Report already exists for memo {memo_id}")
                
                conn.commit()
            except Exception as report_error:
                print(f"Error creating report for memo {memo_id}: {str(report_error)}")
                # Don't fail the entire operation if report creation fails
                conn.rollback()
                conn.commit()  # Re-commit the memo approval
        
        cur.close()

        return jsonify({
            "success": True,
            "message": f"Memo {status} successfully"
        })

    except Exception as e:
        print(f"Error in approve_memo: {str(e)}")
        import traceback
        traceback.print_exc()
        if conn:
            conn.rollback()
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
                SELECT user_id, name, email
                FROM users 
                WHERE user_id = %s
            """, (reviewer_id,))
            
            reviewer = cur.fetchone()
        
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
                "email": reviewer[2]
            } if reviewer else None
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
        
        # Update memo status and reviewer comments
        reviewer_comments = data.get('reviewer_comments', '')
        cur.execute("""
            UPDATE memos 
            SET memo_status = %s, qa_remarks = %s
            WHERE memo_id = %s
        """, (memo_status, reviewer_comments, memo_id))
        
        if cur.rowcount == 0:
            cur.close()
            return jsonify({"success": False, "message": "Memo not found"}), 404
        
        conn.commit()
        cur.close()
        
        return jsonify({
            "success": True,
            "message": f"Memo status updated to {test_status}",
            "memo_status": memo_status
        })
        
    except Exception as e:
        return handle_database_error(get_db_connection(), f"Error updating memo status: {str(e)}")
