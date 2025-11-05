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
        
        # Check if dated1 and dated2 columns exist, if not add them
        cur.execute("""
            SELECT column_name 
            FROM information_schema.columns 
            WHERE table_name='kit_of_parts_inspection_report' 
            AND column_name IN ('dated1', 'dated2')
        """)
        existing_columns = [row[0] for row in cur.fetchall()]
        
        if 'dated1' not in existing_columns:
            print("  Adding dated1 column to kit_of_parts_inspection_report table...")
            cur.execute("""
                ALTER TABLE kit_of_parts_inspection_report 
                ADD COLUMN dated1 DATE
            """)
            conn.commit()
            print("  ✓ Added dated1 column")
        
        if 'dated2' not in existing_columns:
            print("  Adding dated2 column to kit_of_parts_inspection_report table...")
            cur.execute("""
                ALTER TABLE kit_of_parts_inspection_report 
                ADD COLUMN dated2 DATE
            """)
            conn.commit()
            print("  ✓ Added dated2 column")
        
        # Also check for inspection_stage column
        cur.execute("""
            SELECT column_name 
            FROM information_schema.columns 
            WHERE table_name='kit_of_parts_inspection_report' 
            AND column_name='inspection_stage'
        """)
        if not cur.fetchone():
            print("  Adding inspection_stage column to kit_of_parts_inspection_report table...")
            cur.execute("""
                ALTER TABLE kit_of_parts_inspection_report 
                ADD COLUMN inspection_stage TEXT
            """)
            conn.commit()
            print("  ✓ Added inspection_stage column")
        
        # Check if report_card_id column exists, if not add it (preferred field name)
        cur.execute("""
            SELECT column_name 
            FROM information_schema.columns 
            WHERE table_name='kit_of_parts_inspection_report' 
            AND column_name='report_card_id'
        """)
        if not cur.fetchone():
            print("  Adding report_card_id column to kit_of_parts_inspection_report table...")
            cur.execute("""
                ALTER TABLE kit_of_parts_inspection_report 
                ADD COLUMN report_card_id INT REFERENCES reports(report_id) ON DELETE CASCADE
            """)
            conn.commit()
            print("  ✓ Added report_card_id column")
        
        # Get report_card_id from data (the report_id from reports table)
        report_card_id = data.get('report_card_id') or data.get('original_report_id') or data.get('report_id')

        # Get inspection items from the request (support both formats)
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
            # Try to get data from inspectionItems array first (if it exists and has data)
            item = None
            if inspection_items and len(inspection_items) > 0:
                item = next((item for item in inspection_items if item.get('slNo') == i), None)
            
            # If not in array format, try individual fields (camelCase format from frontend)
            observations_key = f'test{i}Observations'
            remarks_key = f'test{i}Remarks'
            upload_key = f'test{i}Upload'
            
            if item:
                # Get data from array format
                expected_value = item.get('expected')
                if not expected_value:
                    expected_value = default_expected[i]
                
                observations = item.get('observations', '')
                remarks = item.get('remarks', '')
                upload = item.get('upload', '') or item.get('fileName', '')
            else:
                # Get data from individual camelCase fields (frontend sends this format)
                observations = data.get(observations_key, '')
                remarks = data.get(remarks_key, '')
                upload = data.get(upload_key, '')
                
                # Get expected value from request or use default
                expected_value = data.get(f'test{i}Expected')
                if not expected_value:
                    expected_value = default_expected[i]
            
            # Convert remarks format (Passed -> OK, Failed -> NOT OK)
            if remarks:
                if remarks == 'Passed':
                    remarks = 'OK'
                elif remarks == 'Failed':
                    remarks = 'NOT OK'
            
            # Ensure we have non-None values
            observations = observations or ''
            remarks = remarks or ''
            upload = upload or ''
            
            test_values.update({
                f'test{i}_expected': expected_value,
                f'test{i}_observations': observations,
                f'test{i}_remarks': remarks,
                f'test{i}_upload': upload
            })
            
            # Debug logging
            print(f"  Test {i}: expected={expected_value}, observations='{observations}', remarks='{remarks}', upload='{upload}'")

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
                prepared_by_qa_g1, verified_by_g1h_qa_g, approved_by,
                report_card_id
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
                %(prepared_by_qa_g1)s, %(verified_by_g1h_qa_g)s, %(approved_by)s,
                %(report_card_id)s
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
            'report_card_id': report_card_id,
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
    """Get a specific kit of parts inspection report
    report_id can be either the original_report_id (from reports table) or the inspection report's own report_id
    """
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        
        # First try to find by report_card_id (from reports table) - preferred method
        cur.execute("""
            SELECT * FROM kit_of_parts_inspection_report 
            WHERE report_card_id = %s
        """, (report_id,))
        
        report = cur.fetchone()
        
        # If not found, try by original_report_id (backward compatibility)
        if not report:
            cur.execute("""
                SELECT * FROM kit_of_parts_inspection_report 
                WHERE original_report_id = %s
            """, (report_id,))
            report = cur.fetchone()
        
        # If still not found, try by the inspection report's own report_id
        if not report:
            cur.execute("SELECT * FROM kit_of_parts_inspection_report WHERE report_id = %s", (report_id,))
            report = cur.fetchone()
        
        if not report:
            cur.close()
            return jsonify({"success": False, "message": "Report not found"}), 404
        
        columns = [desc[0] for desc in cur.description] if cur.description else []
        
        cur.close()
        
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
        
        # First try to find by report_card_id (from reports table) - preferred method
        cur.execute("""
            SELECT report_id FROM kit_of_parts_inspection_report 
            WHERE report_card_id = %s
        """, (report_id,))
        
        result = cur.fetchone()
        actual_report_id = result[0] if result else report_id
        
        # If not found, try by original_report_id (backward compatibility)
        if not result:
            cur.execute("""
                SELECT report_id FROM kit_of_parts_inspection_report 
                WHERE report_id = %s
            """, (report_id,))
            result = cur.fetchone()
            actual_report_id = result[0] if result else report_id
        
        # If still not found, use the report_id directly
        if not result:
            cur.execute("SELECT report_id FROM kit_of_parts_inspection_report WHERE report_id = %s", (report_id,))
            if not cur.fetchone():
                cur.close()
                return jsonify({"success": False, "message": "Report not found"}), 404
            actual_report_id = report_id
        
        # Build dynamic update query
        update_fields = []
        update_values = []
        
        # Map frontend field names to database column names
        field_mapping = {
            'verified_by_g1h_qa_g': 'verified_by_g1h_qa_g',
            'approved_by': 'approved_by',
            'prepared_by_qa_g1': 'prepared_by_qa_g1'
        }
        
        for key, value in data.items():
            if key != 'report_id':  # Don't update the ID
                # Use mapped field name if exists, otherwise use key as-is
                db_field = field_mapping.get(key, key)
                update_fields.append(f"{db_field} = %s")
                update_values.append(value)
        
        if not update_fields:
            cur.close()
            return jsonify({"success": False, "message": "No fields to update"}), 400
        
        update_values.append(actual_report_id)
        
        cur.execute(f"""
            UPDATE kit_of_parts_inspection_report 
            SET {', '.join(update_fields)}
            WHERE report_id = %s
        """, update_values)
        
        if cur.rowcount == 0:
            cur.close()
            return jsonify({"success": False, "message": "Report not found or no changes made"}), 404
        
        conn.commit()
        cur.close()
        
        return jsonify({
            "success": True,
            "message": "Kit of parts inspection report updated successfully"
        })
        
    except Exception as e:
        print(f"Error updating kit of parts inspection report: {str(e)}")
        return handle_database_error(get_db_connection(), f"Error updating kit of parts inspection report: {str(e)}")

