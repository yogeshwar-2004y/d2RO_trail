# COT Screening Inspection Report Routes

import os
import uuid
from flask import Blueprint, request, jsonify, send_file
from config import get_db_connection, Config
from utils.helpers import handle_database_error
from utils.helpers import handle_database_error, allowed_file, validate_file_size

cots_screening_bp = Blueprint('cots_screening', __name__)

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

@cots_screening_bp.route('/api/reports/cot-screening', methods=['POST'])
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
        
        print("Table exists, proceeding with insert/update...")
        
        # Check if report_card_id column exists, add if missing
        report_card_id = data.get('report_card_id')
        cur.execute("""
            SELECT column_name 
            FROM information_schema.columns 
            WHERE table_name = 'cot_screening_inspection_report' 
            AND column_name = 'report_card_id'
        """)
        has_report_card_id = cur.fetchone() is not None
        
        if not has_report_card_id and report_card_id:
            try:
                cur.execute("ALTER TABLE cot_screening_inspection_report ADD COLUMN report_card_id INTEGER")
                conn.commit()
                has_report_card_id = True
                print("Added report_card_id column to cot_screening_inspection_report table")
            except Exception as e:
                print(f"Note: Could not add report_card_id column (may already exist): {str(e)}")
                conn.rollback()
        
        # Check if report already exists for this report_card_id
        existing_report_id = None
        if report_card_id and has_report_card_id:
            cur.execute("""
                SELECT report_id FROM cot_screening_inspection_report 
                WHERE report_card_id = %s
            """, (report_card_id,))
            existing = cur.fetchone()
            if existing:
                existing_report_id = existing[0]
        
        if existing_report_id:
            # Update existing report
            print(f"Updating existing report with ID: {existing_report_id}")
            if has_report_card_id:
                cur.execute("""
                    UPDATE cot_screening_inspection_report SET
                        project_name = %s, report_ref_no = %s, memo_ref_no = %s, lru_name = %s, 
                        sru_name = %s, dp_name = %s, part_no = %s, inspection_stage = %s, 
                        test_venue = %s, quantity = %s, sl_nos = %s, serial_number = %s,
                        start_date = %s, end_date = %s, dated1 = %s, dated2 = %s,
                        test_nature1 = %s, test_nature2 = %s, test_nature3 = %s,
                        rem1 = %s, upload1 = %s, rem2 = %s, upload2 = %s, rem3 = %s, upload3 = %s,
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
                    data.get('start_date') or None,
                    data.get('end_date') or None,
                    data.get('dated1') or None,
                    data.get('dated2') or None,
                    data.get('test_nature1') or None,
                    data.get('test_nature2') or None,
                    data.get('test_nature3') or None,
                    data.get('rem1') or None,
                    data.get('upload1') or None,
                    data.get('rem2') or None,
                    data.get('upload2') or None,
                    data.get('rem3') or None,
                    data.get('upload3') or None,
                    data.get('prepared_by') or None,
                    data.get('verified_by') or None,
                    data.get('approved_by') or None,
                    existing_report_id
                ))
            else:
                cur.execute("""
                    UPDATE cot_screening_inspection_report SET
                        project_name = %s, report_ref_no = %s, memo_ref_no = %s, lru_name = %s, 
                        sru_name = %s, dp_name = %s, part_no = %s, inspection_stage = %s, 
                        test_venue = %s, quantity = %s, sl_nos = %s, serial_number = %s,
                        start_date = %s, end_date = %s, dated1 = %s, dated2 = %s,
                        test_nature1 = %s, test_nature2 = %s, test_nature3 = %s,
                        rem1 = %s, upload1 = %s, rem2 = %s, upload2 = %s, rem3 = %s, upload3 = %s,
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
                    data.get('start_date') or None,
                    data.get('end_date') or None,
                    data.get('dated1') or None,
                    data.get('dated2') or None,
                    data.get('test_nature1') or None,
                    data.get('test_nature2') or None,
                    data.get('test_nature3') or None,
                    data.get('rem1') or None,
                    data.get('upload1') or None,
                    data.get('rem2') or None,
                    data.get('upload2') or None,
                    data.get('rem3') or None,
                    data.get('upload3') or None,
                    data.get('prepared_by') or None,
                    data.get('verified_by') or None,
                    data.get('approved_by') or None,
                    existing_report_id
                ))
            report_id = existing_report_id
            print(f"Update query executed successfully for report ID: {report_id}")
        else:
            # Insert new report
            if has_report_card_id:
                cur.execute("""
                    INSERT INTO cot_screening_inspection_report (
                        report_card_id,
                        project_name, report_ref_no, memo_ref_no, lru_name, sru_name, dp_name,
                        part_no, inspection_stage, test_venue, quantity, sl_nos, serial_number,
                        start_date, end_date, dated1, dated2,
                        test_nature1, test_nature2, test_nature3,
                        rem1, upload1, rem2, upload2, rem3, upload3,
                        prepared_by, verified_by, approved_by
                    ) VALUES (
                        %s,
                        %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
                        %s, %s, %s,
                        %s, %s, %s, %s, %s, %s,
                        %s, %s, %s
                    ) RETURNING report_id
                """, (
                    report_card_id,
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
                    data.get('test_nature1') or None,
                    data.get('test_nature2') or None,
                    data.get('test_nature3') or None,
                    data.get('rem1') or None,
                    data.get('upload1') or None,
                    data.get('rem2') or None,
                    data.get('upload2') or None,
                    data.get('rem3') or None,
                    data.get('upload3') or None,
                    data.get('prepared_by') or None,
                    data.get('verified_by') or None,
                    data.get('approved_by') or None
                ))
            else:
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
                    data.get('test_nature1') or None,
                    data.get('test_nature2') or None,
                    data.get('test_nature3') or None,
                    data.get('rem1') or None,
                    data.get('upload1') or None,
                    data.get('rem2') or None,
                    data.get('upload2') or None,
                    data.get('rem3') or None,
                    data.get('upload3') or None,
                    data.get('prepared_by') or None,
                    data.get('verified_by') or None,
                    data.get('approved_by') or None
                ))
            report_id = cur.fetchone()[0]
            print(f"Insert query executed successfully")
            print(f"Report created with ID: {report_id}")
        
        conn.commit()
        
        # Send notifications if all signatures are complete
        if data.get('prepared_by') and data.get('verified_by') and data.get('approved_by'):
            try:
                from utils.activity_logger import log_notification
                from utils.helpers import get_users_by_role
                
                if report_card_id:
                    cur.execute("""
                        SELECT project_id, submitted_by 
                        FROM reports 
                        WHERE report_id = %s
                    """, (report_card_id,))
                    report_info = cur.fetchone()
                    
                    if report_info and len(report_info) >= 2:
                        project_id = report_info[0]
                        performed_by = report_info[1] or 1002
                        
                        # Send notifications to Design Heads (role_id=4) and QA Heads (role_id=2)
                        for role_id in [4, 2]:
                            try:
                                users = get_users_by_role(role_id)
                                for user in users:
                                    user_id = user.get('user_id') if isinstance(user, dict) else (user[0] if hasattr(user, '__getitem__') else None)
                                    if user_id:
                                        log_notification(
                                            project_id=project_id,
                                            activity_performed="COTS Screening Report Completed",
                                            performed_by=performed_by,
                                            notified_user_id=user_id,
                                            notification_type="report_completed",
                                            additional_info=f"COTS Screening Report (ID: {report_id}) for Report Card {report_card_id} has been completed with all signatures."
                                        )
                            except Exception as e:
                                print(f"Error sending notification to role {role_id}: {str(e)}")
                                pass
            except Exception as e:
                print(f"Error in notification logic: {str(e)}")
                pass
        
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

