# Vehicle Trip Tracker

A full-stack application for tracking vehicle trips with real-time GPS monitoring. Includes a Node.js/Express backend, React Native mobile app, and React web dashboard.

## Project Structure

```
vehicle-tracker/
├── backend/          # Node.js/Express API
├── mobile/           # React Native mobile app
├── web/              # React web dashboard
└── docs/             # Documentation
```

## Features

- ✅ Real-time GPS tracking
- ✅ Trip history and analytics
- ✅ Multi-vehicle support
- ✅ User authentication
- ✅ Distance and duration logging
- ✅ Mobile and web dashboards
- ✅ WebSocket for live updates

## Tech Stack

### Backend
- Node.js + Express
- PostgreSQL
- JWT authentication
- WebSocket (Socket.io)
- Google Maps API

### Mobile
- React Native
- React Navigation
- Geolocation API
- Axios

### Web
- React
- React Router
- Axios
- Google Maps React

## Getting Started

See individual README files in each directory:
- [Backend Setup](./backend/README.md)
- [Mobile Setup](./mobile/README.md)
- [Web Setup](./web/README.md)

## Environment Variables

Each component requires `.env` files. See `.env.example` files for templates.

## API Documentation

See [API_DOCS.md](./docs/API_DOCS.md) for detailed endpoint documentation.

## License

MIT
