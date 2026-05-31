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
    
    # Vehicles Table
    conn.execute('''CREATE TABLE IF NOT EXISTS vehicles 
                    (vehicle_id TEXT PRIMARY KEY, vehicle_name TEXT, driver_name TEXT, driver_phone TEXT,
                     chassis_no TEXT, engine_no TEXT, tyres TEXT, make TEXT, model TEXT, owner_name TEXT,
                     rd_validity TEXT, fitness_validity TEXT, permit_validity TEXT, 
                     insurance_validity TEXT, puc_validity TEXT)''')
    
    # Drivers Table
    conn.execute('''CREATE TABLE IF NOT EXISTS drivers 
                    (driver_id INTEGER PRIMARY KEY AUTOINCREMENT,
                     name TEXT, licence_no TEXT, mobile TEXT, home_no TEXT,
                     village TEXT, district TEXT, state TEXT, pin TEXT,
                     aadhar_no TEXT, agent_name TEXT,
                     licence_image TEXT, aadhar_image TEXT)''')
    
    # Locations & Geofences
    conn.execute('''CREATE TABLE IF NOT EXISTS locations 
                    (id INTEGER PRIMARY KEY, vehicle_id TEXT, lat REAL, lng REAL, 
                     speed REAL, timestamp TEXT, trip_id TEXT)''')
    
    conn.execute('''CREATE TABLE IF NOT EXISTS geofences 
                    (id INTEGER PRIMARY KEY, name TEXT, lat REAL, lng REAL, 
                     radius REAL, type TEXT)''')
    
    conn.commit()
    conn.close()

init_db()

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/mobile_sender.html')
def mobile_sender():
    return send_from_directory('.', 'mobile_sender.html')

@app.route('/add_vehicle', methods=['POST'])
def add_vehicle():
    try:
        data = request.json
        vehicle_id = data.get('vehicle_id', '').strip().upper()
        if not vehicle_id:
            return jsonify({"status": "error", "message": "Vehicle ID required"}), 400

        conn = sqlite3.connect('trips.db')
        conn.execute("""INSERT OR REPLACE INTO vehicles VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                     (vehicle_id, data.get('vehicle_name',''), data.get('driver_name',''), data.get('driver_phone',''),
                      data.get('chassis_no',''), data.get('engine_no',''), data.get('tyres',''),
                      data.get('make',''), data.get('model',''), data.get('owner_name',''),
                      data.get('rd_validity',''), data.get('fitness_validity',''), data.get('permit_validity',''),
                      data.get('insurance_validity',''), data.get('puc_validity','')))
        conn.commit()
        conn.close()
        return jsonify({"status": "success", "message": f"Vehicle {vehicle_id} added successfully"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/vehicles')
def get_vehicles():
    conn = sqlite3.connect('trips.db')
    cursor = conn.execute("SELECT * FROM vehicles")
    vehicles = [dict(zip([col[0] for col in cursor.description], row)) for row in cursor.fetchall()]
    conn.close()
    return jsonify(vehicles)

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

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    print(f"🚛 Vehicle Tracker running on port {port}")
    socketio.run(app, host='0.0.0.0', port=port, allow_unsafe_werkzeug=True)