@kit_of_parts_bp.route('/api/kit-of-parts/notify', methods=['POST'])
def notify_qa_heads_kit_of_parts():
    """Notify QA Heads when a kit of parts inspection report is submitted"""
    try:
        data = request.json
        if not data:
            return jsonify({"success": False, "message": "No data provided"}), 400
        
        report_id = data.get('report_id')
        memo_ref_no = data.get('memo_ref_no')
        reviewer_id = data.get('reviewer_id')
        
        if not report_id or not reviewer_id:
            return jsonify({"success": False, "message": "Report ID and Reviewer ID are required"}), 400
        
        from utils.activity_logger import log_notification, get_users_by_role
        
        # Get all QA Heads (role_id = 2)
        qa_heads = get_users_by_role(2)
        
        # Get reviewer name and report details
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT name FROM users WHERE user_id = %s", (reviewer_id,))
        reviewer_result = cur.fetchone()
        reviewer_name = reviewer_result[0] if reviewer_result else "Reviewer"
        
        # Get report details for activity log
        cur.execute("""
            SELECT report_ref_no, project_name, lru_name 
            FROM kit_of_parts_inspection_report 
            WHERE report_id = %s
        """, (report_id,))
        report_result = cur.fetchone()
        report_ref_no = report_result[0] if report_result else f"Report {report_id}"
        project_name = report_result[1] if report_result else "Unknown"
        lru_name = report_result[2] if report_result else "Unknown"
        cur.close()
        
        # Log activity to activity logs
        from utils.activity_logger import log_activity
        memo_text = f" corresponding to memo {memo_ref_no}" if memo_ref_no else ""
        activity_message = f"Kit of Parts Inspection Report (ID: {report_id}, Ref: {report_ref_no}){memo_text} has been submitted by {reviewer_name} for project '{project_name}', LRU '{lru_name}'."
        
        log_activity(
            project_id=None,  # Report operations don't have project_id in this context
            activity_performed="Kit of Parts Inspection Report Submitted",
            performed_by=reviewer_id,
            additional_info=f"Report ID: {report_id}|Report Ref: {report_ref_no}|Project: {project_name}|LRU: {lru_name}|Submitted by: {reviewer_name}{memo_text}"
        )
        
        print(f"✓ Activity logged: Kit of Parts Inspection Report {report_id} submitted by {reviewer_name}")
        
        # Notify each QA Head
        for qa_head in qa_heads:
            memo_text = f" corresponding to memo {memo_ref_no}" if memo_ref_no else ""
            log_notification(
                project_id=None,
                activity_performed=f"Kit of Parts Inspection Report{memo_text} Submitted",
                performed_by=reviewer_id,
                notified_user_id=qa_head['user_id'],
                notification_type="report_submitted",
                additional_info=f"Report ID {report_id} (Ref: {report_ref_no}){memo_text} has been submitted by {reviewer_name} for project '{project_name}', LRU '{lru_name}'. Please review."
            )
        
        print(f"✓ Notifications sent to {len(qa_heads)} QA Head(s)")
        
        return jsonify({
            "success": True,
            "message": f"Activity logged and notifications sent to {len(qa_heads)} QA Head(s)"
        })
        
    except Exception as e:
        print(f"Error notifying QA Heads for kit of parts report: {str(e)}")
        return handle_database_error(get_db_connection(), f"Error notifying QA Heads: {str(e)}")

