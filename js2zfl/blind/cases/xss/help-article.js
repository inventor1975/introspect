const express = require('express');
const { page, card } = require('./lib/layout');

const router = express.Router();

router.get('/help/:topic', (req, res) => {
  const topic = req.params.topic;
  const summary = req.query.summary || 'No summary available.';
  const content = card(topic, summary);
  res.send(page('Help: ' + topic, content));
});

module.exports = router;
