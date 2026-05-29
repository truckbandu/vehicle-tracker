# Vehicle Tracker API Documentation

## Base URL

```
http://localhost:5000/api
```

## Authentication

All endpoints (except `/auth/register` and `/auth/login`) require a JWT token in the `Authorization` header:

```
Authorization: Bearer <token>
```

## Response Format

All responses follow this format:

### Success Response
```json
{
  "success": true,
  "data": {},
  "message": "Operation successful"
}
```

### Error Response
```json
{
  "success": false,
  "error": "Error message",
  "code": "ERROR_CODE"
}
```

## Endpoints

### Authentication

#### Register
```
POST /auth/register
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "password123",
  "name": "John Doe"
}

Response: 201 Created
{
  "success": true,
  "data": {
    "id": "user_123",
    "email": "user@example.com",
    "name": "John Doe"
  },
  "token": "jwt_token_here"
}
```

#### Login
```
POST /auth/login
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "password123"
}

Response: 200 OK
{
  "success": true,
  "token": "jwt_token_here",
  "user": {
    "id": "user_123",
    "email": "user@example.com",
    "name": "John Doe"
  }
}
```

### Vehicles

#### List All Vehicles
```
GET /vehicles
Authorization: Bearer <token>

Response: 200 OK
{
  "success": true,
  "data": [
    {
      "id": "vehicle_123",
      "make": "Toyota",
      "model": "Camry",
      "year": 2023,
      "licensePlate": "ABC123",
      "userId": "user_123",
      "createdAt": "2023-01-01T00:00:00Z"
    }
  ]
}
```

#### Create Vehicle
```
POST /vehicles
Authorization: Bearer <token>
Content-Type: application/json

{
  "make": "Toyota",
  "model": "Camry",
  "year": 2023,
  "licensePlate": "ABC123"
}

Response: 201 Created
{
  "success": true,
  "data": {
    "id": "vehicle_123",
    "make": "Toyota",
    "model": "Camry",
    "year": 2023,
    "licensePlate": "ABC123"
  }
}
```

### Trips

#### Start Trip
```
POST /trips
Authorization: Bearer <token>
Content-Type: application/json

{
  "vehicleId": "vehicle_123"
}

Response: 201 Created
{
  "success": true,
  "data": {
    "id": "trip_123",
    "vehicleId": "vehicle_123",
    "userId": "user_123",
    "startTime": "2023-01-01T10:00:00Z",
    "status": "active",
    "startLocation": {
      "latitude": 40.7128,
      "longitude": -74.0060
    }
  }
}
```

#### Get Trip Details
```
GET /trips/:id
Authorization: Bearer <token>

Response: 200 OK
{
  "success": true,
  "data": {
    "id": "trip_123",
    "vehicleId": "vehicle_123",
    "startTime": "2023-01-01T10:00:00Z",
    "endTime": "2023-01-01T11:00:00Z",
    "distance": 25.5,
    "duration": 3600,
    "status": "completed",
    "route": []
  }
}
```

#### End Trip
```
POST /trips/:id/end
Authorization: Bearer <token>

Response: 200 OK
{
  "success": true,
  "data": {
    "id": "trip_123",
    "status": "completed",
    "endTime": "2023-01-01T11:00:00Z",
    "distance": 25.5,
    "duration": 3600
  }
}
```

### GPS Tracking

#### Send GPS Update
```
POST /gps/update
Authorization: Bearer <token>
Content-Type: application/json

{
  "tripId": "trip_123",
  "latitude": 40.7128,
  "longitude": -74.0060,
  "speed": 45,
  "altitude": 100,
  "accuracy": 5,
  "timestamp": 1672531200000
}

Response: 200 OK
{
  "success": true,
  "message": "GPS update recorded"
}
```

### Analytics

#### Get Summary
```
GET /analytics/summary
Authorization: Bearer <token>

Response: 200 OK
{
  "success": true,
  "data": {
    "totalTrips": 45,
    "totalDistance": 1250.5,
    "totalDuration": 95400,
    "averageSpeed": 47.3,
    "lastTrip": "2023-01-15T14:30:00Z"
  }
}
```

## Error Codes

| Code | Status | Description |
|------|--------|-------------|
| INVALID_CREDENTIALS | 401 | Invalid email or password |
| TOKEN_EXPIRED | 401 | JWT token has expired |
| UNAUTHORIZED | 401 | Not authenticated |
| FORBIDDEN | 403 | Not authorized to access resource |
| NOT_FOUND | 404 | Resource not found |
| VALIDATION_ERROR | 400 | Invalid input data |
| INTERNAL_ERROR | 500 | Server error |

## WebSocket Events

### Connect
```javascript
socket.on('connect', () => {
  console.log('Connected to server');
});
```

### Send GPS Update
```javascript
socket.emit('gps:update', {
  tripId: 'trip_123',
  latitude: 40.7128,
  longitude: -74.0060,
  speed: 45,
  altitude: 100,
  accuracy: 5,
  timestamp: Date.now()
});
```

### Watch Trip
```javascript
socket.emit('trip:watch', 'trip_123');
socket.on('gps:update', (data) => {
  console.log('GPS update:', data);
});
```
