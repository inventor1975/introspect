const express = require('express');
const fs = require('fs');
const path = require('path');

const HELP_DIR = path.join(__dirname, 'help');
const TOPICS = new Set(['getting-started', 'billing', 'accounts', 'api-keys', 'webhooks']);
const app = express();

app.get('/help', (req, res) => {
  let topic = req.query.topic;
  if (!TOPICS.has(topic)) {
    topic = 'getting-started';
  }
  const text = fs.readFileSync(path.join(HELP_DIR, topic + '.md'), 'utf8');
  res.json({ topic, text });
});

module.exports = app;
