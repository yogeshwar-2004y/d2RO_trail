"""
News updates management routes
"""
from flask import Blueprint, request, jsonify
from config import get_db_connection
from utils.helpers import handle_database_error

news_bp = Blueprint('news', __name__)

# @news_bp.route('/api/news/debug', methods=['GET'])
# def debug_news():
#     """Debug endpoint to check news data and timing"""
#     try:
#         conn = get_db_connection()
#         conn.rollback()
#         cur = conn.cursor()
        
#         # Get current time
#         cur.execute("SELECT NOW()")
#         current_time = cur.fetchone()[0]
        
#         # Get all news records
#         cur.execute("SELECT id, news_text, created_at, updated_at, hidden FROM news_updates ORDER BY id")
#         all_news = cur.fetchall()
        
#         # Get news within 24 hours
#         cur.execute("""
#             SELECT id, news_text, created_at, updated_at, hidden
#             FROM news_updates
#             WHERE updated_at >= NOW() - INTERVAL '24 hours'
#             AND (hidden = FALSE OR hidden IS NULL)
#             ORDER BY updated_at DESC
#         """)
#         recent_news = cur.fetchall()
        
#         cur.close()
        
#         return jsonify({
#             "success": True,
#             "current_time": current_time.isoformat(),
#             "all_news": [
#                 {
#                     "id": item[0],
#                     "news_text": item[1],
#                     "created_at": item[2].isoformat() if item[2] else None,
#                     "updated_at": item[3].isoformat() if item[3] else None,
#                     "hidden": item[4]
#                 } for item in all_news
#             ],
#             "recent_news": [
#                 {
#                     "id": item[0],
#                     "news_text": item[1],
#                     "created_at": item[2].isoformat() if item[2] else None,
#                     "updated_at": item[3].isoformat() if item[3] else None,
#                     "hidden": item[4]
#                 } for item in recent_news
#             ]
#         })
        
#     except Exception as e:
#         conn.rollback()
#         print(f"Error in debug endpoint: {str(e)}")
#         return jsonify({"success": False, "message": "Internal server error"}), 500

@news_bp.route('/api/news', methods=['GET'])
def get_news():
    """Get news updates for frontend display (all non-hidden news)"""
    try:
        conn = get_db_connection()
        conn.rollback()  # Clear any previous transaction errors
        cur = conn.cursor()
        
        cur.execute("""
            SELECT id, news_text, created_at, updated_at, hidden
            FROM news_updates
            WHERE hidden IS NULL OR hidden = FALSE
            ORDER BY updated_at DESC
        """)
        
        news = cur.fetchall()
        cur.close()
        
        news_list = []
        # print("Fetched news items:", news)
        for item in news:
            news_list.append({
                "id": item[0],
                "news_text": item[1],
                "created_at": item[2].isoformat() if item[2] else None,
                "updated_at": item[3].isoformat() if item[3] else None,
                "hidden": item[4]
            })
        # print(news_list)
        return jsonify({
            "success": True,
            "news": news_list
        })
        
    except Exception as e:
        conn.rollback()
        print(f"Error getting news: {str(e)}")
        return jsonify({"success": False, "message": "Internal server error"}), 500

@news_bp.route('/api/news/all', methods=['GET'])
def get_all_news():
    """Get all news updates for management interface"""
    try:
        conn = get_db_connection()
        conn.rollback()
        cur = conn.cursor()
        
        cur.execute("""
            SELECT id, news_text, created_at, updated_at, hidden
            FROM news_updates
            ORDER BY updated_at DESC
        """)
        
        news = cur.fetchall()
        cur.close()
        
        news_list = []
        for item in news:
            news_list.append({
                "id": item[0],
                "news_text": item[1],
                "created_at": item[2].isoformat() if item[2] else None,
                "updated_at": item[3].isoformat() if item[3] else None,
                "hidden": item[4]
            })
        
        return jsonify({
            "success": True,
            "news": news_list
        })
        
    except Exception as e:
        conn.rollback()
        print(f"Error getting all news: {str(e)}")
        return jsonify({"success": False, "message": "Internal server error"}), 500

@news_bp.route('/api/news', methods=['POST'])
def create_news():
    """Create multiple news updates"""
    try:
        data = request.json
        if not data or 'news_items' not in data:
            return jsonify({"success": False, "message": "No news items provided"}), 400
        
        news_items = data['news_items']
        if not news_items:
            return jsonify({"success": False, "message": "News items list is empty"}), 400
        
        conn = get_db_connection()
        cur = conn.cursor()
        
        # Insert each news item
        inserted_ids = []
        for item in news_items:
            if 'news_text' not in item:
                cur.close()
                return jsonify({"success": False, "message": "Missing news_text field in news item"}), 400
            
            if not item['news_text'].strip():
                cur.close()
                return jsonify({"success": False, "message": "News text cannot be empty"}), 400
            
            cur.execute("""
                INSERT INTO news_updates (news_text)
                VALUES (%s)
                RETURNING id
            """, (item['news_text'].strip(),))
            
            inserted_id = cur.fetchone()[0]
            inserted_ids.append(inserted_id)
        
        conn.commit()
        cur.close()
        
        return jsonify({
            "success": True,
            "message": f"Successfully created {len(inserted_ids)} news items",
            "inserted_ids": inserted_ids
        })
        
    except Exception as e:
        return handle_database_error(get_db_connection(), f"Error creating news: {str(e)}")

