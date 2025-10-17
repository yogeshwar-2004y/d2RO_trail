from flask import Blueprint, request, jsonify, Response
from config import get_db_connection
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.units import inch
from datetime import datetime
import io

login_logs_bp = Blueprint('login_logs', __name__)

@login_logs_bp.route('/api/login-logs', methods=['GET'])
def get_login_logs():
    """Get login logs for admin dashboard"""
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        
        # Get query parameters
        limit = request.args.get('limit', 100, type=int)
        offset = request.args.get('offset', 0, type=int)
        
        # Fetch login logs with user information
        cur.execute("""
            SELECT ll.serial_num, ll.user_id, ll.activity_performed, 
                   ll.performed_by, ll.timestamp,
                   COALESCE(u.name, 'Unknown User') as user_name, 
                   COALESCE(u.email, 'N/A') as user_email,
                   COALESCE(p.name, 'Unknown User') as performed_by_name
            FROM login_logs ll
            LEFT JOIN users u ON ll.user_id = u.user_id
            LEFT JOIN users p ON ll.performed_by = p.user_id
            ORDER BY ll.serial_num ASC
            LIMIT %s OFFSET %s
        """, (limit, offset))
        
        logs = cur.fetchall()
        
        # Get total count
        cur.execute("SELECT COUNT(*) FROM login_logs")
        total_count = cur.fetchone()[0]
        
        cur.close()
        
        # Convert to list of dictionaries
        log_list = []
        for log in logs:
            log_list.append({
                'serial_num': log[0],
                'user_id': log[1],
                'activity_performed': log[2],
                'performed_by': log[3],
                'timestamp': log[4].isoformat() if log[4] else None,
                'user_name': log[5],
                'user_email': log[6],
                'performed_by_name': log[7]
            })
        
        return jsonify({
            "success": True,
            "logs": log_list,
            "total": total_count,
            "limit": limit,
            "offset": offset
        })
        
    except Exception as e:
        print(f"Error fetching login logs: {str(e)}")
        return jsonify({"success": False, "message": "Internal server error"}), 500

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
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        
        # Get all login logs
        cur.execute("""
            SELECT ll.serial_num, ll.user_id, ll.activity_performed,
                   ll.performed_by, ll.timestamp,
                   COALESCE(u.name, 'Unknown User') as user_name,
                   COALESCE(u.email, 'N/A') as user_email,
                   COALESCE(p.name, 'Unknown User') as performed_by_name
            FROM login_logs ll
            LEFT JOIN users u ON ll.user_id = u.user_id
            LEFT JOIN users p ON ll.performed_by = p.user_id
            ORDER BY ll.serial_num ASC
        """)
        
        logs = cur.fetchall()
        cur.close()
        
        # Create PDF
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=A4)
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
        date_para = Paragraph(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", styles['Normal'])
        story.append(date_para)
        story.append(Spacer(1, 20))
        
        # Table data
        table_data = [['Serial', 'User ID', 'Activity', 'Performed By', 'Timestamp']]
        
        for log in logs:
            activity_display = log[2]  # Use the activity_performed value directly
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
        
        # Build PDF
        doc.build(story)
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
        return jsonify({"success": False, "message": "Error generating PDF"}), 500