@cots_screening_bp.route('/api/reports/cot-screening/<int:report_id>', methods=['GET'])
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

@cots_screening_bp.route('/api/reports/cot-screening/by-report-card/<int:report_card_id>', methods=['GET'])
def get_cot_screening_report_by_report_card(report_card_id):
    """Get COT screening inspection report by report card ID"""
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        
        # Check if report_card_id column exists
        cur.execute("""
            SELECT column_name 
            FROM information_schema.columns 
            WHERE table_name = 'cot_screening_inspection_report' 
            AND column_name = 'report_card_id'
        """)
        has_report_card_id = cur.fetchone() is not None
        
        if not has_report_card_id:
            cur.close()
            conn.close()
            return jsonify({"success": False, "message": "Report not found"}), 404
        
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
            WHERE report_card_id = %s
        """, (report_card_id,))
        
        report = cur.fetchone()
        cur.close()
        conn.close()
        
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
        
        return jsonify({
            "success": True,
            "report": report_data
        })
        
    except Exception as e:
        print(f"Error fetching COT screening report: {str(e)}")
        return handle_database_error(get_db_connection(), f"Error fetching COT screening report: {str(e)}")

@cots_screening_bp.route('/api/reports/cot-screening/<int:report_id>', methods=['PUT'])
# @require_design_head_role
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

@cots_screening_bp.route('/api/reports/cot-screening', methods=['GET'])
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

@cots_screening_bp.route('/api/reports/cot-screening/count', methods=['GET'])
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

@cots_screening_bp.route('/api/reports/cot-screening/<int:report_id>/upload', methods=['POST'])
# @require_design_head_role
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

@cots_screening_bp.route('/api/reports/cot-screening/files/<path:filename>', methods=['GET'])
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
