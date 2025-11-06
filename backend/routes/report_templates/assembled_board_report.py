# Assembled Board Inspection Report Routes

import os
import uuid
from flask import Blueprint, request, jsonify
from config import get_db_connection, Config
from utils.helpers import handle_database_error
from utils.helpers import handle_database_error, allowed_file, validate_file_size

# Create blueprint for conformal coating inspection reports
assembled_board_bp = Blueprint('assembled_board', __name__)

@assembled_board_bp.route('/api/reports/assembled-board', methods=['POST'])
# @require_design_head_role
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
        
        # Check if report_card_id exists in table, add if missing
        report_card_id = data.get('report_card_id')
        cur.execute("""
            SELECT column_name 
            FROM information_schema.columns 
            WHERE table_name = 'assembled_board_inspection_report' 
            AND column_name = 'report_card_id'
        """)
        has_report_card_id = cur.fetchone() is not None
        
        if not has_report_card_id and report_card_id:
            try:
                cur.execute("ALTER TABLE assembled_board_inspection_report ADD COLUMN report_card_id INTEGER")
                conn.commit()
                has_report_card_id = True
                print("Added report_card_id column to assembled_board_inspection_report table")
            except Exception as e:
                print(f"Note: Could not add report_card_id column (may already exist): {str(e)}")
                conn.rollback()
        
        # Check if report already exists for this report_card_id
        existing_report_id = None
        if report_card_id:
            if has_report_card_id:
                cur.execute("""
                    SELECT report_id FROM assembled_board_inspection_report 
                    WHERE report_card_id = %s
                """, (report_card_id,))
                existing = cur.fetchone()
                if existing:
                    existing_report_id = existing[0]
        
        # Get user ID from request or data
        user_id = request.args.get('user_id', type=int) or data.get('user_id') or 1002
        
        if existing_report_id:
            # Update existing report
            print(f"Updating existing report with ID: {existing_report_id}")
            cur.execute("""
                UPDATE assembled_board_inspection_report SET
                    project_name = %s, report_ref_no = %s, memo_ref_no = %s, lru_name = %s, 
                    sru_name = %s, dp_name = %s, part_no = %s, inspection_stage = %s, 
                    test_venue = %s, quantity = %s, sl_nos = %s, serial_number = %s,
                    start_date = %s, end_date = %s, dated1 = %s, dated2 = %s,
                    obs1 = %s, rem1 = %s, upload1 = %s, obs2 = %s, rem2 = %s, upload2 = %s,
                    obs3 = %s, rem3 = %s, upload3 = %s, obs4 = %s, rem4 = %s, upload4 = %s,
                    obs5 = %s, rem5 = %s, upload5 = %s, obs6 = %s, rem6 = %s, upload6 = %s,
                    obs7 = %s, rem7 = %s, upload7 = %s, obs8 = %s, rem8 = %s, upload8 = %s,
                    obs9 = %s, rem9 = %s, upload9 = %s, obs10 = %s, rem10 = %s, upload10 = %s,
                    obs11 = %s, rem11 = %s, upload11 = %s, obs12 = %s, rem12 = %s, upload12 = %s,
                    obs13 = %s, rem13 = %s, upload13 = %s, obs14 = %s, rem14 = %s, upload14 = %s,
                    obs15 = %s, rem15 = %s, upload15 = %s, obs16 = %s, rem16 = %s, upload16 = %s,
                    obs17 = %s, rem17 = %s, upload17 = %s, obs18 = %s, rem18 = %s, upload18 = %s,
                    obs19 = %s, rem19 = %s, upload19 = %s, obs20 = %s, rem20 = %s, upload20 = %s,
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
                'start_date', 'end_date', 'dated1', 'dated2',
                'obs1', 'rem1', 'upload1', 'obs2', 'rem2', 'upload2', 'obs3', 'rem3', 'upload3',
                'obs4', 'rem4', 'upload4', 'obs5', 'rem5', 'upload5', 'obs6', 'rem6', 'upload6',
                'obs7', 'rem7', 'upload7', 'obs8', 'rem8', 'upload8', 'obs9', 'rem9', 'upload9',
                'obs10', 'rem10', 'upload10', 'obs11', 'rem11', 'upload11', 'obs12', 'rem12', 'upload12',
                'obs13', 'rem13', 'upload13', 'obs14', 'rem14', 'upload14', 'obs15', 'rem15', 'upload15',
                'obs16', 'rem16', 'upload16', 'obs17', 'rem17', 'upload17', 'obs18', 'rem18', 'upload18',
                'obs19', 'rem19', 'upload19', 'obs20', 'rem20', 'upload20',
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
                data.get('start_date') or None,
                data.get('end_date') or None,
                data.get('dated1') or None,
                data.get('dated2') or None,
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
                INSERT INTO assembled_board_inspection_report ({column_names})
                VALUES ({placeholders})
                RETURNING report_id
            """, values)
            
        report_id = cur.fetchone()[0]
        
        print("Insert/Update query executed successfully")  # Debug log
        
        # Commit the transaction FIRST before logging activity
        conn.commit()
        cur.close()
        
        print(f"Report created/updated with ID: {report_id}")  # Debug log
        
        # Log assembled board report submission activity (after commit to avoid rollback)
        try:
            from utils.activity_logger import log_activity
            report_name = data.get('report_ref_no') or f"Assembled Board Report {report_id}"
            
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
                additional_info=f"ID:{report_id}|Name:{report_name}|Assembled Board Report '{report_name}' (ID: {report_id}) was submitted"
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
                                        activity_performed="Assembled Board Inspection Report Completed",
                                        performed_by=performed_by,
                                        notified_user_id=user_id_notify,
                                        notification_type="report_completed",
                                        additional_info=f"Assembled Board Inspection Report (ID: {report_id}) for Report Card {report_card_id} has been completed with all signatures."
                                    )
                        except Exception as e:
                            print(f"Error sending notification to role {role_id}: {str(e)}")
                            pass
            except Exception as e:
                print(f"Error sending notifications: {str(e)}")
                pass
        
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

