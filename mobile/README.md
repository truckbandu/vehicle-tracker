# Vehicle Tracker - Mobile App

React Native mobile application for real-time vehicle trip tracking with GPS.

## Prerequisites

- Node.js 16+
- Expo CLI: `npm install -g expo-cli`
- iOS: Xcode (macOS)
- Android: Android Studio

## Installation

```bash
cd mobile
npm install
```

## Configuration

1. Copy `.env.example` to `.env`
```bash
cp .env.example .env
```

2. Update `.env` with your API URL and Google Maps API key

## Running the App

### Development
```bash
# Start Expo
npm start

# Run on iOS simulator
npm run ios

# Run on Android emulator
npm run android

# Run on web
npm run web
```

### Building
```bash
# Build for iOS
eas build --platform ios

# Build for Android
eas build --platform android

# Build for web
npm run build
```

## Project Structure

```
mobile/
├── src/
│   ├── screens/          # Screen components
│   ├── components/       # Reusable components
│   ├── navigation/       # React Navigation setup
│   ├── services/         # API and utility services
│   ├── context/          # React Context
│   ├── hooks/            # Custom hooks
│   └── App.js            # Entry point
├── assets/               # Images, fonts, etc.
├── app.json              # Expo configuration
└── package.json
```

## Key Features

- Real-time GPS tracking
- Trip history
- Live map view
- Trip statistics
- Offline support
- Push notifications

## Permissions Required

- Location (Always & When in Use)
- Background App Refresh
- Battery optimization exemption

## Dependencies

- expo
- react-native
- react-navigation
- @react-native-geolocation
- react-native-maps
- axios
- socket.io-client

## Testing

```bash
npm test
```

## Troubleshooting

### GPS not working
- Ensure location permissions are granted
- Check that GPS is enabled on device
- Verify API URL is correct

### Connection issues
- Check backend is running
- Verify API_URL in .env
- Check firewall settings
