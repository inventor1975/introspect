const express = require('express');
const path = require('path');

const PUBLIC = path.join(__dirname, 'public', 'pages');
const app = express();

app.get('/pages/:name', (req, res, next) => {
  res.sendFile(req.params.name, { root: PUBLIC, dotfiles: 'deny' }, (err) => {
    if (err) next(err);
  });
});

app.use((err, req, res, next) => {
  res.status(err.status || 500).send(err.status === 404 ? 'Not found' : 'Error');
});

module.exports = app;
