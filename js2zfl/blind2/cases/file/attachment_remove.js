const express = require('express');
const fs = require('fs');
const path = require('path');

const app = express();
const ATTACH_DIR = process.env.ATTACH_DIR || '/var/lib/helpdesk/attachments';

app.delete('/tickets/:ticketId/attachments/:id', (req, res) => {
  const target = path.resolve(ATTACH_DIR, req.params.id);
  fs.unlink(target, (err) => {
    if (err) {
      if (err.code === 'ENOENT') return res.sendStatus(404);
      return res.status(500).json({ error: 'could not remove attachment' });
    }
    res.sendStatus(204);
  });
});

module.exports = app;
