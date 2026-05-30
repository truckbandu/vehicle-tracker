from flask import Flask, request, jsonify, send_from_directory
from flask_socketio import SocketIO
import sqlite3
from datetime import datetime
import os
import math

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='gevent', logger=True, engineio_logger=True)

def init_db():
    conn = sqlite3.connect('trips.db')
    conn.execute('''CREATE TABLE IF NOT EXISTS vehicles 
                    (vehicle_id TEXT PRIMARY KEY, vehicle_name TEXT, driver_name TEXT, driver_phone TEXT)''')
    conn.execute('''CREATE TABLE IF NOT EXISTS locations 
                    (id INTEGER PRIMARY KEY, vehicle_id TEXT, lat REAL, lng REAL, 
                     speed REAL, timestamp TEXT, trip_id TEXT)''')
    conn.execute('''CREATE TABLE IF NOT EXISTS geofences 
                    (id INTEGER PRIMARY KEY, name TEXT, lat REAL, lng REAL, 
                     radius REAL, type TEXT)''')
    conn.commit()
    conn.close()

init_db()

def get_distance(lat1, lon1, lat2, lon2):
    R = 6371000
    φ1 = math.radians(lat1)
    φ2 = math.radians(lat2)
    Δφ = math.radians(lat2 - lat1)
    Δλ = math.radians(lon2 - lon1)
    a = math.sin(Δφ/2)**2 + math.cos(φ1) * math.cos(φ2) * math.sin(Δλ/2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/mobile_sender.html')
def mobile_sender():
    return send_from_directory('.', 'mobile_sender.html')

# Add other routes (add_vehicle, vehicles, add_geofence, delete_geofence, track, etc.)
@app.route('/add_vehicle', methods=['POST'])
def add_vehicle():
    try:
        data = request.json
        vehicle_id = data.get('vehicle_id', '').strip().upper()
        conn = sqlite3.connect('trips.db')
        conn.execute("INSERT OR REPLACE INTO vehicles VALUES (?, ?, ?, ?)",
                     (vehicle_id, data.get('vehicle_name','Unknown'), data.get('driver_name',''), data.get('driver_phone','')))
        conn.commit()
        conn.close()
        return jsonify({"status": "success", "message": f"Vehicle {vehicle_id} added"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/track', methods=['POST'])
def track():
    # Simplified version
    data = request.json
    vehicle_id = data.get('vehicle_id', '').strip().upper()
    lat = float(data['lat'])
    lng = float(data['lng'])
    speed = float(data.get('speed', 0))
    
    conn = sqlite3.connect('trips.db')
    conn.execute("INSERT INTO locations (vehicle_id, lat, lng, speed, timestamp, trip_id) VALUES (?, ?, ?, ?, ?, ?)",
                 (vehicle_id, lat, lng, speed, datetime.now().isoformat(), data.get('trip_id')))
    conn.commit()
    conn.close()

    socketio.emit('location_update', {
        'vehicle_id': vehicle_id,
        'lat': lat,
        'lng': lng,
        'speed': round(speed, 1),
        'timestamp': datetime.now().strftime("%H:%M:%S")
    })
    return jsonify({"status": "success"})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    print(f"🚛 Vehicle Tracker running on port {port}")
    socketio.run(app, host='0.0.0.0', port=port, allow_unsafe_werkzeug=True)
