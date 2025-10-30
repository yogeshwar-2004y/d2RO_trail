"""
File upload and serving routes
"""
import os
from flask import Blueprint, request, jsonify, send_file
from config import get_db_connection, Config
from utils.helpers import allowed_image_file, validate_file_size, create_upload_directories

files_bp = Blueprint('files', __name__)

@files_bp.route('/api/files/plan-documents/<path:filename>', methods=['GET'])
def serve_plan_document(filename):
    """Serve uploaded plan document files"""
    try:
        print(f"📁 Request to serve file: {filename}")
        print(f"📂 Upload folder: {Config.UPLOAD_FOLDER}")
        
        # Clean the filename - remove any path separators
        clean_filename = os.path.basename(filename)
        file_path = os.path.join(Config.UPLOAD_FOLDER, clean_filename)
        
        print(f"🔍 Looking for file at: {file_path}")
        print(f"📄 File exists: {os.path.exists(file_path)}")
        
        if os.path.exists(file_path):
            print(f"📊 File size: {os.path.getsize(file_path)} bytes")
        
        # List files in upload directory for debugging
        try:
            files_in_dir = os.listdir(Config.UPLOAD_FOLDER)
            print(f"📋 Files in upload directory: {files_in_dir}")
        except Exception as list_error:
            print(f"❌ Error listing directory: {list_error}")
        
        # Security check - ensure file is within upload directory
        abs_upload_folder = os.path.abspath(Config.UPLOAD_FOLDER)
        abs_file_path = os.path.abspath(file_path)
        
        if not abs_file_path.startswith(abs_upload_folder):
            print(f"🚫 Security violation: File path outside upload directory")
            return jsonify({"success": False, "message": "Invalid file path"}), 403
        
        if not os.path.exists(file_path):
            print(f"❌ File not found: {file_path}")
            return jsonify({"success": False, "message": f"File not found: {clean_filename}"}), 404
        
        print(f"✅ Serving file: {file_path}")
        return send_file(file_path, as_attachment=False)
        
    except Exception as e:
        print(f"❌ Error serving file {filename}: {str(e)}")
        return jsonify({"success": False, "message": f"Error serving file: {str(e)}"}), 500

@files_bp.route('/api/upload-login-background', methods=['POST'])
def upload_login_background():
    """Upload login background image"""
    try:
        if 'background_image' not in request.files:
            return jsonify({"success": False, "message": "No file provided"}), 400
        
        file = request.files['background_image']
        
        if file.filename == '':
            return jsonify({"success": False, "message": "No file selected"}), 400
        
        if not allowed_image_file(file.filename):
            return jsonify({"success": False, "message": "Invalid file type. Only PNG, JPG, and JPEG files are allowed"}), 400
        
        # Check file size
        if not validate_file_size(file, Config.MAX_IMAGE_SIZE):
            return jsonify({"success": False, "message": "File size too large. Maximum size is 10MB"}), 400
        
        # Generate unique filename
        file_extension = file.filename.rsplit('.', 1)[1].lower()
        unique_filename = f"login_background.{file_extension}"
        file_path = os.path.join(Config.LOGIN_BACKGROUND_FOLDER, unique_filename)
        
        # Remove existing background files
        if os.path.exists(Config.LOGIN_BACKGROUND_FOLDER):
            for existing_file in os.listdir(Config.LOGIN_BACKGROUND_FOLDER):
                if existing_file.startswith('login_background.'):
                    os.remove(os.path.join(Config.LOGIN_BACKGROUND_FOLDER, existing_file))
        
        # Save new file
        file.save(file_path)
        
        # Return the URL for the uploaded background
        background_url = f"http://127.0.0.1:8000/api/login-background/{unique_filename}"
        
        return jsonify({
            "success": True,
            "message": "Background uploaded successfully",
            "background_url": background_url
        })
        
    except Exception as e:
        print(f"Upload error: {str(e)}")
        return jsonify({"success": False, "message": f"Upload error: {str(e)}"}), 500

@files_bp.route('/api/login-background/<filename>')
def serve_login_background(filename):
    """Serve login background images"""
    try:
        file_path = os.path.join(Config.LOGIN_BACKGROUND_FOLDER, filename)
        if os.path.exists(file_path):
            return send_file(file_path)
        else:
            # Fallback to default background
            default_path = os.path.join('..', 'frontend', 'src', 'assets', 'images', 'login-background.png')
            if os.path.exists(default_path):
                return send_file(default_path)
            return jsonify({"success": False, "message": "Background not found"}), 404
    except Exception as e:
        print(f"Serve background error: {str(e)}")
        return jsonify({"success": False, "message": f"Error serving background: {str(e)}"}), 500

@files_bp.route('/api/get-current-background')
def get_current_background():
    """Get current login background URL"""
    try:
        # Check if custom background exists
        for ext in Config.ALLOWED_IMAGE_EXTENSIONS:
            custom_background = os.path.join(Config.LOGIN_BACKGROUND_FOLDER, f"login_background.{ext}")
            if os.path.exists(custom_background):
                background_url = f"http://127.0.0.1:8000/api/login-background/login_background.{ext}"
                return jsonify({
                    "success": True,
                    "background_url": background_url,
                    "is_custom": True
                })
        
        # Return default background URL
        return jsonify({
            "success": True,
            "background_url": "/src/assets/images/login-background.png",
            "is_custom": False
        })
        
    except Exception as e:
        print(f"Get background error: {str(e)}")
        return jsonify({"success": False, "message": f"Error getting background: {str(e)}"}), 500

