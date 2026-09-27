'use strict';

const express = require('express');
const fs = require('fs');
const os = require('os');
const path = require('path');

const SESSION_TMP = path.join(os.tmpdir(), 'editor-sessions');
const router = express.Router();

router.post('/editor/session/close', express.urlencoded({ extended: false }), (req, res) => {
  const sessionKey = req.body.session;
  if (!sessionKey) {
    return res.status(400).send('missing session');
  }
  try {
    fs.rmSync(path.join(SESSION_TMP, sessionKey), { recursive: true, force: true });
  } catch (err) {
    return res.status(500).send('cleanup failed');
  }
  res.send('closed');
});

module.exports = router;
