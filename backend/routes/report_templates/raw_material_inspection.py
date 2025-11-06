# Raw Material Inspection Report API Endpoints

import os
import uuid
from flask import Blueprint, request, jsonify, send_file
from config import get_db_connection, Config
from utils.helpers import handle_database_error
from utils.helpers import handle_database_error, allowed_file, validate_file_size

raw_material_bp = Blueprint('raw_material', __name__)

@raw_material_bp.route('/api/reports/raw-material-inspection', methods=['POST'])
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

@raw_material_bp.route('/api/reports/raw-material-inspection/<int:report_id>', methods=['GET'])
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

@raw_material_bp.route('/api/reports/raw-material-inspection/<int:report_id>', methods=['PUT'])
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

@raw_material_bp.route('/api/reports/raw-material-inspection', methods=['GET'])
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

