# Vehicle Tracker - Web Dashboard

React web application for managing vehicles and viewing trip analytics.

## Prerequisites

- Node.js 16+
- npm or yarn

## Installation

```bash
cd web
npm install
```

## Configuration

1. Copy `.env.example` to `.env.local`
```bash
cp .env.example .env.local
```

2. Update `.env.local` with your API URL and Google Maps API key

## Running the App

```bash
# Development
npm start

# Build for production
npm run build

# Run tests
npm test
```

App runs on `http://localhost:3000`

## Project Structure

```
web/
├── src/
│   ├── components/       # Reusable components
│   ├── pages/            # Page components
│   ├── services/         # API services
│   ├── context/          # React Context
│   ├── hooks/            # Custom hooks
│   ├── utils/            # Utility functions
│   └── App.jsx           # Root component
├── public/               # Static files
└── package.json
```

## Key Pages

- **Dashboard** - Overview of all vehicles and trips
- **Vehicles** - Manage vehicles
- **Trip History** - View past trips
- **Trip Detail** - Detailed view of individual trips
- **Analytics** - Trip statistics and reports
- **Settings** - User settings

## Dependencies

- react
- react-router-dom
- axios
- google-map-react
- recharts (for analytics)
- date-fns

## Testing

```bash
npm test
```

## Deployment

See [DEPLOYMENT.md](../docs/DEPLOYMENT.md) for deployment instructions.
