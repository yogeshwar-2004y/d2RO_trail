from flask import Blueprint, request, jsonify, Response
from config import get_db_connection
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas
from datetime import datetime
import io
import os

login_logs_bp = Blueprint('login_logs', __name__)

@login_logs_bp.route('/api/login-logs', methods=['GET'])
def get_login_logs():
    """Get login logs for admin dashboard"""
    conn = None
    cur = None
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        
        # Get query parameters
        limit = request.args.get('limit', 100, type=int)
        offset = request.args.get('offset', 0, type=int)
        
        # Check if suspicious activity columns exist
        cur.execute("""
            SELECT column_name 
            FROM information_schema.columns 
            WHERE table_name = 'login_logs' AND column_name = 'is_suspicious'
        """)
        has_suspicious_columns = cur.fetchone() is not None
        
        # Build query based on whether suspicious columns exist
        if has_suspicious_columns:
            query = """
                SELECT ll.serial_num, ll.user_id, ll.activity_performed, 
                       ll.performed_by, ll.timestamp,
                       COALESCE(u.name, 'Unknown User') as user_name, 
                       COALESCE(u.email, 'N/A') as user_email,
                       COALESCE(p.name, 'Unknown User') as performed_by_name,
                       COALESCE(ll.is_suspicious, FALSE) as is_suspicious,
                       ll.suspicion_reason
                FROM login_logs ll
                LEFT JOIN users u ON ll.user_id = u.user_id
                LEFT JOIN users p ON ll.performed_by = p.user_id
                ORDER BY ll.timestamp DESC
                LIMIT %s OFFSET %s
            """
        else:
            query = """
                SELECT ll.serial_num, ll.user_id, ll.activity_performed, 
                       ll.performed_by, ll.timestamp,
                       COALESCE(u.name, 'Unknown User') as user_name, 
                       COALESCE(u.email, 'N/A') as user_email,
                       COALESCE(p.name, 'Unknown User') as performed_by_name
                FROM login_logs ll
                LEFT JOIN users u ON ll.user_id = u.user_id
                LEFT JOIN users p ON ll.performed_by = p.user_id
                ORDER BY ll.timestamp DESC
                LIMIT %s OFFSET %s
            """
        
        cur.execute(query, (limit, offset))
        logs = cur.fetchall()
        
        # Get total count
        cur.execute("SELECT COUNT(*) FROM login_logs")
        total_count = cur.fetchone()[0]
        
        cur.close()
        cur = None
        
        # Convert to list of dictionaries
        log_list = []
        for log in logs:
            # Normalize activity_performed to match frontend expectations
            activity = log[2]
            if activity == 'LOGIN':
                activity = 'logged_in'
            elif activity == 'LOGOUT':
                activity = 'logged_out'
            # 'login_failed' and other values remain as-is
            
            log_dict = {
                'serial_number': log[0],  # Map serial_num to serial_number for frontend
                'user_id': log[1],
                'activity_performed': activity,
                'performed_by': log[3],
                'timestamp': log[4].isoformat() if log[4] else None,
                'user_name': log[5],
                'user_email': log[6],
                'performed_by_name': log[7]
            }
            
            # Add suspicious fields if they exist
            if has_suspicious_columns and len(log) > 8:
                log_dict['is_suspicious'] = log[8] if log[8] is not None else False
                log_dict['suspicion_reason'] = log[9] if len(log) > 9 else None
            else:
                log_dict['is_suspicious'] = False
                log_dict['suspicion_reason'] = None
            
            log_list.append(log_dict)
        
        return jsonify({
            "success": True,
            "logs": log_list,
            "total": total_count,
            "limit": limit,
            "offset": offset
        })
        
    except Exception as e:
        print(f"Error fetching login logs: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({"success": False, "message": f"Error loading login logs: {str(e)}"}), 500
    finally:
        if cur:
            try:
                cur.close()
            except:
                pass
        if conn:
            try:
                conn.close()
            except:
                pass

@login_logs_bp.route('/api/login-logs', methods=['POST'])
def log_login_activity():
    """Log login or logout activity"""
    try:
        data = request.json
        if not data:
            return jsonify({"success": False, "message": "No data provided"}), 400
            
        user_id = data.get('user_id')
        activity_performed = data.get('activity_performed')  # 'LOGIN' or 'LOGOUT'
        performed_by = data.get('performed_by', user_id)  # Default to user_id if not specified
        
        if not user_id or not activity_performed:
            return jsonify({"success": False, "message": "user_id and activity_performed are required"}), 400
            
        if activity_performed not in ['LOGIN', 'LOGOUT']:
            return jsonify({"success": False, "message": "activity_performed must be 'LOGIN' or 'LOGOUT'"}), 400
        
        conn = get_db_connection()
        cur = conn.cursor()
        
        # Insert login log
        cur.execute("""
            INSERT INTO login_logs (user_id, activity_performed, performed_by)
            VALUES (%s, %s, %s)
        """, (user_id, activity_performed, performed_by))
        
        conn.commit()
        cur.close()
        
        return jsonify({
            "success": True,
            "message": f"{activity_performed} activity logged successfully"
        })
        
    except Exception as e:
        print(f"Error logging login activity: {str(e)}")
        return jsonify({"success": False, "message": "Internal server error"}), 500

@login_logs_bp.route('/api/login-logs/pdf', methods=['GET'])
def download_login_logs_pdf():
    """Generate and download login logs as PDF"""
    conn = None
    cur = None
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        
        # Get query parameters
        limit = request.args.get('limit', type=int)
        search = request.args.get('search', '').strip()
        user_name = request.args.get('user_name', '').strip()
        user_id = request.args.get('user_id', '').strip()
        activity_type = request.args.get('activity_type', '').strip()
        date_from = request.args.get('date_from', '').strip()
        date_to = request.args.get('date_to', '').strip()
        
        # Check if suspicious activity columns exist
        cur.execute("""
            SELECT column_name 
            FROM information_schema.columns 
            WHERE table_name = 'login_logs' AND column_name = 'is_suspicious'
        """)
        has_suspicious_columns = cur.fetchone() is not None
        
        # Build base query
        if has_suspicious_columns:
            base_query = """
                SELECT ll.serial_num, ll.user_id, ll.activity_performed,
                       ll.performed_by, ll.timestamp,
                       COALESCE(u.name, 'Unknown User') as user_name,
                       COALESCE(u.email, 'N/A') as user_email,
                       COALESCE(p.name, 'Unknown User') as performed_by_name,
                       COALESCE(ll.is_suspicious, FALSE) as is_suspicious,
                       ll.suspicion_reason
                FROM login_logs ll
                LEFT JOIN users u ON ll.user_id = u.user_id
                LEFT JOIN users p ON ll.performed_by = p.user_id
            """
        else:
            base_query = """
                SELECT ll.serial_num, ll.user_id, ll.activity_performed,
                       ll.performed_by, ll.timestamp,
                       COALESCE(u.name, 'Unknown User') as user_name,
                       COALESCE(u.email, 'N/A') as user_email,
                       COALESCE(p.name, 'Unknown User') as performed_by_name
                FROM login_logs ll
                LEFT JOIN users u ON ll.user_id = u.user_id
                LEFT JOIN users p ON ll.performed_by = p.user_id
            """
        
        # Build WHERE conditions for all filters
        where_conditions = []
        query_params = []
        
        # General search (if provided)
        if search:
            search_pattern = f'%{search}%'
            search_lower = search.lower()
            
            search_conditions = [
                "CAST(ll.serial_num AS TEXT) ILIKE %s",
                "CAST(ll.user_id AS TEXT) ILIKE %s",
                "CAST(ll.performed_by AS TEXT) ILIKE %s",
                "COALESCE(u.name, '') ILIKE %s",
                "COALESCE(u.email, '') ILIKE %s",
                "COALESCE(p.name, '') ILIKE %s",
                "LOWER(ll.activity_performed) ILIKE %s"
            ]
            query_params.extend([search_pattern] * 7)
            
            if 'login' in search_lower and 'logout' not in search_lower and 'failed' not in search_lower:
                search_conditions.append("ll.activity_performed IN ('LOGIN', 'logged_in')")
            elif 'logout' in search_lower:
                search_conditions.append("ll.activity_performed IN ('LOGOUT', 'logged_out')")
            elif 'failed' in search_lower:
                search_conditions.append("ll.activity_performed = 'login_failed'")
            
            if has_suspicious_columns:
                search_conditions.append("COALESCE(ll.suspicion_reason, '') ILIKE %s")
                if 'suspicious' in search_lower:
                    search_conditions.append("ll.is_suspicious = TRUE")
                query_params.append(search_pattern)
            
            search_conditions.append("TO_CHAR(ll.timestamp, 'YYYY-MM-DD HH24:MI:SS') ILIKE %s")
            query_params.append(search_pattern)
            
            where_conditions.append("(" + " OR ".join(search_conditions) + ")")
        
        # Advanced filters
        if user_name:
            where_conditions.append("(COALESCE(u.name, '') ILIKE %s OR COALESCE(p.name, '') ILIKE %s)")
            user_name_pattern = f'%{user_name}%'
            query_params.extend([user_name_pattern, user_name_pattern])
        
        if user_id:
            where_conditions.append("(CAST(ll.user_id AS TEXT) ILIKE %s OR CAST(ll.performed_by AS TEXT) ILIKE %s)")
            user_id_pattern = f'%{user_id}%'
            query_params.extend([user_id_pattern, user_id_pattern])
        
        if activity_type:
            # Map frontend values to database values
            if activity_type == 'logged_in':
                where_conditions.append("ll.activity_performed IN ('LOGIN', 'logged_in')")
            elif activity_type == 'logged_out':
                where_conditions.append("ll.activity_performed IN ('LOGOUT', 'logged_out')")
            elif activity_type == 'login_failed':
                where_conditions.append("ll.activity_performed = 'login_failed'")
            else:
                where_conditions.append("ll.activity_performed = %s")
                query_params.append(activity_type)
        
        if date_from:
            where_conditions.append("DATE(ll.timestamp) >= %s")
            query_params.append(date_from)
        
        if date_to:
            where_conditions.append("DATE(ll.timestamp) <= %s")
            query_params.append(date_to)
        
        # Add WHERE clause if we have any conditions
        if where_conditions:
            base_query += " WHERE " + " AND ".join(where_conditions)
        
        # Add ORDER BY
        base_query += " ORDER BY ll.timestamp DESC"
        
        # Only apply limit if no filters are active (to export all filtered results when filters are applied)
        has_any_filters = search or user_name or user_id or activity_type or date_from or date_to
        if not has_any_filters and limit and limit > 0:
            base_query += " LIMIT %s"
            query_params.append(limit)
        
        # Debug: print query and params
        print(f"PDF Export Query: {base_query}")
        print(f"PDF Export Params: {query_params}")
        print(f"Has filters: {has_any_filters}, Limit applied: {not has_any_filters and limit and limit > 0}")
        
        cur.execute(base_query, tuple(query_params) if query_params else None)
        logs = cur.fetchall()
        
        print(f"PDF Export found {len(logs)} logs matching filters")
        
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
        
        # Title
        title = Paragraph("Login Logs Report", title_style)
        story.append(title)
        story.append(Spacer(1, 12))
        
        # Date
        date_para = Paragraph(f"Generated on: {export_timestamp.strftime('%Y-%m-%d %H:%M:%S')}", styles['Normal'])
        story.append(date_para)
        story.append(Spacer(1, 20))
        
        # Table data
        table_data = [['Serial', 'User ID', 'Activity', 'Performed By', 'Timestamp']]
        
        # If no logs found, add a message row
        if not logs or len(logs) == 0:
            table_data.append(['No logs found', 'matching', 'search criteria', '', ''])
        
        for log in logs:
            # Normalize activity for display
            activity = log[2]
            if activity == 'LOGIN':
                activity_display = 'LOGIN'
            elif activity == 'LOGOUT':
                activity_display = 'LOGOUT'
            elif activity == 'login_failed':
                activity_display = 'FAILED LOGIN'
            else:
                activity_display = activity
            
            timestamp = log[4].strftime('%Y-%m-%d %H:%M:%S') if log[4] else 'N/A'
            
            table_data.append([
                str(log[0]),
                str(log[1]) if log[1] != 0 else 'N/A',
                activity_display,
                log[7] if log[7] else 'Unknown',
                timestamp
            ])
        
        # Create table
        table = Table(table_data, colWidths=[0.8*inch, 0.8*inch, 1*inch, 1.5*inch, 1.8*inch])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, 0), 'CENTER'),  # Headers centered
            ('ALIGN', (0, 1), (0, -1), 'CENTER'),   # Serial column centered
            ('ALIGN', (1, 1), (1, -1), 'CENTER'),   # User ID column centered
            ('ALIGN', (2, 1), (2, -1), 'CENTER'),   # Activity column centered
            ('ALIGN', (3, 1), (3, -1), 'LEFT'),     # Performed By column left-aligned
            ('ALIGN', (4, 1), (4, -1), 'CENTER'),   # Timestamp column centered
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('FONTSIZE', (0, 1), (-1, -1), 8),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.beige]),
        ]))
        
        story.append(table)
        
        # Build PDF with header and footer on all pages
        doc.build(story, onFirstPage=add_header_footer, onLaterPages=add_header_footer)
        buffer.seek(0)
        
        return Response(
            buffer.getvalue(),
            mimetype='application/pdf',
            headers={
                'Content-Disposition': f'attachment; filename=login_logs_{datetime.now().strftime("%Y%m%d")}.pdf'
            }
        )
        
    except Exception as e:
        print(f"Error generating PDF: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({"success": False, "message": "Error generating PDF"}), 500
    finally:
        if cur:
            try:
                cur.close()
            except:
                pass
        if conn:
            try:
                conn.close()
            except:
                pass
