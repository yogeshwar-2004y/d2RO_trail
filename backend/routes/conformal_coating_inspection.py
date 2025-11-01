"""
Conformal Coating Inspection Report API Routes
Handles all database operations for conformal coating inspection reports
"""
from flask import Blueprint, request, jsonify
from config import get_db_connection
from utils.helpers import handle_database_error

# Create blueprint for conformal coating inspection reports
conformal_coating_bp = Blueprint('conformal_coating', __name__)


@conformal_coating_bp.route('/api/reports/conformal-coating-inspection', methods=['POST'])
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
        
        conn = None
        cur = None
        try:
            conn = get_db_connection()
            cur = conn.cursor()
            
            # Verify table exists
            cur.execute("""
                SELECT EXISTS (
                    SELECT FROM information_schema.tables 
                    WHERE table_schema = 'public' 
                    AND table_name = 'conformal_coating_inspection_report'
                );
            """)
            table_exists = cur.fetchone()[0]
            if not table_exists:
                raise Exception("Table 'conformal_coating_inspection_report' does not exist in the database. Please create the table first.")
            print(f"  ✓ Table 'conformal_coating_inspection_report' exists")
            
            # Debug: Print received data
            print(f"Creating conformal coating report with data:")
            print(f"  Project: {data.get('project_name')}")
            print(f"  Report Ref: {data.get('report_ref_no')}")
            print(f"  Tests array length: {len(data.get('tests', []))}")
            print(f"  Prepared By: {data.get('prepared_by')}")
            print(f"  Verified By: {data.get('verified_by')}")
            print(f"  Approved By: {data.get('approved_by')}")
            
            # Extract and prepare test data
            tests = data.get('tests', [])
            while len(tests) < 9:
                tests.append({})
            
            # Prepare test values - get observation, remark, upload, and expected for each test
            # Note: rem1-rem9 have CHECK constraints allowing only 'OK', 'NOT OK', or 'NA'
            # Empty remarks will be set to None (NULL) to satisfy constraints
            test_values = []
            for i in range(9):
                test = tests[i] if i < len(tests) else {}
                observation = test.get('observation', '') or None
                remark = test.get('remark', '').strip() if test.get('remark') else None
                # Ensure remark is valid for CHECK constraint: 'OK', 'NOT OK', 'NA', or NULL
                if remark and remark not in ['OK', 'NOT OK', 'NA']:
                    remark = None
                upload = test.get('upload', '') or None
                expected = test.get('expected', '') or None
                
                test_values.extend([observation, remark, upload, expected])
            
            print(f"  Test values prepared: {len(test_values)} values")
            for i in range(min(9, len(tests))):
                idx = i * 4
                if idx + 3 < len(test_values):
                    print(f"  Test {i+1} - obs: {test_values[idx]}, rem: {test_values[idx+1]}, upload: {test_values[idx+2]}, expected: {test_values[idx+3]}")
            
            print(f"  Saving signature paths:")
            print(f"    Prepared By: {data.get('prepared_by')}")
            print(f"    Verified By: {data.get('verified_by')}")
            print(f"    Approved By: {data.get('approved_by')}")
            
            # Prepare quantity - ensure it's an integer or None
            quantity = data.get('quantity')
            if quantity is not None:
                try:
                    quantity = int(quantity)
                except (ValueError, TypeError):
                    quantity = None
            
            # Prepare quality_rating - ensure it's an integer or None
            quality_rating = data.get('quality_rating')
            if quality_rating is not None:
                try:
                    quality_rating = int(quality_rating)
                except (ValueError, TypeError):
                    quality_rating = None
            
            # Prepare all values for INSERT
            insert_values = (
                data['project_name'],
                data['report_ref_no'],
                data.get('memo_ref_no') or None,
                data.get('lru_name') or None,
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
                # Test cases 1-9 - using prepared test_values (36 values)
                *test_values,
                # Summary fields (3 values)
                data.get('overall_status') or None,
                quality_rating,
                data.get('recommendations') or None,
                # Signatures with paths (3 values)
                data.get('prepared_by') or None,
                data.get('verified_by') or None,
                data.get('approved_by') or None
            )
            
            # Verify value count matches placeholder count
            placeholder_count = 58  # 16 headers + 36 tests + 3 summary + 3 signatures
            value_count = len(insert_values)
            
            print(f"  INSERT VALUES COUNT CHECK:")
            print(f"    Expected: {placeholder_count} values")
            print(f"    Actual: {value_count} values")
            print(f"    Test values count: {len(test_values)} (should be 36)")
            
            if value_count != placeholder_count:
                raise ValueError(f"Value count mismatch! Expected {placeholder_count}, got {value_count}. Test values: {len(test_values)}")
            
            # Insert conformal coating inspection report into the database
            # This INSERT statement stores ALL data in the conformal_coating_inspection_report table
            print(f"  Executing INSERT INTO conformal_coating_inspection_report...")
            try:
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
                """, insert_values)
                
                report_id = cur.fetchone()[0]
                print(f"  ✓ INSERT executed successfully, got report_id: {report_id}")
                
            except Exception as db_error:
                print(f"  ✗ DATABASE ERROR during INSERT:")
                print(f"    Error type: {type(db_error).__name__}")
                print(f"    Error message: {str(db_error)}")
                import traceback
                print(f"    Full traceback:")
                traceback.print_exc()
                raise  # Re-raise to be caught by outer exception handler
            
            # Commit the transaction to save data to database
            print(f"  Committing transaction...")
            conn.commit()
            print(f"  ✓ Transaction committed successfully")
            
            print(f"✓ Successfully saved conformal coating report to database with ID: {report_id}")
            print(f"  Storage location: conformal_coating_inspection_report table")
            print(f"  Saved fields:")
            print(f"    - Header fields (16): project_name, report_ref_no, memo_ref_no, lru_name, sru_name, dp_name, part_no, inspection_stage, test_venue, quantity, sl_nos, serial_number, start_date, end_date, dated1, dated2")
            print(f"    - Test cases 1-9 (36 fields): obs1-9, rem1-9, upload1-9, expected1-9")
            print(f"    - Summary (3 fields): overall_status, quality_rating, recommendations")
            print(f"    - Signatures (3 fields): prepared_by, verified_by, approved_by (with signature paths)")
            print(f"  Total: 58 fields stored in conformal_coating_inspection_report table")
            print(f"  All data stored successfully according to your database schema")
            
            # Log conformal coating report submission activity (non-critical, don't fail if this errors)
            try:
                from utils.activity_logger import log_activity
                report_name = data.get('report_ref_no') or f"Conformal Coating Report {report_id}"
                log_activity(
                    project_id=None,  # Report operations don't have project_id in this context
                    activity_performed="Report Submitted",
                    performed_by=data.get('prepared_by', 1002),  # Default to admin if not provided
                    additional_info=f"ID:{report_id}|Name:{report_name}|Conformal Coating Report '{report_name}' (ID: {report_id}) was submitted"
                )
                print(f"  ✓ Activity logged successfully")
            except Exception as log_error:
                print(f"  ⚠ Warning: Could not log activity (non-critical): {str(log_error)}")
                # Don't fail the request if activity logging fails
            
            return jsonify({
                "success": True,
                "message": "Conformal coating inspection report created successfully",
                "report_id": report_id
            })
            
        except Exception as e:
            # Rollback transaction on error
            if conn:
                conn.rollback()
            print(f"ERROR creating conformal coating inspection report: {str(e)}")
            import traceback
            traceback.print_exc()
            return jsonify({
                "success": False,
                "message": f"Error creating conformal coating inspection report: {str(e)}"
            }), 500
        finally:
            # Close cursor and connection
            if cur:
                cur.close()
            if conn:
                conn.close()
                
    except Exception as e:
        # Catch any errors in validation or other parts
        print(f"ERROR in conformal coating inspection report endpoint: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({
            "success": False,
            "message": f"Error processing request: {str(e)}"
        }), 500


@conformal_coating_bp.route('/api/reports/conformal-coating-inspection/<int:report_id>', methods=['GET'])
def get_conformal_coating_inspection_report(report_id):
    """Get conformal coating inspection report details"""
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        
        cur.execute("""
            SELECT * FROM conformal_coating_inspection_report WHERE report_id = %s
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
        print(f"Error fetching conformal coating inspection report: {str(e)}")
        return handle_database_error(get_db_connection(), f"Error fetching conformal coating inspection report: {str(e)}")


