const express = require('express');
const pug = require('pug');

const app = express();

const announce = pug.compile([
  'section.announcement',
  '  h2= heading',
  '  p!= details',
].join('\n'));

app.get('/announce', (req, res) => {
  res.send(announce({ heading: 'Announcement', details: req.query.details }));
});

module.exports = app;
