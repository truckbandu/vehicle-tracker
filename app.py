from flask import Flask, request, jsonify, send_from_directory
from flask_socketio import SocketIO
import sqlite3
from datetime import datetime
import os
import math

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='gevent')

def init_db():
    conn = sqlite3.connect('trips.db')
    conn.execute('''CREATE TABLE IF NOT EXISTS vehicles 
                    (vehicle_id TEXT PRIMARY KEY, vehicle_name TEXT, driver_name TEXT, driver_phone TEXT)''')
    conn.execute('''CREATE TABLE IF NOT EXISTS locations 
                    (id INTEGER PRIMARY KEY, vehicle_id TEXT, lat REAL, lng REAL, speed REAL, timestamp TEXT, trip_id TEXT)''')
    conn.execute('''CREATE TABLE IF NOT EXISTS geofences 
                    (id INTEGER PRIMARY KEY, name TEXT, lat REAL, lng REAL, radius REAL, type TEXT)''')
    conn.commit()
    conn.close()

conn.execute('''CREATE TABLE IF NOT EXISTS drivers 
                    (driver_id INTEGER PRIMARY KEY AUTOINCREMENT,
                     name TEXT,
                     licence_no TEXT,
                     mobile TEXT,
                     home_no TEXT,
                     village TEXT,
                     district TEXT,
                     state TEXT,
                     pin TEXT,
                     aadhar_no TEXT,
                     agent_name TEXT,
                     licence_image TEXT,
                     aadhar_image TEXT)''')

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

@app.route('/vehicles')
def get_vehicles():
    conn = sqlite3.connect('trips.db')
    cursor = conn.execute("SELECT * FROM vehicles")
    vehicles = [{"vehicle_id": r[0], "vehicle_name": r[1], "driver_name": r[2], "driver_phone": r[3]} for r in cursor.fetchall()]
    conn.close()
    return jsonify(vehicles)

@app.route('/add_vehicle', methods=['POST'])
def add_vehicle():
    try:
        data = request.json
        vehicle_id = data.get('vehicle_id', '').strip().upper()
        if not vehicle_id:
            return jsonify({"status": "error", "message": "Vehicle ID required"}), 400

        conn = sqlite3.connect('trips.db')
        conn.execute("INSERT OR REPLACE INTO vehicles VALUES (?, ?, ?, ?)",
                     (vehicle_id, data.get('vehicle_name','Unknown'), data.get('driver_name',''), data.get('driver_phone','')))
        conn.commit()
        conn.close()
        return jsonify({"status": "success", "message": f"Vehicle {vehicle_id} added successfully"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/add_geofence', methods=['POST'])
def add_geofence():
    try:
        data = request.json
        conn = sqlite3.connect('trips.db')
        conn.execute("INSERT INTO geofences (name, lat, lng, radius, type) VALUES (?, ?, ?, ?, ?)",
                     (data['name'], data['lat'], data['lng'], data['radius'], data['type']))
        conn.commit()
        conn.close()
        return jsonify({"status": "success", "message": f"{data['type']} point added"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/geofences')
def get_geofences():
    conn = sqlite3.connect('trips.db')
    cursor = conn.execute("SELECT * FROM geofences")
    geofences = [{"id": r[0], "name": r[1], "lat": r[2], "lng": r[3], "radius": r[4], "type": r[5]} for r in cursor.fetchall()]
    conn.close()
    return jsonify(geofences)

@app.route('/delete_geofence/<int:geofence_id>', methods=['DELETE'])
def delete_geofence(geofence_id):
    conn = sqlite3.connect('trips.db')
    conn.execute("DELETE FROM geofences WHERE id = ?", (geofence_id,))
    conn.commit()
    conn.close()
    return jsonify({"status": "success", "message": "Geofence deleted"})

@app.route('/add_driver', methods=['POST'])
def add_driver():
    try:
        data = request.form
        conn = sqlite3.connect('trips.db')
        conn.execute("""INSERT INTO drivers 
                        (name, licence_no, mobile, home_no, village, district, state, pin, 
                         aadhar_no, agent_name, licence_image, aadhar_image) 
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                     (data.get('name'), data.get('licence_no'), data.get('mobile'),
                      data.get('home_no'), data.get('village'), data.get('district'),
                      data.get('state'), data.get('pin'), data.get('aadhar_no'),
                      data.get('agent_name'), data.get('licence_image'), data.get('aadhar_image')))
        conn.commit()
        conn.close()
        return jsonify({"status": "success", "message": "Driver added successfully"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/drivers')
def get_drivers():
    conn = sqlite3.connect('trips.db')
    cursor = conn.execute("SELECT * FROM drivers")
    drivers = [dict(zip([col[0] for col in cursor.description], row)) for row in cursor.fetchall()]
    conn.close()
    return jsonify(drivers)


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    print(f"🚛 Vehicle Tracker running on port {port}")
    socketio.run(app, host='0.0.0.0', port=port, allow_unsafe_werkzeug=True)
