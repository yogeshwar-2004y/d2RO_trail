-- Database trigger to automatically create reports when memo status changes to 'assigned'
-- This ensures that reports are created automatically for any memo that gets assigned

-- First, create a function that will be called by the trigger
CREATE OR REPLACE FUNCTION create_report_for_assigned_memo()
RETURNS TRIGGER AS $$
DECLARE
    default_project_id INTEGER := 1;
    default_lru_id INTEGER := 1;
    default_serial_id INTEGER := 1;
    memo_project_id INTEGER;
    memo_lru_id INTEGER;
    memo_serial_id INTEGER;
BEGIN
    -- Only proceed if the memo status is being changed to 'assigned'
    IF NEW.memo_status = 'assigned' AND (OLD.memo_status IS NULL OR OLD.memo_status != 'assigned') THEN
        
        -- Check if report already exists for this memo
        IF EXISTS (SELECT 1 FROM reports WHERE memo_id = NEW.memo_id) THEN
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
        
        RAISE NOTICE 'Report created automatically for memo %', NEW.memo_id;
        
    END IF;
    
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Create the trigger that calls the function
DROP TRIGGER IF EXISTS trigger_create_report_on_memo_assigned ON memos;

CREATE TRIGGER trigger_create_report_on_memo_assigned
    AFTER UPDATE ON memos
    FOR EACH ROW
    EXECUTE FUNCTION create_report_for_assigned_memo();

-- Add comment for documentation
COMMENT ON FUNCTION create_report_for_assigned_memo() IS 'Automatically creates a report when a memo status changes to assigned';
COMMENT ON TRIGGER trigger_create_report_on_memo_assigned ON memos IS 'Triggers report creation when memo is assigned';
