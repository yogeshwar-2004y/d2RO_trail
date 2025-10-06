-- Migration to add signature_password field to users table
-- This field will store the hashed name of the user as default signature password

-- Add the signature_password column to users table
ALTER TABLE users ADD COLUMN signature_password VARCHAR(64);

-- Update existing users to have their name as the default signature password (hashed)
-- Using SHA-256 hash of the user's name
UPDATE users SET signature_password = encode(sha256(name::bytea), 'hex') WHERE signature_password IS NULL;

-- Make the column NOT NULL after setting default values
ALTER TABLE users ALTER COLUMN signature_password SET NOT NULL;

-- Add a comment to document the purpose of this field
COMMENT ON COLUMN users.signature_password IS 'Hashed signature password, defaults to SHA-256 hash of user name';
