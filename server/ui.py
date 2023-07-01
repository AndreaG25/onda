from http.server import HTTPServer, SimpleHTTPRequestHandler
import os

class CustomHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        # Controlla se il percorso richiesto corrisponde a un file esistente
        if not os.path.exists(self.translate_path(self.path)):
            # File non trovato, invia risposta 404 personalizzata
            self.send_custom_404()
            return

        # Chiamata alla classe base per gestire le richieste GET
        super().do_GET()

    def send_custom_404(self):
        self.send_response(404)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(b'<h1>Errore 404 - Pagina non trovata</h1><br><a href="./home.html"<button>HOME</button></a>')

# Configurazione del server
host = 'localhost'
port = 5000
server_address = (host, port)
httpd = HTTPServer(server_address, CustomHandler)

# Avvio del server
print(f"Server in esecuzione su {host}:{port}")
httpd.serve_forever()
