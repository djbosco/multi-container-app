from flask import Flask, render_template, request, jsonify
import redis
import os

app = Flask(__name__)

# Connect to Redis
redis_host = os.getenv('REDIS_HOST', 'redis')
redis_port = 6379
try:
    r = redis.Redis(host=redis_host, port=redis_port, db=0, decode_responses=True)
    r.ping()  # Test connection
except redis.ConnectionError:
    r = None

@app.route('/')
def index():
    visit_count = 0
    if r:
        visit_count = r.incr('visits')
    ip_address = request.remote_addr
    return render_template('index.html', count=visit_count, ip=ip_address)

@app.route('/stats')
def stats():
    visits = r.get('visits') if r else "Redis not connected"
    return jsonify({
        "visits": visits,
        "client_ip": request.remote_addr,
        "status": "OK" if r else "Redis error"
    })

@app.route('/health')
def health():
    status = "UP" if r else "DOWN"
    return jsonify({"status": status})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
