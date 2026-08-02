import os
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs, urlparse

from rag import ask

HTML_PAGE = """
<!doctype html>
<html lang='en'>
<head>
  <meta charset='utf-8'>
  <meta name='viewport' content='width=device-width, initial-scale=1'>
  <title>Educational RAG Chatbot</title>
  <style>
    body { font-family: Arial, sans-serif; max-width: 800px; margin: 40px auto; padding: 20px; }
    textarea { width: 100%; height: 100px; padding: 10px; }
    button { margin-top: 10px; padding: 10px 16px; }
    .answer { margin-top: 20px; padding: 12px; background: #f5f7fb; border-radius: 8px; }
    .sources { margin-top: 10px; color: #555; }
  </style>
</head>
<body>
  <h2>Educational RAG Chatbot</h2>
  <form id='chat-form'>
    <textarea name='question' placeholder='Ask a question about the PDF content'></textarea><br>
    <button type='submit'>Ask</button>
  </form>
  <div id='result' class='answer'>Waiting for your question...</div>
  <div id='sources' class='sources'></div>

  <script>
    const form = document.getElementById('chat-form');
    const result = document.getElementById('result');
    const sources = document.getElementById('sources');

    form.addEventListener('submit', async (e) => {
      e.preventDefault();
      const data = new FormData(form);
      result.textContent = 'Thinking...';
      sources.textContent = '';

      const response = await fetch('/ask', {
        method: 'POST',
        body: new URLSearchParams(data)
      });
      const json = await response.json();
      result.textContent = json.answer || '';
      if (json.sources && json.sources.length) {
        sources.innerHTML = '<strong>Sources:</strong><br>' + json.sources.map(s => '• ' + s).join('<br>');
      } else {
        sources.textContent = 'No sources found.';
      }
    });
  </script>
</body>
</html>
"""


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/' or self.path.startswith('/?'):
            self.send_response(200)
            self.send_header('Content-Type', 'text/html; charset=utf-8')
            self.end_headers()
            self.wfile.write(HTML_PAGE.encode('utf-8'))
        else:
            self.send_response(404)
            self.end_headers()

    def do_POST(self):
        if self.path != '/ask':
            self.send_response(404)
            self.end_headers()
            return

        length = int(self.headers.get('Content-Length', '0'))
        body = self.rfile.read(length).decode('utf-8')
        params = parse_qs(body)
        question = params.get('question', [''])[0]

        answer, sources = ask(question)

        payload = {
            'answer': answer,
            'sources': sources,
        }

        self.send_response(200)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.end_headers()
        import json
        self.wfile.write(json.dumps(payload).encode('utf-8'))

    def log_message(self, format, *args):
        return


if __name__ == '__main__':
    port = int(os.getenv('PORT', '8000'))
    host = os.getenv('HOST', '0.0.0.0')
    server = HTTPServer((host, port), Handler)
    print(f'Server running at http://{host}:{port}')
    server.serve_forever()
