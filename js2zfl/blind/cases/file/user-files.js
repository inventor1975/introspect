const express = require('express');
const { readUserFile, statUserFile } = require('./lib/storage');

const router = express.Router();

router.get('/users/files/:name', async (req, res, next) => {
  try {
    const info = await statUserFile(req.params.name);
    if (!info.isFile()) return res.sendStatus(404);
    const data = await readUserFile(req.params.name);
    res.set('Content-Length', String(info.size));
    res.type('application/octet-stream').send(data);
  } catch (err) {
    if (err.code === 'ENOENT') return res.sendStatus(404);
    next(err);
  }
});

module.exports = router;
