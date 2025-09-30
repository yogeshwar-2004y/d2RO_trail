-- Updated database trigger to create reports only for accepted memos
-- This ensures that reports are created only when memos are both assigned AND accepted

-- Drop the existing trigger and function
DROP TRIGGER IF EXISTS trigger_create_report_on_memo_assigned ON memos;
DROP FUNCTION IF EXISTS create_report_for_assigned_memo();

-- Create updated function that checks both memo status and approval status
CREATE OR REPLACE FUNCTION create_report_for_accepted_memo()
RETURNS TRIGGER AS $$
DECLARE
    default_project_id INTEGER := 1;
    default_lru_id INTEGER := 1;
    default_serial_id INTEGER := 1;
    memo_project_id INTEGER;
    memo_lru_id INTEGER;
    memo_serial_id INTEGER;
    approval_status TEXT;
BEGIN
    -- Only proceed if the memo status is being changed to 'assigned'
    IF NEW.memo_status = 'assigned' AND (OLD.memo_status IS NULL OR OLD.memo_status != 'assigned') THEN
        
        -- Check if there's an approval record with 'accepted' status
        SELECT status INTO approval_status
        FROM memo_approval 
        WHERE memo_id = NEW.memo_id AND status = 'accepted';
        
        -- Only create report if memo is accepted (not just assigned)
        IF approval_status IS NULL THEN
            RAISE NOTICE 'Memo % is assigned but not accepted, skipping report creation', NEW.memo_id;
            RETURN NEW;
        END IF;
        
        -- Check if report already exists for this memo
        IF EXISTS (SELECT 1 FROM reports WHERE memo_id = NEW.memo_id) THEN
            RAISE NOTICE 'Report already exists for memo %, skipping', NEW.memo_id;
            RETURN NEW;
        END IF;
        
        -- Try to determine project_id based on wing_proj_ref_no
        SELECT project_id INTO memo_project_id
        FROM projects 
        WHERE LOWER(project_name) = ANY(
            SELECT LOWER(unnest(string_to_array(NEW.wing_proj_ref_no, '/')))
        )
        LIMIT 1;
        
        IF memo_project_id IS NULL THEN
            memo_project_id := default_project_id;
        END IF;
        
        -- Try to determine lru_id based on lru_sru_desc
        SELECT lru_id INTO memo_lru_id
        FROM lrus 
        WHERE LOWER(lru_name) = LOWER(NEW.lru_sru_desc)
        LIMIT 1;
        
        IF memo_lru_id IS NULL THEN
            memo_lru_id := default_lru_id;
        END IF;
        
        -- Determine serial_id
        SELECT serial_id INTO memo_serial_id
        FROM serial_numbers 
        WHERE lru_id = memo_lru_id 
        ORDER BY serial_id 
        LIMIT 1;
        
        IF memo_serial_id IS NULL THEN
            -- Create a new serial number entry
            INSERT INTO serial_numbers (lru_id, serial_number)
            VALUES (memo_lru_id, 1)
            RETURNING serial_id INTO memo_serial_id;
        END IF;
        
        -- Create the report
        INSERT INTO reports (
            memo_id, 
            project_id, 
            lru_id, 
            serial_id,
            inspection_stage, 
            date_of_review, 
            review_venue,
            status, 
            created_at
        ) VALUES (
            NEW.memo_id,
            memo_project_id,
            memo_lru_id,
            memo_serial_id,
            NEW.lru_sru_desc,  -- inspection_stage
            NEW.memo_date,     -- date_of_review
            NEW.venue,         -- review_venue
            'ASSIGNED',        -- status
            NOW()              -- created_at
        );
        
        RAISE NOTICE 'Report created automatically for accepted memo %', NEW.memo_id;
        
    END IF;
    
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Create the updated trigger
CREATE TRIGGER trigger_create_report_on_memo_accepted
    AFTER UPDATE ON memos
    FOR EACH ROW
    EXECUTE FUNCTION create_report_for_accepted_memo();

-- Add comment for documentation
COMMENT ON FUNCTION create_report_for_accepted_memo() IS 'Automatically creates a report when a memo status changes to assigned AND the memo has been accepted';
COMMENT ON TRIGGER trigger_create_report_on_memo_accepted ON memos IS 'Triggers report creation when memo is assigned and accepted';
