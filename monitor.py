import requests
import smtplib
import time
import os
from datetime import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from shapely.geometry import Point, Polygon
from config import (
    API_BASE_URL,
    CLINICIAN_IDS,
    POLLING_INTERVAL,
    EMAIL_CONFIG
)

out_of_bounds_status = {}

def get_clinician_status(clinician_id):
    url = f"{API_BASE_URL}/clinicianstatus/{clinician_id}"
    try:
        response = requests.get(url, timeout=10)
        return response.json() if response.status_code == 200 else None
    except requests.exceptions.RequestException:
        return None

def extract_location_data(status_data):
    if not status_data or not isinstance(status_data, dict):
        return None, None

    try:
        if status_data.get('type') == 'FeatureCollection' and 'features' in status_data:
            current_coords = None
            boundary_coords = None
            
            for feature in status_data['features']:
                if not isinstance(feature, dict) or 'geometry' not in feature:
                    continue
                    
                geometry = feature['geometry']
                if geometry.get('type') == 'Point':
                    current_coords = geometry['coordinates']
                elif geometry.get('type') == 'Polygon':
                    boundary_coords = geometry['coordinates']
            
            return current_coords, boundary_coords
        
        if 'geometry' in status_data:
            return (status_data['geometry'].get('coordinates'),
                   status_data.get('properties', {}).get('boundary', {}).get('coordinates'))
        
        return (status_data.get('coordinates'),
               status_data.get('boundary', {}).get('coordinates'))
        
    except Exception:
        return None, None

def is_inside_boundary(current_location, boundary_coords):
    try:
        if not current_location or not boundary_coords:
            return False
            
        point = Point(current_location[0], current_location[1])
        
        if isinstance(boundary_coords[0][0], (list, tuple)):
            polygon_coords = boundary_coords[0]
        else:
            polygon_coords = boundary_coords
            
        polygon = Polygon(polygon_coords)
        return polygon.contains(point)
        
    except Exception:
        return False

def send_alert_email(clinician_id, current_location):
    try:
        message = MIMEMultipart()
        message["From"] = EMAIL_CONFIG['sender_email']
        message["To"] = EMAIL_CONFIG['recipient_email']
        message["Subject"] = f"🚨 ALERT: Phlebotomist {clinician_id} Out of Bounds"
        
        body = f"""
⚠️ SECURITY ALERT - IMMEDIATE ACTION REQUIRED

Phlebotomist ID: {clinician_id}
Status: OUT OF BOUNDS
Current Location: {current_location}
Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

This phlebotomist has left their designated safety zone.
Please investigate immediately to ensure their safety.

---
This is an automated alert from the Phlebotomist Monitoring System.
"""
        message.attach(MIMEText(body, "plain"))
        
        with smtplib.SMTP(EMAIL_CONFIG['smtp_server'], EMAIL_CONFIG['smtp_port']) as server:
            server.starttls()
            server.login(EMAIL_CONFIG['sender_email'], EMAIL_CONFIG['sender_password'])
            server.sendmail(
                EMAIL_CONFIG['sender_email'],
                EMAIL_CONFIG['recipient_email'],
                message.as_string()
            )
        
        print(f"Alert email sent for clinician {clinician_id}")
        return True
        
    except Exception as e:
        print(f"Failed to send alert email: {str(e)}")
        return False

def check_single_clinician(clinician_id):
    status_data = get_clinician_status(clinician_id)
    if not status_data:
        return
        
    current_coords, boundary_coords = extract_location_data(status_data)
    if not current_coords or not boundary_coords:
        return
        
    is_safe = is_inside_boundary(current_coords, boundary_coords)
    current_time = datetime.now()
    
    if not is_safe:
        if clinician_id not in out_of_bounds_status:
            if send_alert_email(clinician_id, current_coords):
                out_of_bounds_status[clinician_id] = {
                    'timestamp': current_time,
                    'location': current_coords,
                    'last_alert': current_time
                }
        else:
            last_alert = out_of_bounds_status[clinician_id]['last_alert']
            if (current_time - last_alert).total_seconds() >= 300:  # 5 minutes
                if send_alert_email(clinician_id, current_coords):
                    out_of_bounds_status[clinician_id]['last_alert'] = current_time
                    
    elif clinician_id in out_of_bounds_status:
        print(f"Clinician {clinician_id} has returned to safety zone")
        del out_of_bounds_status[clinician_id]

def check_all_clinicians():
    for clinician_id in CLINICIAN_IDS:
        try:
            check_single_clinician(clinician_id)
        except Exception as e:
            print(f"Error checking clinician {clinician_id}: {str(e)}")
        time.sleep(1)

def run_monitoring():
    print("Starting phlebotomist monitoring system...")
    
    while True:
        try:
            check_all_clinicians()
            time.sleep(POLLING_INTERVAL)
            
        except KeyboardInterrupt:
            print("Monitoring stopped by user")
            break
            
        except Exception as e:
            print(f"Unexpected error in monitoring loop: {str(e)}")
            time.sleep(30)

if __name__ == "__main__":
    run_monitoring()