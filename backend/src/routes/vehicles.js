const express = require('express');
const router = express.Router();

// GET /api/vehicles
router.get('/', (req, res) => {
  res.json({ message: 'List vehicles - to be implemented' });
});

// POST /api/vehicles
router.post('/', (req, res) => {
  res.json({ message: 'Create vehicle - to be implemented' });
});

// GET /api/vehicles/:id
router.get('/:id', (req, res) => {
  res.json({ message: 'Get vehicle - to be implemented' });
});

// PUT /api/vehicles/:id
router.put('/:id', (req, res) => {
  res.json({ message: 'Update vehicle - to be implemented' });
});

// DELETE /api/vehicles/:id
router.delete('/:id', (req, res) => {
  res.json({ message: 'Delete vehicle - to be implemented' });
});

module.exports = router;
