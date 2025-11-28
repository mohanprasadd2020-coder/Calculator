from flask import Flask, send_from_directory, render_template_string, abort
import os

app = Flask(__name__, static_folder=None)

# Root folder where your HTML files live
ROOT = os.path.dirname(os.path.abspath(__file__))


def list_html_files():
    """Return a sorted list of .html files in the project root."""
    try:
        files = [f for f in os.listdir(ROOT) if f.lower().endswith('.html')]
    except OSError:
        files = []
    return sorted(files)


@app.route('/')
def index():
    """Serve index.html as the main file."""
    return send_from_directory(ROOT, 'index.html')


@app.route('/files')
def files_index():
    """Return a simple HTML page with links to all HTML files found."""
    files = list_html_files()
    links = ''.join(f'<li><a href="/{f}">{f}</a></li>' for f in files)
    page = f"""
    <!doctype html>
    <html>
      <head>
        <meta charset="utf-8">
        <title>HTML files index</title>
      </head>
      <body>
        <h1>Available HTML files</h1>
        <ul>
          {links}
        </ul>
        <p><a href="/">Open index.html</a></p>
      </body>
    </html>
    """
    return render_template_string(page)


@app.route('/<path:filename>')
def serve_file(filename):
    """Serve a requested file (HTML, images, etc.) from the project root.

    Security: disallow path-traversal by comparing basename and checking file
    presence in the allowed list. Only serves common static file types.
    """
    # Prevent traversal like ../../etc/passwd
    if os.path.basename(filename) != filename:
        abort(404)

    # Allowed file extensions
    allowed_extensions = {'.html', '.jpg', '.jpeg', '.png', '.gif', '.css', '.js', '.svg', '.webp'}
    _, ext = os.path.splitext(filename.lower())
    if ext not in allowed_extensions:
        abort(403)  # Forbidden

    # Check if file exists in the project root
    file_path = os.path.join(ROOT, filename)
    if not os.path.isfile(file_path):
        abort(404)

    return send_from_directory(ROOT, filename)


if __name__ == '__main__':
    # Run a development server on port 5000
    app.run(host='0.0.0.0', port=5000, debug=True)