@conformal_coating_bp.route('/api/reports/conformal-coating-inspection/<int:report_id>', methods=['PUT'])
def update_conformal_coating_inspection_report(report_id):
    """Update conformal coating inspection report"""
    conn = None
    cur = None
    try:
        data = request.json
        if not data:
            return jsonify({"success": False, "message": "No data provided"}), 400
        
        print(f"UPDATE request received for conformal coating report ID: {report_id}")
        print(f"Update data: {data}")
        
        conn = get_db_connection()
        cur = conn.cursor()
        
        # First, check if the report exists
        cur.execute("""
            SELECT report_id FROM conformal_coating_inspection_report WHERE report_id = %s
        """, (report_id,))
        
        existing_report = cur.fetchone()
        if not existing_report:
            print(f"Report ID {report_id} not found in conformal_coating_inspection_report table")
            return jsonify({
                "success": False, 
                "message": f"Report not found with ID: {report_id}. Please create the report first."
            }), 404
        
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
                # Handle quantity as integer
                if field == 'quantity' and data[field] is not None:
                    try:
                        update_values.append(int(data[field]))
                    except (ValueError, TypeError):
                        update_values.append(None)
                else:
                    update_values.append(data[field] or None)
        
        # Test cases (obs1-9, rem1-9, upload1-9, expected1-9)
        for i in range(1, 10):
            for prefix in ['obs', 'rem', 'upload', 'expected']:
                field = f"{prefix}{i}"
                if field in data:
                    update_fields.append(f"{field} = %s")
                    # Validate remarks for CHECK constraint
                    if prefix == 'rem' and data[field]:
                        remark_value = data[field].strip()
                        if remark_value not in ['OK', 'NOT OK', 'NA']:
                            print(f"Warning: Invalid remark value '{remark_value}' for {field}, setting to None")
                            update_values.append(None)
                        else:
                            update_values.append(remark_value)
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
        
        # Signatory fields (signature URLs are stored in the user fields, not separate columns)
        signatory_fields = ['prepared_by', 'verified_by', 'approved_by']
        for field in signatory_fields:
            if field in data:
                update_fields.append(f"{field} = %s")
                update_values.append(data[field] or None)
        
        if not update_fields:
            return jsonify({"success": False, "message": "No fields to update"}), 400
        
        # Add updated_at timestamp
        update_fields.append("updated_at = CURRENT_TIMESTAMP")
        
        # Execute update on the conformal_coating_inspection_report table
        update_query = f"UPDATE conformal_coating_inspection_report SET {', '.join(update_fields)} WHERE report_id = %s"
        update_values.append(report_id)
        
        print(f"Updating conformal_coating_inspection_report table - Report ID: {report_id}")
        print(f"Update fields: {update_fields}")
        print(f"Update values count: {len(update_values)}")
        
        cur.execute(update_query, update_values)
        
        # Commit the transaction
        conn.commit()
        
        print(f"✓ Successfully updated report ID {report_id} in conformal_coating_inspection_report table")
        print(f"  Updated fields: {', '.join([f for f in update_fields if f != 'updated_at = CURRENT_TIMESTAMP'])}")
        
        return jsonify({
            "success": True,
            "message": "Conformal coating inspection report updated successfully",
            "report_id": report_id
        })
        
    except Exception as e:
        # Rollback transaction on error
        if conn:
            conn.rollback()
        print(f"ERROR updating conformal coating inspection report: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({
            "success": False,
            "message": f"Error updating conformal coating inspection report: {str(e)}"
        }), 500
    finally:
        # Close cursor and connection
        if cur:
            cur.close()
        if conn:
            conn.close()


