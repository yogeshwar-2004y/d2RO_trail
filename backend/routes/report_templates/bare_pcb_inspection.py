# ------------------ Bare PCB Inspection Report Routes ------------------ #

import os
import uuid
from flask import Blueprint, request, jsonify, send_file
from config import get_db_connection, Config
from utils.helpers import handle_database_error
from utils.helpers import handle_database_error, allowed_file, validate_file_size

bare_pcb_bp = Blueprint('bare_pcb', __name__)

@bare_pcb_bp.route('/api/reports/bare-pcb-inspection', methods=['POST'])
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

@bare_pcb_bp.route('/api/reports/bare-pcb-inspection/<int:report_id>', methods=['GET'])
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

@bare_pcb_bp.route('/api/reports/bare-pcb-inspection/by-report-card/<int:report_card_id>', methods=['GET'])
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

@bare_pcb_bp.route('/api/reports/bare-pcb-inspection', methods=['GET'])
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
