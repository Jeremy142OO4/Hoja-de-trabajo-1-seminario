import json
import os
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer


PORT = int(os.getenv("PORT", "3000"))
CARNET = os.getenv("CARNET", "202300644")
ESTUDIANTE = os.getenv("ESTUDIANTE", "Jeremy Estuardo Orellana Aldana")


class ApiHandler(BaseHTTPRequestHandler):
    def send_json(self, status_code, payload):
        body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(status_code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        if self.path == "/check":
            self.send_json(200, {"status": "OK"})
        elif self.path == "/":
            self.send_json(
                200,
                {
                    "Instancia": "Instancia #2 - API #2",
                    "Curso": "Seminario de Sistemas 1",
                    "Estudiante": f"{ESTUDIANTE} - {CARNET}",
                },
            )
        else:
            self.send_json(404, {"error": "Not found"})

    def do_POST(self):
        self.send_json(405, {"error": "Method not allowed"})

    def log_message(self, message_format, *args):
        print(f"{self.client_address[0]} - {message_format % args}")


if __name__ == "__main__":
    server = ThreadingHTTPServer(("0.0.0.0", PORT), ApiHandler)
    print(f"API #2 listening on port {PORT}")
    server.serve_forever()
