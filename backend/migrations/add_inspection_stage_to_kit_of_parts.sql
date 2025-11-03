-- Add inspection_stage column to kit_of_parts_inspection_report table
ALTER TABLE public.kit_of_parts_inspection_report
ADD COLUMN IF NOT EXISTS inspection_stage text COLLATE pg_catalog."default";