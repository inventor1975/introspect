const express = require('express');
const { readUserFile, listUserFiles } = require('./lib/userFiles');

const router = express.Router();

router.get('/documents', async (req, res) => {
  const files = await listUserFiles(req.user.id);
  res.json({ files });
});

router.get('/documents/open', async (req, res) => {
  try {
    const body = await readUserFile(req.user.id, req.query.doc);
    res.type('text/plain').send(body);
  } catch (e) {
    res.status(404).json({ error: 'not found' });
  }
});

module.exports = router;
