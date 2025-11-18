-- Migration: Create trigger to sync report status when memo status changes
-- Date: 2025-01-XX
-- Description: Automatically updates report status when corresponding memo status changes

-- Drop existing trigger and function if they exist
DROP TRIGGER IF EXISTS trigger_sync_report_status_on_memo_status_change ON memos;
DROP FUNCTION IF EXISTS sync_report_status_on_memo_status_change();

-- Create function to sync report status
CREATE OR REPLACE FUNCTION sync_report_status_on_memo_status_change()
RETURNS TRIGGER AS $$
DECLARE
    report_status TEXT;
BEGIN
    -- Only proceed if memo_status has changed
    IF NEW.memo_status = OLD.memo_status THEN
        RETURN NEW;
    END IF;
    
    -- Map memo status to report status
    CASE NEW.memo_status
        WHEN 'assigned' THEN
            report_status := 'ASSIGNED';
        WHEN 'successfully_completed' THEN
            report_status := 'SUCCESSFULLY COMPLETED';
        WHEN 'completed_with_observations' THEN
            report_status := 'COMPLETED WITH OBSERVATIONS';
        WHEN 'test_failed' THEN
            report_status := 'TEST FAILED';
        WHEN 'test_not_conducted' THEN
            report_status := 'TEST NOT CONDUCTED';
        ELSE
            -- For other statuses (rejected, not_assigned, etc.), don't update report
            RETURN NEW;
    END CASE;
    
    -- Update corresponding report status (one-to-one relationship)
    UPDATE reports 
    SET status = report_status
    WHERE memo_id = NEW.memo_id;
    
    -- Log if report was updated
    IF FOUND THEN
        RAISE NOTICE 'Updated report status to % for memo %', report_status, NEW.memo_id;
    END IF;
    
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Create the trigger
CREATE TRIGGER trigger_sync_report_status_on_memo_status_change
    AFTER UPDATE OF memo_status ON memos
    FOR EACH ROW
    WHEN (NEW.memo_status IS DISTINCT FROM OLD.memo_status)
    EXECUTE FUNCTION sync_report_status_on_memo_status_change();

-- Add comment for documentation
COMMENT ON FUNCTION sync_report_status_on_memo_status_change() IS 'Automatically syncs report status when memo status changes';
COMMENT ON TRIGGER trigger_sync_report_status_on_memo_status_change ON memos IS 'Triggers report status sync when memo status is updated';

