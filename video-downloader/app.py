import os
from flask import Flask, request, jsonify, send_from_directory, abort, render_template
from redis import Redis
from rq import Queue

app = Flask(__name__, template_folder='templates')

REDIS_URL = os.getenv('REDIS_URL', 'redis://redis:6379/0')
redis_conn = Redis.from_url(REDIS_URL)
q = Queue(connection=redis_conn)

DOWNLOAD_FOLDER = os.getenv('DOWNLOAD_FOLDER', '/app/downloads')
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/download', methods=['POST'])
def enqueue():
    data = request.get_json() or {}
    url = data.get('url')
    if not url:
        return jsonify({'error':'url required'}), 400
    job = q.enqueue('tasks.download_video', url, DOWNLOAD_FOLDER, result_ttl=86400)
    return jsonify({'job_id': job.get_id()}), 202

@app.route('/api/status/<job_id>', methods=['GET'])
def status(job_id):
    from rq.job import Job
    try:
        job = Job.fetch(job_id, connection=redis_conn)
    except Exception:
        return jsonify({'error':'not found'}), 404
    return jsonify({'id': job.id, 'status': job.get_status(), 'result': job.result}), 200

@app.route('/downloads/<path:filename>', methods=['GET'])
def serve_file(filename):
    safe_path = os.path.abspath(os.path.join(DOWNLOAD_FOLDER, filename))
    if not safe_path.startswith(os.path.abspath(DOWNLOAD_FOLDER)):
        abort(403)
    return send_from_directory(DOWNLOAD_FOLDER, filename, as_attachment=True)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
