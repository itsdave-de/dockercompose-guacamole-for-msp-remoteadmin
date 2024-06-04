import re
import docker
import threading
from bottle import Bottle, run, response

app = Bottle()
client = docker.from_env()
session_data = {
    "last_id": None,
    "sessions": {}
}

# Expressões regulares para capturar o início e término da conexão
start_pattern = re.compile(r'Connection ID is "\$([^"]+)"')
end_pattern = re.compile(r'Connection "\$([^"]+)" removed')

def capture_logs():
    for log in client.containers.get('guacd').logs(stream=True):
        log = log.decode('utf-8').strip()
        start_match = start_pattern.search(log)
        end_match = end_pattern.search(log)

        if start_match:
            session_id = start_match.group(1)
            session_data["last_id"] = session_id
            session_data["sessions"][session_id] = {"start": log}
            print(f"Captured Connection Start ID: {session_id}")

        if end_match:
            session_id = end_match.group(1)
            if session_id in session_data["sessions"]:
                session_data["sessions"][session_id]["end"] = log
            else:
                session_data["sessions"][session_id] = {"end": log}
            print(f"Captured Connection End ID: {session_id}")

@app.route('/last_id')
def get_last_id():
    if session_data["last_id"]:
        return {"last_id": session_data["last_id"]}
    response.status = 404
    return {"error": "No Connection ID found"}

@app.route('/session/<session_id>')
def get_session(session_id):
    session = session_data["sessions"].get(session_id)
    if session:
        return session
    response.status = 404
    return {"error": f"No session found with ID {session_id}"}

if __name__ == "__main__":
    # Inicia a captura de logs em uma thread separada
    threading.Thread(target=capture_logs, daemon=True).start()
    # Executa o servidor Bottle
    run(app, host='0.0.0.0', port=8085)

