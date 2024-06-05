import re
import requests
import docker
import threading
import time
import os
from datetime import datetime

# Configurations for Docker client
client = docker.from_env()

# Match the connection ID from the log
start_pattern = re.compile(r'Connection ID is "\$([^"]+)"')
end_pattern = re.compile(r'Connection "\$([^"]+)" removed')

# Frappe API url
FRAPPE_URL = os.getenv('FRAPPE_URL')

def monitor_logs():
    for log in client.containers.get('guacd').logs(stream=True):
        log = log.decode('utf-8').strip()
        start_match = start_pattern.search(log)
        end_match = end_pattern.search(log)

        if start_match:
            session_id = start_match.group(1)
            start_time = datetime.now().isoformat()
            send_start_session(session_id, start_time)
            print(f"Captured Connection Start ID: {session_id} at {start_time}")

        if end_match:
            session_id = end_match.group(1)
            end_time = datetime.now().isoformat()
            send_end_session(session_id, end_time)
            print(f"Captured Connection End ID: {session_id} at {end_time}")

def send_start_session(session_id, start_time):
    data = {
        "session_id": session_id,
        "start_time": start_time
    }
    try:
        response = requests.post(f"{FRAPPE_URL}/api/method/msp_remoteadmin.tools.log_start_session", json=data)
        if response.status_code == 200:
            print(f"Successfully sent start session data for ID: {session_id}")
        else:
            print(f"Failed to send start session data for ID: {session_id}, Status Code: {response.status_code}")
    except Exception as e:
        print(f"Error sending start session data for ID: {session_id}: {str(e)}")

def send_end_session(session_id, end_time):
    data = {
        "session_id": session_id,
        "end_time": end_time
    }
    try:
        response = requests.post(f"{FRAPPE_URL}/api/method/msp_remoteadmin.tools.log_end_session", json=data)
        if response.status_code == 200:
            print(f"Successfully sent end session data for ID: {session_id}")
        else:
            print(f"Failed to send end session data for ID: {session_id}, Status Code: {response.status_code}")
    except Exception as e:
        print(f"Error sending end session data for ID: {session_id}: {str(e)}")

if __name__ == "__main__":
    # Start the log monitoring thread
    thread = threading.Thread(target=monitor_logs)
    thread.daemon = True
    thread.start()

    # Keep the main thread running
    print("Log monitoring service started")
    while True:
        time.sleep(1)