@conformal_coating_bp.route('/api/reports/conformal-coating-inspection/notify', methods=['POST'])
def notify_qa_heads_conformal_coating():
    """Notify QA Heads when a conformal coating inspection report is submitted"""
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
        
        # Get reviewer name
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT name FROM users WHERE user_id = %s", (reviewer_id,))
        reviewer_result = cur.fetchone()
        reviewer_name = reviewer_result[0] if reviewer_result else "Reviewer"
        cur.close()
        
        # Notify each QA Head
        for qa_head in qa_heads:
            memo_text = f" corresponding to memo {memo_ref_no}" if memo_ref_no else ""
            log_notification(
                project_id=None,
                activity_performed=f"Conformal Coating Inspection Report{memo_text} Submitted",
                performed_by=reviewer_id,
                notified_user_id=qa_head['user_id'],
                notification_type="report_submitted",
                additional_info=f"Report ID {report_id}{memo_text} has been submitted by {reviewer_name}. Please review."
            )
        
        return jsonify({
            "success": True,
            "message": f"Notifications sent to {len(qa_heads)} QA Head(s)"
        })
        
    except Exception as e:
        print(f"Error notifying QA Heads for conformal coating report: {str(e)}")
        return handle_database_error(get_db_connection(), f"Error notifying QA Heads: {str(e)}")


@conformal_coating_bp.route('/api/reports/conformal-coating-inspection', methods=['GET'])
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

