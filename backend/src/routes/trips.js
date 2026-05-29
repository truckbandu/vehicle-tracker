const express = require('express');
const router = express.Router();

// GET /api/trips
router.get('/', (req, res) => {
  res.json({ message: 'List trips - to be implemented' });
});

// POST /api/trips
router.post('/', (req, res) => {
  res.json({ message: 'Start trip - to be implemented' });
});

// GET /api/trips/:id
router.get('/:id', (req, res) => {
  res.json({ message: 'Get trip - to be implemented' });
});

// PUT /api/trips/:id
router.put('/:id', (req, res) => {
  res.json({ message: 'Update trip - to be implemented' });
});

// POST /api/trips/:id/end
router.post('/:id/end', (req, res) => {
  res.json({ message: 'End trip - to be implemented' });
});

// GET /api/trips/:id/route
router.get('/:id/route', (req, res) => {
  res.json({ message: 'Get trip route - to be implemented' });
});

module.exports = router;
