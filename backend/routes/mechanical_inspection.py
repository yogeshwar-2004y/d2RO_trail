"""
Mechanical Inspection Report management routes
"""
from flask import Blueprint, request, jsonify
from config import get_db_connection
from utils.helpers import handle_database_error

mechanical_inspection_bp = Blueprint('mechanical_inspection', __name__)


def _serialize_dates(report_data):
    """Convert date objects to ISO format strings for JSON serialization"""
    date_fields = ['dated1', 'dated2', 'start_date', 'end_date', 'created_at', 'updated_at']
    for field in date_fields:
        if field in report_data and report_data[field]:
            if hasattr(report_data[field], 'isoformat'):
                report_data[field] = report_data[field].isoformat()
    return report_data

@mechanical_inspection_bp.route('/api/mechanical-inspection', methods=['POST'])
def create_mechanical_inspection():
    """Create a new mechanical inspection report"""
    try:
        data = request.json
        if not data:
            return jsonify({"success": False, "message": "No data provided"}), 400
        
        # Validate required fields
        required_fields = ['project_name', 'report_ref_no', 'lru_name', 'dp_name', 'part_no', 'quantity']
        for field in required_fields:
            if field not in data or not data[field]:
                return jsonify({"success": False, "message": f"Missing required field: {field}"}), 400
        
        conn = get_db_connection()
        cur = conn.cursor()
        
        # Ensure table exists
        cur.execute("""
            CREATE TABLE IF NOT EXISTS mechanical_inspection_report (
                report_id SERIAL PRIMARY KEY,
                report_card_id INT REFERENCES reports(report_id) ON DELETE CASCADE,
                project_name TEXT,
                report_ref_no VARCHAR(100),
                memo_ref_no VARCHAR(100),
                lru_name TEXT,
                inspection_stage TEXT,
                test_venue TEXT,
                sl_nos TEXT,
                dp_name TEXT,
                dated1 DATE,
                dated2 DATE,
                sru_name TEXT,
                part_no VARCHAR(100),
                quantity INT,
                start_date DATE,
                end_date DATE,
                dim1_dimension TEXT, dim1_tolerance TEXT, dim1_observed_value TEXT, dim1_instrument_used TEXT, dim1_remarks TEXT, dim1_upload TEXT,
                dim2_dimension TEXT, dim2_tolerance TEXT, dim2_observed_value TEXT, dim2_instrument_used TEXT, dim2_remarks TEXT, dim2_upload TEXT,
                dim3_dimension TEXT, dim3_tolerance TEXT, dim3_observed_value TEXT, dim3_instrument_used TEXT, dim3_remarks TEXT, dim3_upload TEXT,
                dim4_dimension TEXT, dim4_tolerance TEXT, dim4_observed_value TEXT, dim4_instrument_used TEXT, dim4_remarks TEXT, dim4_upload TEXT,
                param1_name TEXT DEFAULT 'Burrs', param1_compliance_observation TEXT, param1_expected TEXT DEFAULT 'Not Expected (NO)', param1_remarks TEXT, param1_upload TEXT,
                param2_name TEXT DEFAULT 'Damages', param2_compliance_observation TEXT, param2_expected TEXT DEFAULT 'Not Expected (NO)', param2_remarks TEXT, param2_upload TEXT,
                param3_name TEXT DEFAULT 'Name Plate', param3_compliance_observation TEXT, param3_expected TEXT DEFAULT 'As per Drawing (YES)', param3_remarks TEXT, param3_upload TEXT,
                param4_name TEXT DEFAULT 'Engraving', param4_compliance_observation TEXT, param4_expected TEXT DEFAULT 'As per Drawing (YES)', param4_remarks TEXT, param4_upload TEXT,
                param5_name TEXT DEFAULT 'Passivation', param5_compliance_observation TEXT, param5_expected TEXT DEFAULT 'As per Drawing (YES)', param5_remarks TEXT, param5_upload TEXT,
                param6_name TEXT DEFAULT 'Chromate', param6_compliance_observation TEXT, param6_expected TEXT DEFAULT 'As per Drawing (YES)', param6_remarks TEXT, param6_upload TEXT,
                param7_name TEXT DEFAULT 'Electro-less Nickel plating', param7_compliance_observation TEXT, param7_expected TEXT DEFAULT 'As per Drawing (YES)', param7_remarks TEXT, param7_upload TEXT,
                param8_name TEXT DEFAULT 'Fasteners', param8_compliance_observation TEXT, param8_expected TEXT DEFAULT 'As per Drawing (YES)', param8_remarks TEXT, param8_upload TEXT,
                prepared_by TEXT,
                verified_by TEXT,
                approved_by TEXT,
                created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Add report_card_id column if missing (for existing tables)
        try:
            cur.execute("""
                SELECT EXISTS (
                    SELECT 1 FROM information_schema.columns 
                    WHERE table_name='mechanical_inspection_report' AND column_name='report_card_id'
                );
            """)
            column_exists = cur.fetchone()[0]
            
            if not column_exists:
                cur.execute("""
                    ALTER TABLE mechanical_inspection_report 
                    ADD COLUMN report_card_id INT REFERENCES reports(report_id) ON DELETE CASCADE;
                """)
                cur.execute("""
                    CREATE INDEX IF NOT EXISTS idx_mechanical_inspection_report_card_id 
                    ON mechanical_inspection_report(report_card_id);
                """)
                conn.commit()
        except Exception as e:
            conn.rollback()
        
        report_card_id = data.get('report_card_id')
        existing_report = None
        if report_card_id:
            try:
                cur.execute("SELECT report_id FROM mechanical_inspection_report WHERE report_card_id = %s", (report_card_id,))
                existing_report = cur.fetchone()
            except Exception:
                pass
        
        if existing_report:
            # Update existing report
            cur.execute("""
                UPDATE mechanical_inspection_report SET
                    project_name = %s, report_ref_no = %s, memo_ref_no = %s, lru_name = %s, 
                    inspection_stage = %s, test_venue = %s, sl_nos = %s, dp_name = %s,
                    dated1 = %s, dated2 = %s, sru_name = %s, part_no = %s, quantity = %s,
                    start_date = %s, end_date = %s,
                    dim1_dimension = %s, dim1_tolerance = %s, dim1_observed_value = %s, dim1_instrument_used = %s, dim1_remarks = %s, dim1_upload = %s,
                    dim2_dimension = %s, dim2_tolerance = %s, dim2_observed_value = %s, dim2_instrument_used = %s, dim2_remarks = %s, dim2_upload = %s,
                    dim3_dimension = %s, dim3_tolerance = %s, dim3_observed_value = %s, dim3_instrument_used = %s, dim3_remarks = %s, dim3_upload = %s,
                    dim4_dimension = %s, dim4_tolerance = %s, dim4_observed_value = %s, dim4_instrument_used = %s, dim4_remarks = %s, dim4_upload = %s,
                    param1_compliance_observation = %s, param1_expected = %s, param1_remarks = %s, param1_upload = %s,
                    param2_compliance_observation = %s, param2_expected = %s, param2_remarks = %s, param2_upload = %s,
                    param3_compliance_observation = %s, param3_expected = %s, param3_remarks = %s, param3_upload = %s,
                    param4_compliance_observation = %s, param4_expected = %s, param4_remarks = %s, param4_upload = %s,
                    param5_compliance_observation = %s, param5_expected = %s, param5_remarks = %s, param5_upload = %s,
                    param6_compliance_observation = %s, param6_expected = %s, param6_remarks = %s, param6_upload = %s,
                    param7_compliance_observation = %s, param7_expected = %s, param7_remarks = %s, param7_upload = %s,
                    param8_compliance_observation = %s, param8_expected = %s, param8_remarks = %s, param8_upload = %s,
                    prepared_by = %s, verified_by = %s, approved_by = %s,
                    updated_at = CURRENT_TIMESTAMP
                WHERE report_card_id = %s
                RETURNING report_id
            """, (
                data['project_name'], data['report_ref_no'], data.get('memo_ref_no'), data['lru_name'],
                data.get('inspection_stage'), data.get('test_venue'), data.get('sl_nos'), data['dp_name'],
                data.get('dated1'), data.get('dated2'), data.get('sru_name'), data['part_no'], data['quantity'],
                data.get('start_date'), data.get('end_date'),
                data.get('dim1_dimension'), data.get('dim1_tolerance'), data.get('dim1_observed_value'),
                data.get('dim1_instrument_used'), data.get('dim1_remarks'), data.get('dim1_upload'),
                data.get('dim2_dimension'), data.get('dim2_tolerance'), data.get('dim2_observed_value'),
                data.get('dim2_instrument_used'), data.get('dim2_remarks'), data.get('dim2_upload'),
                data.get('dim3_dimension'), data.get('dim3_tolerance'), data.get('dim3_observed_value'),
                data.get('dim3_instrument_used'), data.get('dim3_remarks'), data.get('dim3_upload'),
                data.get('dim4_dimension'), data.get('dim4_tolerance'), data.get('dim4_observed_value'),
                data.get('dim4_instrument_used'), data.get('dim4_remarks'), data.get('dim4_upload'),
                data.get('param1_compliance_observation'), data.get('param1_expected'),
                data.get('param1_remarks'), data.get('param1_upload'),
                data.get('param2_compliance_observation'), data.get('param2_expected'),
                data.get('param2_remarks'), data.get('param2_upload'),
                data.get('param3_compliance_observation'), data.get('param3_expected'),
                data.get('param3_remarks'), data.get('param3_upload'),
                data.get('param4_compliance_observation'), data.get('param4_expected'),
                data.get('param4_remarks'), data.get('param4_upload'),
                data.get('param5_compliance_observation'), data.get('param5_expected'),
                data.get('param5_remarks'), data.get('param5_upload'),
                data.get('param6_compliance_observation'), data.get('param6_expected'),
                data.get('param6_remarks'), data.get('param6_upload'),
                data.get('param7_compliance_observation'), data.get('param7_expected'),
                data.get('param7_remarks'), data.get('param7_upload'),
                data.get('param8_compliance_observation'), data.get('param8_expected'),
                data.get('param8_remarks'), data.get('param8_upload'),
                data.get('prepared_by'), data.get('verified_by'), data.get('approved_by'),
                report_card_id
            ))
        else:
            # Insert new mechanical inspection report with all fields
            cur.execute("""
            INSERT INTO mechanical_inspection_report (
                    report_card_id, project_name, report_ref_no, memo_ref_no, lru_name, inspection_stage,
                test_venue, sl_nos, dp_name, dated1, dated2, sru_name, part_no, quantity,
                start_date, end_date,
                dim1_dimension, dim1_tolerance, dim1_observed_value, dim1_instrument_used, dim1_remarks, dim1_upload,
                dim2_dimension, dim2_tolerance, dim2_observed_value, dim2_instrument_used, dim2_remarks, dim2_upload,
                dim3_dimension, dim3_tolerance, dim3_observed_value, dim3_instrument_used, dim3_remarks, dim3_upload,
                dim4_dimension, dim4_tolerance, dim4_observed_value, dim4_instrument_used, dim4_remarks, dim4_upload,
                param1_compliance_observation, param1_expected, param1_remarks, param1_upload,
                param2_compliance_observation, param2_expected, param2_remarks, param2_upload,
                param3_compliance_observation, param3_expected, param3_remarks, param3_upload,
                param4_compliance_observation, param4_expected, param4_remarks, param4_upload,
                param5_compliance_observation, param5_expected, param5_remarks, param5_upload,
                param6_compliance_observation, param6_expected, param6_remarks, param6_upload,
                param7_compliance_observation, param7_expected, param7_remarks, param7_upload,
                param8_compliance_observation, param8_expected, param8_remarks, param8_upload,
                prepared_by, verified_by, approved_by
            ) VALUES (
                %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
                %s, %s, %s, %s, %s, %s,
                %s, %s, %s, %s, %s, %s,
                %s, %s, %s, %s, %s, %s,
                %s, %s, %s, %s, %s, %s,
                %s, %s, %s, %s,
                %s, %s, %s, %s,
                %s, %s, %s, %s,
                %s, %s, %s, %s,
                %s, %s, %s, %s,
                %s, %s, %s, %s,
                %s, %s, %s, %s,
                %s, %s, %s, %s,
                %s, %s, %s
            ) RETURNING report_id
        """, (
            report_card_id,
            data['project_name'], 
            data['report_ref_no'], 
            data.get('memo_ref_no'), 
            data['lru_name'],
            data.get('inspection_stage'), 
            data.get('test_venue'), 
            data.get('sl_nos'), 
            data['dp_name'],
            data.get('dated1'),
            data.get('dated2'), 
            data.get('sru_name'), 
            data['part_no'], 
            data['quantity'],
            data.get('start_date'), 
            data.get('end_date'),
            # Dimension 1
            data.get('dim1_dimension'),
            data.get('dim1_tolerance'),
            data.get('dim1_observed_value'),
            data.get('dim1_instrument_used'),
            data.get('dim1_remarks'),
            data.get('dim1_upload'),
            # Dimension 2
            data.get('dim2_dimension'),
            data.get('dim2_tolerance'),
            data.get('dim2_observed_value'),
            data.get('dim2_instrument_used'),
            data.get('dim2_remarks'),
            data.get('dim2_upload'),
            # Dimension 3
            data.get('dim3_dimension'),
            data.get('dim3_tolerance'),
            data.get('dim3_observed_value'),
            data.get('dim3_instrument_used'),
            data.get('dim3_remarks'),
            data.get('dim3_upload'),
            # Dimension 4
            data.get('dim4_dimension'),
            data.get('dim4_tolerance'),
            data.get('dim4_observed_value'),
            data.get('dim4_instrument_used'),
            data.get('dim4_remarks'),
            data.get('dim4_upload'),
            # Parameter 1
            data.get('param1_compliance_observation'),
            data.get('param1_expected'),
            data.get('param1_remarks'),
            data.get('param1_upload'),
            # Parameter 2
            data.get('param2_compliance_observation'),
            data.get('param2_expected'),
            data.get('param2_remarks'),
            data.get('param2_upload'),
            # Parameter 3
            data.get('param3_compliance_observation'),
            data.get('param3_expected'),
            data.get('param3_remarks'),
            data.get('param3_upload'),
            # Parameter 4
            data.get('param4_compliance_observation'),
            data.get('param4_expected'),
            data.get('param4_remarks'),
            data.get('param4_upload'),
            # Parameter 5
            data.get('param5_compliance_observation'),
            data.get('param5_expected'),
            data.get('param5_remarks'),
            data.get('param5_upload'),
            # Parameter 6
            data.get('param6_compliance_observation'),
            data.get('param6_expected'),
            data.get('param6_remarks'),
            data.get('param6_upload'),
            # Parameter 7
            data.get('param7_compliance_observation'),
            data.get('param7_expected'),
            data.get('param7_remarks'),
            data.get('param7_upload'),
            # Parameter 8
            data.get('param8_compliance_observation'),
            data.get('param8_expected'),
            data.get('param8_remarks'),
            data.get('param8_upload'),
            # Signatures
            data.get('prepared_by'),
            data.get('verified_by'),
            data.get('approved_by')
        ))
        
        report_id = cur.fetchone()[0]
        conn.commit()
        cur.close()
        
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
                    performed_by = report_info[1]
                    
                    for role_id in [4, 2]:  # Design Heads = 4, QA Heads = 2
                        try:
                            users = get_users_by_role(role_id)
                            for user in users:
                                user_id = user.get('user_id') if isinstance(user, dict) else (user[0] if hasattr(user, '__getitem__') else None)
                                if user_id:
                                    log_notification(
                                        project_id=project_id,
                                        activity_performed="Mechanical Inspection Report Completed",
                                        performed_by=performed_by,
                                        notified_user_id=user_id,
                                        notification_type="report_completed",
                                        additional_info=f"Mechanical Inspection Report (ID: {report_id}) for Report Card {report_card_id} has been completed with all signatures."
                                    )
                        except Exception:
                            pass
            except Exception:
                pass
        
        return jsonify({
            "success": True,
            "message": "Mechanical inspection report created successfully",
            "report_id": report_id
        })
        
    except Exception as e:
        return handle_database_error(get_db_connection(), f"Error creating mechanical inspection report: {str(e)}")

@mechanical_inspection_bp.route('/api/mechanical-inspection/by-report-card/<int:report_card_id>', methods=['GET'])
def get_mechanical_inspection_by_report_card(report_card_id):
    """Get mechanical inspection report by report card ID"""
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        
        cur.execute("SELECT * FROM mechanical_inspection_report WHERE report_card_id = %s", (report_card_id,))
        report = cur.fetchone()
        
        if not report:
            cur.close()
            return jsonify({"success": False, "message": "Report not found"}), 404
        
        columns = [desc[0] for desc in cur.description] if cur.description else []
        cur.close()
        
        report_data = _serialize_dates(dict(zip(columns, report)))
        
        return jsonify({
            "success": True,
            "report": report_data
        })
        
    except Exception as e:
        return handle_database_error(get_db_connection(), f"Error fetching mechanical inspection report: {str(e)}")

