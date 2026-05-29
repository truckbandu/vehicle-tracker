const express = require('express');
const router = express.Router();

// GET /api/analytics/summary
router.get('/summary', (req, res) => {
  res.json({ message: 'Analytics summary - to be implemented' });
});

// GET /api/analytics/monthly
router.get('/monthly', (req, res) => {
  res.json({ message: 'Monthly analytics - to be implemented' });
});

// GET /api/analytics/vehicle/:id
router.get('/vehicle/:id', (req, res) => {
  res.json({ message: 'Vehicle analytics - to be implemented' });
});

module.exports = router;
