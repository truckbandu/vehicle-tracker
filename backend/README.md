# Vehicle Tracker - Backend API

Node.js/Express REST API with WebSocket support for real-time GPS tracking.

## Prerequisites

- Node.js 16+
- PostgreSQL 12+
- npm or yarn

## Installation

```bash
cd backend
npm install
```

## Configuration

1. Copy `.env.example` to `.env`
```bash
cp .env.example .env
```

2. Update `.env` with your configuration:
   - Database credentials
   - JWT secret
   - Google Maps API key

## Database Setup

```bash
# Create database
creatdb vehicle_tracker

# Run migrations
npm run migrate

# Seed sample data (optional)
npm run seed
```

## Running the Server

```bash
# Development
npm run dev

# Production
npm start
```

Server runs on `http://localhost:5000`

## Project Structure

```
backend/
├── src/
│   ├── models/          # Database models
│   ├── routes/          # API routes
│   ├── controllers/      # Route controllers
│   ├── middleware/       # Custom middleware
│   ├── services/        # Business logic
│   ├── utils/           # Utility functions
│   ├── validators/      # Input validation
│   └── app.js           # Express app
├── migrations/          # Database migrations
├── seeds/               # Seed data
├── server.js            # Entry point
└── package.json
```

## API Endpoints

### Authentication
- `POST /api/auth/register` - Register user
- `POST /api/auth/login` - Login user
- `POST /api/auth/logout` - Logout user
- `POST /api/auth/refresh` - Refresh token

### Vehicles
- `GET /api/vehicles` - List all vehicles
- `POST /api/vehicles` - Create vehicle
- `GET /api/vehicles/:id` - Get vehicle details
- `PUT /api/vehicles/:id` - Update vehicle
- `DELETE /api/vehicles/:id` - Delete vehicle

### Trips
- `GET /api/trips` - List all trips
- `POST /api/trips` - Start new trip
- `GET /api/trips/:id` - Get trip details
- `PUT /api/trips/:id` - Update trip
- `POST /api/trips/:id/end` - End trip
- `GET /api/trips/:id/route` - Get trip route

### GPS Tracking
- `POST /api/gps/update` - Send GPS location
- `GET /api/gps/live/:tripId` - Get live GPS data (WebSocket)

### Analytics
- `GET /api/analytics/summary` - Trip summary
- `GET /api/analytics/monthly` - Monthly statistics
- `GET /api/analytics/vehicle/:id` - Vehicle statistics

## WebSocket Events

### Connect
```javascript
socket.on('connect', () => {
  // Connection established
});
```

### GPS Update
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

### Trip Events
```javascript
socket.on('trip:started', (tripData) => {});
socket.on('trip:ended', (tripData) => {});
socket.on('trip:paused', (tripData) => {});
```

## Error Handling

All errors return a consistent format:

```json
{
  "success": false,
  "error": "Error message",
  "code": "ERROR_CODE",
  "statusCode": 400
}
```

## Testing

```bash
# Run tests
npm test

# Run with coverage
npm run test:coverage
```

## Deployment

See [DEPLOYMENT.md](../docs/DEPLOYMENT.md) for deployment instructions.
