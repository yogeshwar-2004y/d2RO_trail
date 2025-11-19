-- Migration to add lru_part_number field to lrus table
-- This field will store LRU part numbers that can contain a mix of numbers, text, and symbols

-- Add the lru_part_number column to lrus table
-- Using VARCHAR to support mix of numbers, text, and symbols
ALTER TABLE lrus ADD COLUMN IF NOT EXISTS lru_part_number VARCHAR(100);

-- Add a comment to document the purpose of this field
COMMENT ON COLUMN lrus.lru_part_number IS 'LRU Part Number - supports mix of numbers, text, and symbols (e.g., ABC-123-XYZ, 456/789, etc.)';

