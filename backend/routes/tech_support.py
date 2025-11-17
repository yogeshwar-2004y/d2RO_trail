"""
Tech support management routes
"""
from flask import Blueprint, request, jsonify, Response
from config import get_db_connection
from utils.helpers import handle_database_error
from utils.activity_logger import log_activity, log_notification, get_users_by_role
from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas
import io
import os

tech_support_bp = Blueprint('tech_support', __name__)

@tech_support_bp.route('/api/tech-support', methods=['POST'])
def submit_tech_support():
    """Submit a tech support request"""
    try:
        data = request.json
        if not data:
            return jsonify({"success": False, "message": "No data provided"}), 400
        
        # Validate required fields
        required_fields = ['username', 'userId', 'date', 'issue']
        for field in required_fields:
            if not data.get(field):
                return jsonify({"success": False, "message": f"Missing required field: {field}"}), 400
        
        # Validate user_id is a valid integer
        try:
            user_id = int(data['userId'])
        except (ValueError, TypeError):
            return jsonify({"success": False, "message": "User ID must be a valid number"}), 400
        
        conn = get_db_connection()
        cur = conn.cursor()
        
        # Create tech_support_requests table if it doesn't exist
        cur.execute("""
            CREATE TABLE IF NOT EXISTS tech_support_requests (
                id SERIAL PRIMARY KEY,
                username VARCHAR(255) NOT NULL,
                user_id INTEGER NOT NULL,
                issue_date DATE NOT NULL,
                issue_description TEXT NOT NULL,
                status VARCHAR(50) DEFAULT 'pending',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                status_updated_by INTEGER,
                status_updated_at TIMESTAMP
            )
        """)
        
        # Check for duplicate requests (same user, same date, same issue)
        cur.execute("""
            SELECT id, status FROM tech_support_requests 
            WHERE username = %s AND user_id = %s AND issue_date = %s AND issue_description = %s
            ORDER BY created_at DESC
            LIMIT 1
        """, (data['username'], str(user_id), data['date'], data['issue']))
        
        existing_request = cur.fetchone()
        
        if existing_request:
            # Request already exists, return existing request info
            return jsonify({
                "success": True,
                "message": "Request already exists",
                "existing_request_id": existing_request[0],
                "existing_status": existing_request[1],
                "duplicate": True
            })
        
        # Insert the tech support request
        cur.execute("""
            INSERT INTO tech_support_requests (username, user_id, issue_date, issue_description)
            VALUES (%s, %s, %s, %s)
            RETURNING id
        """, (
            data['username'],
            str(user_id),  # Convert to string to match database type
            data['date'],
            data['issue']
        ))
        
        request_id = cur.fetchone()[0]
        
        conn.commit()
        cur.close()
        
        # Log the activity
        try:
            log_activity(
                project_id=None,
                activity_performed="TECH_SUPPORT_REQUEST",
                performed_by=user_id,
                additional_info=f"Tech support request submitted by {data['username']} (User ID: {data['userId']})"
            )
        except Exception as log_error:
            print(f"Warning: Failed to log activity: {str(log_error)}")
            # Continue execution even if logging fails
        
        # Send notifications to all admins
        try:
            admins = get_users_by_role(1)  # role_id = 1 for Admin
            for admin in admins:
                log_notification(
                    project_id=None,
                    activity_performed="New Tech Support Request",
                    performed_by=user_id,
                    notified_user_id=admin['user_id'],
                    notification_type="tech_support_request",
                    additional_info=f"New tech support request #{request_id} from {data['username']} (User ID: {data['userId']}). Issue: {data['issue'][:100]}{'...' if len(data['issue']) > 100 else ''}"
                )
        except Exception as notification_error:
            print(f"Warning: Failed to send notifications: {str(notification_error)}")
            # Continue execution even if notifications fail
        
        return jsonify({
            "success": True,
            "message": "Tech support request submitted successfully"
        })
        
    except Exception as e:
        if 'conn' in locals():
            conn.rollback()
        print(f"Error submitting tech support request: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({"success": False, "message": f"Internal server error: {str(e)}"}), 500

@tech_support_bp.route('/api/tech-support/user/<user_id>', methods=['GET'])
def get_user_tech_support_requests(user_id):
    """Get tech support requests for a specific user"""
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        
        cur.execute("""
            SELECT id, username, user_id, issue_date, issue_description, 
                   status, created_at, updated_at, status_updated_by, status_updated_at
            FROM tech_support_requests
            WHERE user_id = %s
            ORDER BY created_at DESC
        """, (user_id,))
        
        requests = cur.fetchall()
        cur.close()
        
        request_list = []
        for req in requests:
            request_list.append({
                "id": req[0],
                "username": req[1],
                "user_id": req[2],
                "issue_date": req[3].isoformat() if req[3] else None,
                "issue_description": req[4],
                "status": req[5],
                "created_at": req[6].isoformat() if req[6] else None,
                "updated_at": req[7].isoformat() if req[7] else None,
                "status_updated_by": req[8],
                "status_updated_at": req[9].isoformat() if req[9] else None
            })
        
        return jsonify({
            "success": True,
            "requests": request_list,
            "total_count": len(request_list)
        })
        
    except Exception as e:
        print(f"Error fetching user tech support requests: {str(e)}")
        return jsonify({"success": False, "message": "Internal server error"}), 500

@tech_support_bp.route('/api/tech-support', methods=['GET'])
def get_tech_support_requests():
    """Get all tech support requests (admin only)"""
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        
        cur.execute("""
            SELECT id, username, user_id, issue_date, issue_description, 
                   status, created_at, updated_at, status_updated_by, status_updated_at
            FROM tech_support_requests
            ORDER BY created_at DESC
        """)
        
        requests = cur.fetchall()
        cur.close()
        
        request_list = []
        for req in requests:
            request_list.append({
                "id": req[0],
                "username": req[1],
                "user_id": req[2],
                "issue_date": req[3].isoformat() if req[3] else None,
                "issue_description": req[4],
                "status": req[5],
                "created_at": req[6].isoformat() if req[6] else None,
                "updated_at": req[7].isoformat() if req[7] else None,
                "status_updated_by": req[8],
                "status_updated_at": req[9].isoformat() if req[9] else None
            })
        
        return jsonify({
            "success": True,
            "requests": request_list
        })
        
    except Exception as e:
        print(f"Error fetching tech support requests: {str(e)}")
        return jsonify({"success": False, "message": "Internal server error"}), 500

@tech_support_bp.route('/api/tech-support/<int:request_id>/status', methods=['PUT'])
def update_tech_support_status(request_id):
    """Update tech support request status (admin only)"""
    try:
        data = request.json
        if not data or 'status' not in data:
            return jsonify({"success": False, "message": "Status is required"}), 400
        
        # Get admin user info from request headers or body
        admin_user_id = data.get('admin_user_id')
        if not admin_user_id:
            return jsonify({"success": False, "message": "Admin user ID is required"}), 400
        
        valid_statuses = ['pending', 'in_progress', 'resolved', 'closed']
        if data['status'] not in valid_statuses:
            return jsonify({"success": False, "message": "Invalid status"}), 400
        
        conn = get_db_connection()
        cur = conn.cursor()
        
        # Update the status with tracking information
        cur.execute("""
            UPDATE tech_support_requests 
            SET status = %s, 
                status_updated_by = %s,
                status_updated_at = CURRENT_TIMESTAMP,
                updated_at = CURRENT_TIMESTAMP
            WHERE id = %s
        """, (data['status'], admin_user_id, request_id))
        
        if cur.rowcount == 0:
            return jsonify({"success": False, "message": "Request not found"}), 404
        
        conn.commit()
        cur.close()
        
        # Log the activity
        try:
            log_activity(
                project_id=None,
                activity_performed="TECH_SUPPORT_STATUS_UPDATE",
                performed_by=admin_user_id,
                additional_info=f"Updated tech support request #{request_id} status to {data['status']}"
            )
        except Exception as log_error:
            print(f"Warning: Failed to log activity: {str(log_error)}")
        
        return jsonify({
            "success": True,
            "message": "Status updated successfully"
        })
        
    except Exception as e:
        if 'conn' in locals():
            conn.rollback()
        print(f"Error updating tech support status: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({"success": False, "message": f"Internal server error: {str(e)}"}), 500

@tech_support_bp.route('/api/tech-support/pdf', methods=['GET'])
def download_tech_support_pdf():
    """Generate and download tech support requests as PDF"""
    conn = None
    cur = None
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        
        # Get query parameters
        limit = request.args.get('limit', type=int)
        
        # Build query
        base_query = """
            SELECT id, username, user_id, issue_date, issue_description, 
                   status, created_at, updated_at, status_updated_by, status_updated_at
            FROM tech_support_requests
        """
        
        query_params = []
        if limit and limit > 0:
            base_query += " ORDER BY created_at DESC LIMIT %s"
            query_params.append(limit)
        else:
            base_query += " ORDER BY created_at DESC"
        
        cur.execute(base_query, tuple(query_params) if query_params else None)
        requests = cur.fetchall()
        
        cur.close()
        cur = None
        
        # Create PDF
        buffer = io.BytesIO()
        export_timestamp = datetime.now()
        
        # Define header and footer functions
        def add_header_footer(canvas_obj, doc_obj):
            """Add header and footer to each page"""
            canvas_obj.saveState()
            
            # Get page dimensions
            page_width, page_height = A4
            
            # Get the paths to logos
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            drdo_logo_path = os.path.join(base_dir, 'static', 'images', 'DRDO.png')
            aviatrax_logo_path = os.path.join(base_dir, 'static', 'images', 'Aviatrax_Trademark.png')
            
            # Header - DRDO Logo on left and AVIATRAX Trademark on right
            logo_size = 0.8 * inch  # Logo size
            
            # Draw DRDO logo on the left side if it exists
            if os.path.exists(drdo_logo_path):
                try:
                    canvas_obj.drawImage(drdo_logo_path, 50, page_height - 80, 
                                       width=logo_size, height=logo_size, 
                                       preserveAspectRatio=True, mask='auto')
                except Exception as e:
                    print(f"Error drawing DRDO logo: {str(e)}")
                    # If logo fails, continue without it
            
            # Draw AVIATRAX Trademark logo on the right side if it exists
            if os.path.exists(aviatrax_logo_path):
                try:
                    # Position on right side, parallel to DRDO logo
                    aviatrax_x = page_width - 50 - logo_size
                    canvas_obj.drawImage(aviatrax_logo_path, aviatrax_x, page_height - 80, 
                                       width=logo_size, height=logo_size, 
                                       preserveAspectRatio=True, mask='auto')
                except Exception as e:
                    print(f"Error drawing AVIATRAX trademark logo: {str(e)}")
                    # If logo fails, continue without it
            
            # AVIATRAX text next to DRDO logo
            text_start_x = 50 + logo_size + 15  # Start text after logo with some spacing
            canvas_obj.setFont("Helvetica-Bold", 18)
            # Purple color for AVIATRAX (#6A1B9A = RGB 106, 27, 154)
            canvas_obj.setFillColorRGB(106/255.0, 27/255.0, 154/255.0)
            canvas_obj.drawString(text_start_x, page_height - 40, "AVIATRAX™")
            
            canvas_obj.setFont("Helvetica", 10)
            canvas_obj.setFillColor(colors.black)
            canvas_obj.drawString(text_start_x, page_height - 55, "Defence Research and Development Org. (DRDO)")
            canvas_obj.drawString(text_start_x, page_height - 68, "Combat Aircraft Systems Development and Integration Centre")
            
            # Draw a line under header
            canvas_obj.setStrokeColor(colors.grey)
            canvas_obj.setLineWidth(1)
            canvas_obj.line(50, page_height - 85, page_width - 50, page_height - 85)
            
            # Footer - Export timestamp
            canvas_obj.setFont("Helvetica", 8)
            canvas_obj.setFillColor(colors.grey)
            footer_text = f"Exported on: {export_timestamp.strftime('%Y-%m-%d %H:%M:%S')}"
            text_width = canvas_obj.stringWidth(footer_text, "Helvetica", 8)
            canvas_obj.drawString((page_width - text_width) / 2, 30, footer_text)
            
            # Draw a line above footer
            canvas_obj.setStrokeColor(colors.grey)
            canvas_obj.setLineWidth(0.5)
            canvas_obj.line(50, 40, page_width - 50, 40)
            
            canvas_obj.restoreState()
        
        doc = SimpleDocTemplate(
            buffer, 
            pagesize=A4,
            rightMargin=50,
            leftMargin=50,
            topMargin=100,
            bottomMargin=60
        )
        story = []
        
        # Styles
        styles = getSampleStyleSheet()
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=16,
            spaceAfter=30,
            alignment=1  # Center alignment
        )
        
        # Create a style for wrapped text in cells
        cell_style = ParagraphStyle(
            'CellStyle',
            parent=styles['Normal'],
            fontSize=8,
            leading=10,
            alignment=0,  # Left align
            wordWrap='CJK'  # Enable word wrapping
        )
        
        # Title
        title = Paragraph("Tech Support Requests Report", title_style)
        story.append(title)
        story.append(Spacer(1, 12))
        
        # Date
        date_para = Paragraph(f"Generated on: {export_timestamp.strftime('%Y-%m-%d %H:%M:%S')}", styles['Normal'])
        story.append(date_para)
        story.append(Spacer(1, 20))
        
        # Table data
        table_data = [['ID', 'User', 'User ID', 'Issue Date', 'Issue Description', 'Status', 'Submitted']]
        
        # If no requests found, add a message row
        if not requests or len(requests) == 0:
            table_data.append(['No requests found', '', '', '', '', '', ''])
        else:
            for req in requests:
                # Format dates
                issue_date_str = 'N/A'
                if req[3]:  # issue_date
                    try:
                        if isinstance(req[3], str):
                            issue_date_str = datetime.fromisoformat(req[3].replace('Z', '+00:00')).strftime('%Y-%m-%d')
                        else:
                            issue_date_str = req[3].strftime('%Y-%m-%d')
                    except:
                        issue_date_str = str(req[3])
                
                created_at_str = 'N/A'
                if req[6]:  # created_at
                    try:
                        if isinstance(req[6], str):
                            created_at_str = datetime.fromisoformat(req[6].replace('Z', '+00:00')).strftime('%Y-%m-%d %H:%M:%S')
                        else:
                            created_at_str = req[6].strftime('%Y-%m-%d %H:%M:%S')
                    except:
                        created_at_str = str(req[6])
                
                # Escape special characters for issue description and create Paragraph for wrapping
                issue_desc = str(req[4] if req[4] else 'N/A')
                issue_desc_escaped = issue_desc.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
                issue_desc_para = Paragraph(issue_desc_escaped, cell_style)
                
                table_data.append([
                    str(req[0]),  # id
                    str(req[1] if req[1] else 'Unknown'),  # username
                    str(req[2] if req[2] else 'N/A'),  # user_id
                    issue_date_str,
                    issue_desc_para,  # issue description as Paragraph for wrapping
                    str(req[5] if req[5] else 'pending').upper(),  # status
                    created_at_str
                ])
        
        # Create table with column widths - adjusted to include issue description
        # Total: ID(0.5) + User(1.2) + UserID(0.7) + IssueDate(1.0) + IssueDesc(2.5) + Status(0.8) + Submitted(1.3) = 8.0 inches
        table = Table(table_data, colWidths=[0.5*inch, 1.2*inch, 0.7*inch, 1.0*inch, 2.5*inch, 0.8*inch, 1.3*inch])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, 0), 'CENTER'),  # Headers centered
            ('ALIGN', (0, 1), (0, -1), 'CENTER'),   # ID column centered
            ('ALIGN', (1, 1), (1, -1), 'LEFT'),     # User column left-aligned
            ('ALIGN', (2, 1), (2, -1), 'CENTER'),    # User ID column centered
            ('ALIGN', (3, 1), (3, -1), 'CENTER'),   # Issue Date column centered
            ('ALIGN', (4, 1), (4, -1), 'LEFT'),     # Issue Description column left-aligned
            ('ALIGN', (5, 1), (5, -1), 'CENTER'),   # Status column centered
            ('ALIGN', (6, 1), (6, -1), 'CENTER'),   # Submitted column centered
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('FONTSIZE', (0, 1), (-1, -1), 8),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),    # Changed to TOP for better wrapping
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.beige]),
            ('LEFTPADDING', (0, 0), (-1, -1), 4),
            ('RIGHTPADDING', (0, 0), (-1, -1), 4),
            ('TOPPADDING', (0, 0), (-1, -1), 6),
            ('BOTTOMPADDING', (0, 1), (-1, -1), 6),
        ]))
        
        story.append(table)
        
        # Build PDF with header and footer on all pages
        doc.build(story, onFirstPage=add_header_footer, onLaterPages=add_header_footer)
        
        buffer.seek(0)
        
        return Response(
            buffer.getvalue(),
            mimetype='application/pdf',
            headers={
                'Content-Disposition': f'attachment; filename=tech_support_requests_{export_timestamp.strftime("%Y%m%d_%H%M%S")}.pdf'
            }
        )
        
    except Exception as e:
        if cur:
            cur.close()
        if conn:
            conn.close()
        print(f"Error generating tech support PDF: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({"success": False, "message": f"Error generating PDF: {str(e)}"}), 500
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()