@news_bp.route('/api/news/<int:news_id>', methods=['DELETE'])
def delete_news_item(news_id):
    """Hide a single news item from frontend display (soft delete)"""
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        
        # Check if news item exists
        cur.execute("SELECT id FROM news_updates WHERE id = %s", (news_id,))
        if not cur.fetchone():
            cur.close()
            return jsonify({"success": False, "message": "News item not found"}), 404
        
        # Hide the news item (soft delete)
        cur.execute("UPDATE news_updates SET hidden = TRUE WHERE id = %s", (news_id,))
        
        conn.commit()
        cur.close()
        
        return jsonify({
            "success": True,
            "message": "News item hidden successfully"
        })
        
    except Exception as e:
        return handle_database_error(get_db_connection(), f"Error hiding news item: {str(e)}")

@news_bp.route('/api/news/<int:news_id>/permanent', methods=['DELETE'])
def permanently_delete_news_item(news_id):
    """Permanently delete a single news item (hard delete from management)"""
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        
        # Check if news item exists
        cur.execute("SELECT id FROM news_updates WHERE id = %s", (news_id,))
        if not cur.fetchone():
            cur.close()
            return jsonify({"success": False, "message": "News item not found"}), 404
        
        # Delete the news item permanently
        cur.execute("DELETE FROM news_updates WHERE id = %s", (news_id,))
        
        conn.commit()
        cur.close()
        
        return jsonify({
            "success": True,
            "message": "News item deleted permanently"
        })
        
    except Exception as e:
        return handle_database_error(get_db_connection(), f"Error deleting news item permanently: {str(e)}")

@news_bp.route('/api/news/<int:news_id>/repost', methods=['PUT'])
def repost_news_item(news_id):
    """Repost a news item by updating its timestamp and making it visible"""
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        
        # Check if news item exists
        cur.execute("SELECT id FROM news_updates WHERE id = %s", (news_id,))
        if not cur.fetchone():
            cur.close()
            return jsonify({"success": False, "message": "News item not found"}), 404
        
        # Update the news item: set updated_at to current time and make it visible
        cur.execute("""
            UPDATE news_updates 
            SET updated_at = NOW(), hidden = FALSE 
            WHERE id = %s
        """, (news_id,))
        
        conn.commit()
        cur.close()
        
        return jsonify({
            "success": True,
            "message": "News item reposted successfully"
        })
        
    except Exception as e:
        return handle_database_error(get_db_connection(), f"Error reposting news item: {str(e)}")

@news_bp.route('/api/news/all', methods=['DELETE'])
def delete_all_news():
    """Hide all visible news updates from frontend display"""
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        
        # Count visible news items
        cur.execute("""
            SELECT COUNT(*) FROM news_updates 
            WHERE hidden = FALSE
        """)
        count = cur.fetchone()[0]
        
        if count == 0:
            cur.close()
            return jsonify({"success": False, "message": "No visible news items to hide"}), 400
        
        # Hide all visible news items
        cur.execute("""
            UPDATE news_updates 
            SET hidden = TRUE 
            WHERE hidden = FALSE
        """)
        
        conn.commit()
        cur.close()
        
        return jsonify({
            "success": True,
            "message": f"Successfully hidden {count} news items"
        })
        
    except Exception as e:
        return handle_database_error(get_db_connection(), f"Error hiding all news: {str(e)}")

@news_bp.route('/api/news/permanent/all', methods=['DELETE'])
def permanently_delete_all_news():
    """Permanently delete all news updates (hard delete from management)"""
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        
        # Count existing news items
        cur.execute("SELECT COUNT(*) FROM news_updates")
        count = cur.fetchone()[0]
        
        if count == 0:
            cur.close()
            return jsonify({"success": False, "message": "No news items to delete"}), 400
        
        # Delete all news items permanently
        cur.execute("DELETE FROM news_updates")
        
        conn.commit()
        cur.close()
        
        return jsonify({
            "success": True,
            "message": f"Successfully deleted {count} news items permanently"
        })
        
    except Exception as e:
        return handle_database_error(get_db_connection(), f"Error deleting all news permanently: {str(e)}")
