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
        
        # Prepare serial numbers array from checkboxes
        slno_units = []
        if form_data.get('slNo1'): slno_units.append('1')
        if form_data.get('slNo2'): slno_units.append('2')
        if form_data.get('slNo3'): slno_units.append('3')
        if form_data.get('slNo4'): slno_units.append('4')
        if form_data.get('slNo5'): slno_units.append('5')
        if form_data.get('slNo6'): slno_units.append('6')
        if form_data.get('slNo7'): slno_units.append('7')
        if form_data.get('slNo8'): slno_units.append('8')
        if form_data.get('slNo9'): slno_units.append('9')
        if form_data.get('slNo10'): slno_units.append('10')
        
        # Convert to empty array if empty for PostgreSQL
        slno_units = slno_units if slno_units else []

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
            print(f"unit_identification: {unit_identification}")
            print(f"certified: {certified}")
            
            cur.execute("""
                INSERT INTO memos (
                    from_person, to_person, thru_person, casdic_ref_no, dated,
                    wing_proj_ref_no, lru_sru_desc, part_number, slno_units, qty_offered,
                    manufacturer, drawing_no_rev, source, unit_identification, mechanical_inspn,
                    inspn_test_stage_offered, stte_status, test_stage_cleared, venue,
                    memo_date, name_designation, test_facility, test_cycle_duration,
                    test_start_on, test_complete_on, calibration_status, func_check_initial,
                    perf_check_during, func_check_end, certified, remarks,
                    submitted_at, submitted_by
                ) VALUES (
                    %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
                    %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
                    %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
                    %s, %s, %s
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
                data.get('submitted_by')
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
    """Get all memos with pagination"""
    try:
        page = request.args.get('page', 1, type=int)
        limit = request.args.get('limit', 10, type=int)
        offset = (page - 1) * limit

        conn = get_db_connection()
        cur = conn.cursor()

        # Get total count
        cur.execute("SELECT COUNT(*) FROM memos")
        total_count = cur.fetchone()[0]

        # Get memos with user information
        cur.execute("""
            SELECT 
                m.memo_id, m.from_person, m.to_person, m.thru_person,
                m.casdic_ref_no, m.dated, m.wing_proj_ref_no, m.lru_sru_desc,
                m.part_number, m.manufacturer, m.qty_offered, m.venue,
                m.memo_date, m.submitted_at, m.accepted_at,
                u1.name as submitted_by_name,
                u2.name as accepted_by_name
            FROM memos m
            LEFT JOIN users u1 ON m.submitted_by = u1.user_id
            LEFT JOIN users u2 ON m.accepted_by = u2.user_id
            ORDER BY m.submitted_at DESC
            LIMIT %s OFFSET %s
        """, (limit, offset))

        memos = cur.fetchall()
        cur.close()

        memo_list = []
        for memo in memos:
            memo_list.append({
                "memo_id": memo[0],
                "from_person": memo[1],
                "to_person": memo[2],
                "thru_person": memo[3],
                "casdic_ref_no": memo[4],
                "dated": memo[5].isoformat() if memo[5] else None,
                "wing_proj_ref_no": memo[6],
                "lru_sru_desc": memo[7],
                "part_number": memo[8],
                "manufacturer": memo[9],
                "qty_offered": memo[10],
                "venue": memo[11],
                "memo_date": memo[12].isoformat() if memo[12] else None,
                "submitted_at": memo[13].isoformat() if memo[13] else None,
                "accepted_at": memo[14].isoformat() if memo[14] else None,
                "submitted_by_name": memo[15],
                "accepted_by_name": memo[16]
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
            LEFT JOIN users u1 ON m.submitted_by = u1.user_id
            LEFT JOIN users u2 ON m.accepted_by = u2.user_id
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

        # Convert memo to dictionary
        memo_dict = {
            "memo_id": memo[0],
            "from_person": memo[1],
            "to_person": memo[2],
            "thru_person": memo[3],
            "casdic_ref_no": memo[4],
            "dated": memo[5].isoformat() if memo[5] else None,
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
            "memo_date": memo[20].isoformat() if memo[20] else None,
            "name_designation": memo[21],
            "test_facility": memo[22],
            "test_cycle_duration": memo[23],
            "test_start_on": memo[24].isoformat() if memo[24] else None,
            "test_complete_on": memo[25].isoformat() if memo[25] else None,
            "calibration_status": memo[26],
            "func_check_initial": memo[27].isoformat() if memo[27] else None,
            "perf_check_during": memo[28].isoformat() if memo[28] else None,
            "func_check_end": memo[29].isoformat() if memo[29] else None,
            "certified": memo[30],
            "remarks": memo[31],
            "submitted_at": memo[32].isoformat() if memo[32] else None,
            "submitted_by": memo[33],
            "accepted_at": memo[34].isoformat() if memo[34] else None,
            "accepted_by": memo[35],
            "submitted_by_name": memo[36],
            "accepted_by_name": memo[37]
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
    """Approve or reject a memo"""
    try:
        data = request.json
        if not data:
            return jsonify({"success": False, "message": "No data provided"}), 400

        # Validate required fields
        required_fields = ['status', 'user_id']
        for field in required_fields:
            if field not in data:
                return jsonify({"success": False, "message": f"Missing required field: {field}"}), 400

        status = data.get('status')
        if status not in ['accepted', 'rejected']:
            return jsonify({"success": False, "message": "Status must be 'accepted' or 'rejected'"}), 400

        conn = get_db_connection()
        cur = conn.cursor()

        # Check if memo exists
        cur.execute("SELECT memo_id FROM memos WHERE memo_id = %s", (memo_id,))
        if not cur.fetchone():
            cur.close()
            return jsonify({"success": False, "message": "Memo not found"}), 404

        # Update memo approval status
        if status == 'accepted':
            cur.execute("""
                UPDATE memos 
                SET accepted_at = %s, accepted_by = %s
                WHERE memo_id = %s
            """, (datetime.now(), data.get('user_id'), memo_id))
        
        # Insert or update memo_approval record
        cur.execute("""
            INSERT INTO memo_approval (memo_id, test_date, user_id, comments, authentication, attachment_path, status)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (memo_id) DO UPDATE SET
                test_date = EXCLUDED.test_date,
                user_id = EXCLUDED.user_id,
                comments = EXCLUDED.comments,
                authentication = EXCLUDED.authentication,
                attachment_path = EXCLUDED.attachment_path,
                status = EXCLUDED.status
        """, (
            memo_id,
            datetime.strptime(data.get('test_date'), '%Y-%m-%d').date() if data.get('test_date') else None,
            data.get('user_id'),
            data.get('comments'),
            data.get('authentication'),
            data.get('attachment_path'),
            status
        ))

        conn.commit()
        cur.close()

        return jsonify({
            "success": True,
            "message": f"Memo {status} successfully"
        })

    except Exception as e:
        if 'conn' in locals():
            conn.rollback()
        return handle_database_error(get_db_connection(), f"Error approving memo: {str(e)}")