@kit_of_parts_bp.route('/api/kit-of-parts/notify-approval', methods=['POST'])
def notify_qa_heads_approval_kit_of_parts():
    """Notify QA Heads when a kit of parts inspection report is approved"""
    try:
        data = request.json
        if not data:
            return jsonify({"success": False, "message": "No data provided"}), 400
        
        report_id = data.get('report_id')
        approved_by_id = data.get('approved_by_id')
        
        if not report_id or not approved_by_id:
            return jsonify({"success": False, "message": "Report ID and Approved By ID are required"}), 400
        
        from utils.activity_logger import log_notification, get_users_by_role
        
        # Get all QA Heads (role_id = 2)
        qa_heads = get_users_by_role(2)
        print(f"DEBUG: Found {len(qa_heads)} QA Head(s)")
        
        if not qa_heads or len(qa_heads) == 0:
            print(f"WARNING: No QA Heads found with role_id = 2")
            # Still log the activity even if no QA Heads found
        else:
            for qa_head in qa_heads:
                print(f"DEBUG: QA Head found - ID: {qa_head['user_id']}, Name: {qa_head['name']}, Email: {qa_head['email']}")
        
        # Get approver name and report details
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT name FROM users WHERE user_id = %s", (approved_by_id,))
        approver_result = cur.fetchone()
        approver_name = approver_result[0] if approver_result else "Approver"
        
        # Get report details for activity log
        cur.execute("""
            SELECT report_ref_no, project_name, lru_name, memo_ref_no 
            FROM kit_of_parts_inspection_report 
            WHERE report_id = %s
        """, (report_id,))
        report_result = cur.fetchone()
        report_ref_no = report_result[0] if report_result else f"Report {report_id}"
        project_name = report_result[1] if report_result else "Unknown"
        lru_name = report_result[2] if report_result else "Unknown"
        memo_ref_no = report_result[3] if report_result else None
        cur.close()
        
        print(f"DEBUG: Report details - Ref: {report_ref_no}, Project: {project_name}, LRU: {lru_name}")
        
        # Log activity to activity logs
        from utils.activity_logger import log_activity
        activity_message = f"Kit of Parts Inspection Report (ID: {report_id}, Ref: {report_ref_no}) has been approved by {approver_name} for project '{project_name}', LRU '{lru_name}'."
        
        activity_logged = log_activity(
            project_id=None,  # Report operations don't have project_id in this context
            activity_performed="Kit of Parts Inspection Report Approved",
            performed_by=approved_by_id,
            additional_info=f"Report ID: {report_id}|Report Ref: {report_ref_no}|Project: {project_name}|LRU: {lru_name}|Approved by: {approver_name}"
        )
        
        if activity_logged:
            print(f"✓ Activity logged: Kit of Parts Inspection Report {report_id} approved by {approver_name}")
        else:
            print(f"✗ Failed to log activity for report {report_id}")
        
        # Notify each QA Head
        notification_count = 0
        notification_errors = []
        
        if qa_heads and len(qa_heads) > 0:
            for qa_head in qa_heads:
                notification_message = f"Report num : {report_ref_no} has been approved"
                print(f"DEBUG: Attempting to notify QA Head {qa_head['user_id']} ({qa_head['name']})")
                
                notification_sent = log_notification(
                    project_id=None,
                    activity_performed=notification_message,
                    performed_by=approved_by_id,
                    notified_user_id=qa_head['user_id'],
                    notification_type="report_approved",
                    additional_info=f"Report ID {report_id} (Ref: {report_ref_no}) has been approved by {approver_name} for project '{project_name}', LRU '{lru_name}'. Please review."
                )
                
                if notification_sent:
                    notification_count += 1
                    print(f"✓ Notification sent to QA Head {qa_head['user_id']} ({qa_head['name']})")
                else:
                    error_msg = f"Failed to send notification to QA Head {qa_head['user_id']} ({qa_head['name']})"
                    notification_errors.append(error_msg)
                    print(f"✗ {error_msg}")
        else:
            print(f"WARNING: No QA Heads to notify. Cannot send approval notifications.")
        
        print(f"✓ Approval notifications sent to {notification_count} QA Head(s)")
        
        if notification_errors:
            print(f"ERROR: {len(notification_errors)} notification(s) failed:")
            for error in notification_errors:
                print(f"  - {error}")
        
        if notification_count > 0:
            return jsonify({
                "success": True,
                "message": f"Activity logged and approval notifications sent to {notification_count} QA Head(s)"
            })
        else:
            if not qa_heads or len(qa_heads) == 0:
                return jsonify({
                    "success": False,
                    "message": "Activity logged but no QA Heads found to notify. Please ensure QA Heads are assigned role_id = 2."
                })
            else:
                return jsonify({
                    "success": False,
                    "message": f"Activity logged but failed to send notifications to {len(qa_heads)} QA Head(s). Check server logs for details."
                })
        
    except Exception as e:
        print(f"Error notifying QA Heads for kit of parts report approval: {str(e)}")
        return handle_database_error(get_db_connection(), f"Error notifying QA Heads for approval: {str(e)}")

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
