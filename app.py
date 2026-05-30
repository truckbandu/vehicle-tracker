from flask import Flask, request, jsonify, send_file
from flask_socketio import SocketIO
import sqlite3
from datetime import datetime
import math

app = Flask(__name__, static_folder='.', static_url_path='')
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='gevent')

def init_db():
    conn = sqlite3.connect('trips.db')
    conn.execute('''CREATE TABLE IF NOT EXISTS vehicles 
                    (vehicle_id TEXT PRIMARY KEY, vehicle_name TEXT, driver_name TEXT, driver_phone TEXT)''')
    
    conn.execute('''CREATE TABLE IF NOT EXISTS locations 
                    (id INTEGER PRIMARY KEY, vehicle_id TEXT, lat REAL, lng REAL, 
                     speed REAL, timestamp TEXT, trip_id TEXT)''')
    
    conn.execute('''CREATE TABLE IF NOT EXISTS geofences 
                    (id INTEGER PRIMARY KEY, name TEXT, lat REAL, lng REAL, 
                     radius REAL, type TEXT)''')  # type: 'pickup' or 'drop'
    conn.commit()
    conn.close()

init_db()

def get_distance(lat1, lon1, lat2, lon2):
    R = 6371000  # meters
    φ1 = math.radians(lat1)
    φ2 = math.radians(lat2)
    Δφ = math.radians(lat2 - lat1)
    Δλ = math.radians(lon2 - lon1)
    a = math.sin(Δφ/2)**2 + math.cos(φ1) * math.cos(φ2) * math.sin(Δλ/2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c

# ====================== ROUTES ======================

@app.route('/')
def index():
    return send_file('index.html')

@app.route('/mobile_sender.html')
def mobile_sender():
    return send_file('mobile_sender.html')

@app.route('/add_vehicle', methods=['POST'])
def add_vehicle():
    data = request.json
    vehicle_id = data.get('vehicle_id', '').strip().upper()
    vehicle_name = data.get('vehicle_name', 'Unknown')
    driver_name = data.get('driver_name', '')
    driver_phone = data.get('driver_phone', '')
    
    conn = sqlite3.connect('trips.db')
    conn.execute("INSERT OR REPLACE INTO vehicles VALUES (?, ?, ?, ?)",
                 (vehicle_id, vehicle_name, driver_name, driver_phone))
    conn.commit()
    conn.close()
    return jsonify({"status": "success", "message": f"Vehicle {vehicle_id} added"})

@app.route('/vehicles')
def get_vehicles():
    conn = sqlite3.connect('trips.db')
    cursor = conn.execute("SELECT * FROM vehicles")
    vehicles = [{"vehicle_id": r[0], "vehicle_name": r[1], "driver_name": r[2], "driver_phone": r[3]} for r in cursor.fetchall()]
    conn.close()
    return jsonify(vehicles)

@app.route('/add_geofence', methods=['POST'])
def add_geofence():
    data = request.json
    conn = sqlite3.connect('trips.db')
    conn.execute("INSERT INTO geofences (name, lat, lng, radius, type) VALUES (?, ?, ?, ?, ?)",
                 (data['name'], data['lat'], data['lng'], data['radius'], data['type']))
    conn.commit()
    conn.close()
    return jsonify({"status": "success", "message": f"{data['type'].capitalize()} point added"})

@app.route('/geofences')
def get_geofences():
    conn = sqlite3.connect('trips.db')
    cursor = conn.execute("SELECT * FROM geofences")
    geofences = [{"id": r[0], "name": r[1], "lat": r[2], "lng": r[3], "radius": r[4], "type": r[5]} for r in cursor.fetchall()]
    conn.close()
    return jsonify(geofences)

@app.route('/delete_geofence/<int:geofence_id>', methods=['DELETE'])
def delete_geofence(geofence_id):
    try:
        conn = sqlite3.connect('trips.db')
        conn.execute("DELETE FROM geofences WHERE id = ?", (geofence_id,))
        conn.commit()
        conn.close()
        return jsonify({"status": "success", "message": "Geofence deleted successfully"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500
    
@app.route('/track', methods=['POST'])
def track():
    data = request.json
    vehicle_id = data.get('vehicle_id', '').strip().upper()
    lat = float(data['lat'])
    lng = float(data['lng'])
    speed = float(data.get('speed', 0))
    current_trip_id = data.get('trip_id')

    conn = sqlite3.connect('trips.db')
    trip_id = current_trip_id

    # Geofence Logic
    cursor = conn.execute("SELECT * FROM geofences")
    for row in cursor.fetchall():
        _, name, g_lat, g_lng, radius, g_type = row
        distance = get_distance(lat, lng, g_lat, g_lng)
        
        if distance <= radius:
            if g_type == 'pickup':
                if not trip_id:                                 # Start Trip at first pickup
                    trip_id = f"TRIP_{vehicle_id}_{datetime.now().strftime('%Y%m%d_%H%M')}"
                    print(f"🚀 Auto Start Trip at {name}")
                else:                                           # End Trip when reaching next pickup
                    print(f"🏁 Auto End Trip at {name}")
                    if confirm_auto_action(vehicle_id, name):   # Confirmation
                        trip_id = None

    # Save Location
    conn.execute("INSERT INTO locations (vehicle_id, lat, lng, speed, timestamp, trip_id) VALUES (?, ?, ?, ?, ?, ?)",
                 (vehicle_id, lat, lng, speed, datetime.now().isoformat(), trip_id))
    conn.commit()
    conn.close()

    socketio.emit('location_update', {
        'vehicle_id': vehicle_id,
        'lat': lat,
        'lng': lng,
        'speed': round(speed, 1),
        'timestamp': datetime.now().strftime("%H:%M:%S"),
        'trip_id': trip_id
    })
    return jsonify({"status": "success", "trip_id": trip_id})

def confirm_auto_action(vehicle_id, location_name):
    # This is server-side log. Real confirmation can be enhanced with Socket.IO later
    print(f"✅ Confirmation: Trip ended for {vehicle_id} at {location_name}")
    return True

if __name__ == '__main__':
    print("🚛 Vehicle Tracking Server Started with Geofencing (Next Pickup = End Trip)")
    socketio.run(app, debug=True, host='0.0.0.0', port=5000, allow_unsafe_werkzeug=True)