const express = require('express');
const router = express.Router();

// POST /api/gps/update
router.post('/update', (req, res) => {
  res.json({ message: 'GPS update - to be implemented' });
});

// GET /api/gps/live/:tripId
router.get('/live/:tripId', (req, res) => {
  res.json({ message: 'Live GPS - to be implemented' });
});

module.exports = router;
