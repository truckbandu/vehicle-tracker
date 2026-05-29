# Deployment Guide

## Backend Deployment

### Heroku

1. Create Heroku app
```bash
heroku create vehicle-tracker-api
```

2. Set environment variables
```bash
heroku config:set NODE_ENV=production
heroku config:set JWT_SECRET=your_secret
heroku config:set DATABASE_URL=your_postgres_url
```

3. Deploy
```bash
git push heroku main
```

### AWS EC2

1. Launch EC2 instance
2. Install Node.js and PostgreSQL
3. Clone repository
4. Install dependencies and run

## Mobile Deployment

### iOS (App Store)
```bash
eas build --platform ios
eas submit --platform ios
```

### Android (Google Play)
```bash
eas build --platform android
eas submit --platform android
```

## Web Deployment

### Vercel
```bash
npm i -g vercel
vercel
```

### Netlify
```bash
npm run build
# Upload dist folder to Netlify
```

## Database Setup

### PostgreSQL on AWS RDS

1. Create RDS instance
2. Update CONNECTION_STRING in environment
3. Run migrations

## Environment Configuration

Ensure all environment variables are set before deployment:

- Backend: See `backend/.env.example`
- Mobile: See `mobile/.env.example`
- Web: See `web/.env.example`
