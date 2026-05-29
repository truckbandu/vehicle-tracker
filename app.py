from flask import Flask, request, jsonify, render_template
from flask_socketio import SocketIO
import sqlite3
from datetime import datetime
import threading
import time

app = Flask(__name__)
socketio = SocketIO(app)

# Database setup
def init_db():
    conn = sqlite3.connect('trips.db')
    conn.execute('''CREATE TABLE IF NOT EXISTS locations 
                    (id INTEGER PRIMARY KEY, vehicle_id TEXT, lat REAL, lng REAL, speed REAL, timestamp TEXT)''')
    conn.close()

init_db()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/track', methods=['POST'])
def track():
    data = request.json
    vehicle_id = data.get('vehicle_id', 'VEH001')
    lat = data['lat']
    lng = data['lng']
    speed = data.get('speed', 0)
    
    conn = sqlite3.connect('trips.db')
    conn.execute("INSERT INTO locations (vehicle_id, lat, lng, speed, timestamp) VALUES (?, ?, ?, ?, ?)",
                 (vehicle_id, lat, lng, speed, datetime.now().isoformat()))
    conn.commit()
    conn.close()
    
    # Broadcast live update
    socketio.emit('location_update', {
        'vehicle_id': vehicle_id,
        'lat': lat,
        'lng': lng,
        'speed': speed,
        'timestamp': datetime.now().strftime("%H:%M:%S")
    })
    return jsonify({"status": "success"})

@app.route('/history')
def history():
    conn = sqlite3.connect('trips.db')
    cursor = conn.execute("SELECT * FROM locations ORDER BY timestamp DESC LIMIT 100")
    rows = cursor.fetchall()
    conn.close()
    return jsonify([{"id": r[0], "vehicle_id": r[1], "lat": r[2], "lng": r[3], "speed": r[4], "time": r[5]} for r in rows])

if __name__ == '__main__':
    socketio.run(app, debug=True, host='0.0.0.0', port=5000)
