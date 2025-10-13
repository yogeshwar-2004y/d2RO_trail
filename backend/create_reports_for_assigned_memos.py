"""
Script to create reports for all existing assigned memos
This script will automatically create report records for memos that are in 'assigned' state
"""

import psycopg2
from config import get_db_connection
from datetime import datetime

def create_reports_for_assigned_memos():
    """Create reports for all memos that are currently in 'assigned' state"""
    conn = None
    try:
        conn = get_db_connection()
        cur = conn.cursor()

        print("✅ Database connection established successfully")
        print("Starting report creation for assigned memos...")

        # Fetch all assigned memos
        cur.execute("""
            SELECT 
                m.memo_id,
                m.wing_proj_ref_no,
                m.lru_sru_desc,
                m.part_number,
                m.venue,
                m.slno_units,
                m.qty_offered,
                m.manufacturer,
                m.drawing_no_rev,
                m.source,
                m.mechanical_inspn,
                m.inspn_test_stage_offered,
                m.stte_status,
                m.test_stage_cleared,
                m.memo_date,
                m.name_designation,
                m.test_facility,
                m.test_cycle_duration,
                m.calibration_status,
                m.remarks,
                m.accepted_at,
                m.accepted_by
            FROM memos m
            WHERE m.memo_status = 'assigned'
            ORDER BY m.memo_id
        """)

        assigned_memos = cur.fetchall()
        print(f"📋 Found {len(assigned_memos)} assigned memos to process")

        # Fetch project and LRU mappings
        cur.execute("SELECT project_id, project_name FROM projects ORDER BY project_id")
        projects = {row[1].lower(): row[0] for row in cur.fetchall()}

        cur.execute("SELECT lru_id, lru_name FROM lrus ORDER BY lru_id")
        lrus = {row[1].lower(): row[0] for row in cur.fetchall()}

        reports_created = 0

        for memo in assigned_memos:
            memo_id = memo[0]
            wing_proj_ref_no = memo[1] or ""
            lru_sru_desc = memo[2] or ""
            venue = memo[4]
            slno_units = memo[5]
            memo_date = memo[14]

            print(f"\n🚀 Processing Memo ID: {memo_id}")
            print(f"   ➤ Wing/Project Ref: {wing_proj_ref_no}")
            print(f"   ➤ LRU Description: {lru_sru_desc}")
            print(f"   ➤ Venue: {venue}")

            # Skip if report already exists
            cur.execute("SELECT report_id FROM reports WHERE memo_id = %s", (memo_id,))
            if cur.fetchone():
                print(f"   ⚠ Report already exists for memo {memo_id}, skipping...")
                continue

            # Map project_id
            project_id = 1  # default fallback
            for proj_name, proj_id in projects.items():
                if proj_name in wing_proj_ref_no.lower():
                    project_id = proj_id
                    break

            # Map lru_id
            lru_id = 1  # default fallback
            for lru_name, lru_val in lrus.items():
                if lru_name in lru_sru_desc.lower():
                    lru_id = lru_val
                    break

            # Determine valid serial_id
            serial_id = None
            try:
                cur.execute("""
                    SELECT serial_id FROM serial_numbers
                    WHERE lru_id = %s
                    ORDER BY serial_id
                    LIMIT 1
                """, (lru_id,))
                serial_result = cur.fetchone()
                if serial_result:
                    serial_id = serial_result[0]
                else:
                    # Create a new serial record safely
                    cur.execute("""
                        INSERT INTO serial_numbers (lru_id, serial_number, created_at)
                        VALUES (%s, %s, %s)
                        RETURNING serial_id
                    """, (lru_id, 1, datetime.now()))
                    serial_id = cur.fetchone()[0]
                    print(f"   ➕ Created new serial_id: {serial_id} for LRU {lru_id}")
            except Exception as e:
                print(f"   ⚠ Serial number lookup failed: {e}")
                serial_id = 1  # safe fallback

            # Ensure serial_id exists before insert
            if not serial_id:
                print(f"   ⚠ No valid serial_id found — skipping memo {memo_id}")
                continue

            # Create report
            try:
                cur.execute("""
                    INSERT INTO reports (
                        memo_id, project_id, lru_id, serial_id,
                        inspection_stage, date_of_review, review_venue,
                        status, created_at
                    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                    RETURNING report_id
                """, (
                    memo_id,
                    project_id,
                    lru_id,
                    serial_id,
                    lru_sru_desc,
                    memo_date,
                    venue,
                    'ASSIGNED',
                    datetime.now()
                ))

                report_id = cur.fetchone()[0]
                conn.commit()
                reports_created += 1
                print(f"   ✅ Created report ID: {report_id}")
                print(f"      → Project ID: {project_id}, LRU ID: {lru_id}, Serial ID: {serial_id}")

            except Exception as e:
                conn.rollback()
                print(f"   ❌ Error creating report for memo {memo_id}: {e}")

        print(f"\n🎯 Successfully created {reports_created} new reports")

    except Exception as e:
        print(f"🔥 Fatal Error: {e}")
        if conn:
            conn.rollback()
    finally:
        if conn:
            conn.close()
            print("🔒 Database connection closed.")

if __name__ == "__main__":
    create_reports_for_assigned_memos()
