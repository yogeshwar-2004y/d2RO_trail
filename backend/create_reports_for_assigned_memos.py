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
        
        print("Starting report creation for assigned memos...")
        
        # Get all assigned memos with their details
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
        print(f"Found {len(assigned_memos)} assigned memos to process")
        
        # Get available projects and LRUs for mapping
        cur.execute("SELECT project_id, project_name FROM projects ORDER BY project_id")
        projects = {row[1]: row[0] for row in cur.fetchall()}
        
        cur.execute("SELECT lru_id, lru_name FROM lrus ORDER BY lru_id")
        lrus = {row[1]: row[0] for row in cur.fetchall()}
        
        print(f"Available projects: {list(projects.keys())}")
        print(f"Available LRUs: {list(lrus.keys())}")
        
        reports_created = 0
        
        for memo in assigned_memos:
            memo_id = memo[0]
            wing_proj_ref_no = memo[1]
            lru_sru_desc = memo[2]
            part_number = memo[3]
            venue = memo[4]
            slno_units = memo[5]  # Array of serial numbers
            qty_offered = memo[6]
            
            print(f"\nProcessing Memo ID: {memo_id}")
            print(f"  Wing/Project Ref: {wing_proj_ref_no}")
            print(f"  LRU Description: {lru_sru_desc}")
            print(f"  Part Number: {part_number}")
            print(f"  Venue: {venue}")
            print(f"  Serial Numbers: {slno_units}")
            print(f"  Quantity: {qty_offered}")
            
            # Check if report already exists for this memo
            cur.execute("SELECT report_id FROM reports WHERE memo_id = %s", (memo_id,))
            if cur.fetchone():
                print(f"  Report already exists for memo {memo_id}, skipping...")
                continue
            
            # Determine project_id and lru_id
            # Try to match based on project name patterns or use defaults
            project_id = 1  # Default project
            lru_id = 1      # Default LRU
            
            # Try to find matching project based on wing_proj_ref_no
            if wing_proj_ref_no:
                for proj_name, proj_id in projects.items():
                    if proj_name.lower() in wing_proj_ref_no.lower():
                        project_id = proj_id
                        break
            
            # Try to find matching LRU based on lru_sru_desc
            if lru_sru_desc:
                for lru_name, lru_id_val in lrus.items():
                    if lru_name.lower() in lru_sru_desc.lower():
                        lru_id = lru_id_val
                        break
            
            # Determine serial_id based on slno_units
            serial_id = 1  # Default serial
            if slno_units and len(slno_units) > 0:
                # Use the first serial number or create a default
                try:
                    # Try to find existing serial number or create one
                    cur.execute("""
                        SELECT serial_id FROM serial_numbers 
                        WHERE lru_id = %s 
                        ORDER BY serial_id 
                        LIMIT 1
                    """, (lru_id,))
                    result = cur.fetchone()
                    if result:
                        serial_id = result[0]
                    else:
                        # Create a new serial number entry
                        cur.execute("""
                            INSERT INTO serial_numbers (lru_id, serial_number)
                            VALUES (%s, %s)
                            RETURNING serial_id
                        """, (lru_id, 1))
                        serial_id = cur.fetchone()[0]
                except Exception as e:
                    print(f"    Warning: Could not determine serial_id: {e}")
                    serial_id = 1
            
            # Create the report
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
                    lru_sru_desc,  # inspection_stage
                    memo[14],      # memo_date as date_of_review
                    venue,         # review_venue
                    'ASSIGNED',    # status
                    datetime.now() # created_at
                ))
                
                report_id = cur.fetchone()[0]
                reports_created += 1
                print(f"  ✓ Created report ID: {report_id}")
                print(f"    Project ID: {project_id}, LRU ID: {lru_id}, Serial ID: {serial_id}")
                
            except Exception as e:
                print(f"  ✗ Error creating report for memo {memo_id}: {e}")
                continue
        
        # Commit all changes
        conn.commit()
        print(f"\n✓ Successfully created {reports_created} reports")
        
        # Verify the results
        cur.execute("""
            SELECT COUNT(*) 
            FROM reports r
            JOIN memos m ON r.memo_id = m.memo_id
            WHERE m.memo_status = 'assigned'
        """)
        total_reports = cur.fetchone()[0]
        print(f"Total reports for assigned memos: {total_reports}")
        
        cur.close()
        
    except Exception as e:
        print(f"Error: {str(e)}")
        if conn:
            conn.rollback()
    finally:
        if conn:
            conn.close()

if __name__ == "__main__":
    create_reports_for_assigned_memos()