@assembled_board_bp.route('/api/reports/assembled-board/<int:report_id>', methods=['GET'])
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

@assembled_board_bp.route('/api/reports/assembled-board/by-report-card/<int:report_card_id>', methods=['GET'])
def get_assembled_board_report_by_report_card(report_card_id):
    """Get assembled board inspection report by report card ID"""
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        
        # Check if report_card_id column exists
        cur.execute("""
            SELECT column_name 
            FROM information_schema.columns 
            WHERE table_name = 'assembled_board_inspection_report' 
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
                obs1, rem1, upload1, obs2, rem2, upload2, obs3, rem3, upload3,
                obs4, rem4, upload4, obs5, rem5, upload5, obs6, rem6, upload6,
                obs7, rem7, upload7, obs8, rem8, upload8, obs9, rem9, upload9,
                obs10, rem10, upload10, obs11, rem11, upload11, obs12, rem12, upload12,
                obs13, rem13, upload13, obs14, rem14, upload14, obs15, rem15, upload15,
                obs16, rem16, upload16, obs17, rem17, upload17, obs18, rem18, upload18,
                obs19, rem19, upload19, obs20, rem20, upload20,
                prepared_by, verified_by, approved_by, created_at, updated_at
            FROM assembled_board_inspection_report 
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

@assembled_board_bp.route('/api/reports/assembled-board/<int:report_id>', methods=['PUT'])
# @require_design_head_role
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

@assembled_board_bp.route('/api/reports/assembled-board', methods=['GET'])
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

@assembled_board_bp.route('/api/reports/assembled-board/count', methods=['GET'])
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

@assembled_board_bp.route('/api/reports/assembled-board/upload', methods=['POST'])
# @require_design_head_role
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

@assembled_board_bp.route('/api/reports/assembled-board/files/<path:filename>', methods=['GET'])
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