@files_bp.route('/api/reset-login-background', methods=['POST'])
def reset_login_background():
    """Reset login background to default"""
    try:
        # Remove all custom background files
        if os.path.exists(Config.LOGIN_BACKGROUND_FOLDER):
            for existing_file in os.listdir(Config.LOGIN_BACKGROUND_FOLDER):
                if existing_file.startswith('login_background.'):
                    os.remove(os.path.join(Config.LOGIN_BACKGROUND_FOLDER, existing_file))
        
        return jsonify({
            "success": True,
            "message": "Background reset to default successfully"
        })
        
    except Exception as e:
        print(f"Reset background error: {str(e)}")
        return jsonify({"success": False, "message": f"Error resetting background: {str(e)}"}), 500

@files_bp.route('/api/upload-gallery-image/<int:image_number>', methods=['POST'])
def upload_gallery_image(image_number):
    """Upload a specific gallery image (1-5)"""
    try:
        if image_number < 1 or image_number > 5:
            return jsonify({"success": False, "message": "Image number must be between 1 and 5"}), 400
        
        if 'image' not in request.files:
            return jsonify({"success": False, "message": "No file provided"}), 400
        
        file = request.files['image']
        
        if file.filename == '':
            return jsonify({"success": False, "message": "No file selected"}), 400
        
        if not allowed_image_file(file.filename):
            return jsonify({"success": False, "message": "Invalid file type. Only PNG, JPG, and JPEG files are allowed"}), 400
        
        # Check file size
        if not validate_file_size(file, Config.MAX_IMAGE_SIZE):
            return jsonify({"success": False, "message": "File size too large. Maximum size is 10MB"}), 400
        
        # Ensure directory exists
        create_upload_directories()
        
        # Generate filename
        file_extension = file.filename.rsplit('.', 1)[1].lower()
        filename = f"gallery_image_{image_number}.{file_extension}"
        file_path = os.path.join(Config.LOGIN_BACKGROUND_FOLDER, filename)
        
        # Remove existing file for this image number
        if os.path.exists(Config.LOGIN_BACKGROUND_FOLDER):
            for existing_file in os.listdir(Config.LOGIN_BACKGROUND_FOLDER):
                if existing_file.startswith(f'gallery_image_{image_number}.'):
                    os.remove(os.path.join(Config.LOGIN_BACKGROUND_FOLDER, existing_file))
        
        # Save new file
        file.save(file_path)
        
        # Return the URL for the uploaded image
        image_url = f"http://127.0.0.1:5000/api/gallery-image/{filename}"
        
        return jsonify({
            "success": True,
            "message": f"Gallery image {image_number} uploaded successfully",
            "image_url": image_url
        })
        
    except Exception as e:
        print(f"Upload gallery image error: {str(e)}")
        return jsonify({"success": False, "message": f"Upload error: {str(e)}"}), 500

@files_bp.route('/api/gallery-image/<filename>')
def serve_gallery_image(filename):
    """Serve gallery images"""
    try:
        file_path = os.path.join(Config.LOGIN_BACKGROUND_FOLDER, filename)
        if os.path.exists(file_path):
            return send_file(file_path)
        else:
            return jsonify({"success": False, "message": "Image not found"}), 404
    except Exception as e:
        print(f"Serve gallery image error: {str(e)}")
        return jsonify({"success": False, "message": f"Error serving image: {str(e)}"}), 500

@files_bp.route('/api/get-gallery-images')
def get_gallery_images():
    """Get current gallery images URLs"""
    try:
        gallery_images = {}
        
        # Check if custom gallery images exist
        if os.path.exists(Config.LOGIN_BACKGROUND_FOLDER):
            for image_num in range(1, 6):
                for ext in Config.ALLOWED_IMAGE_EXTENSIONS:
                    custom_image = os.path.join(Config.LOGIN_BACKGROUND_FOLDER, f"gallery_image_{image_num}.{ext}")
                    if os.path.exists(custom_image):
                        gallery_images[f'image_{image_num}'] = f"http://127.0.0.1:5000/api/gallery-image/gallery_image_{image_num}.{ext}"
                        break
                # If no custom image found, store empty string to indicate default should be used
                if f'image_{image_num}' not in gallery_images:
                    gallery_images[f'image_{image_num}'] = ""
        
        return jsonify({
            "success": True,
            "gallery_images": gallery_images
        })
        
    except Exception as e:
        print(f"Get gallery images error: {str(e)}")
        return jsonify({"success": False, "message": f"Error getting gallery images: {str(e)}"}), 500

@files_bp.route('/api/reset-gallery-image/<int:image_number>', methods=['POST'])
def reset_gallery_image(image_number):
    """Reset a specific gallery image to default"""
    try:
        if image_number < 1 or image_number > 5:
            return jsonify({"success": False, "message": "Image number must be between 1 and 5"}), 400
        
        # Remove existing file for this image number
        if os.path.exists(Config.LOGIN_BACKGROUND_FOLDER):
            for existing_file in os.listdir(Config.LOGIN_BACKGROUND_FOLDER):
                if existing_file.startswith(f'gallery_image_{image_number}.'):
                    os.remove(os.path.join(Config.LOGIN_BACKGROUND_FOLDER, existing_file))
        
        return jsonify({
            "success": True,
            "message": f"Gallery image {image_number} reset to default successfully"
        })
        
    except Exception as e:
        print(f"Reset gallery image error: {str(e)}")
        return jsonify({"success": False, "message": f"Error resetting gallery image: {str(e)}"}), 500
