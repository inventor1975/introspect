const express = require('express');

const app = express();

app.get('/handle/preview', (req, res) => {
  let handle = req.query.handle;
  if (typeof handle !== 'string' || !/^[a-z0-9_]{1,32}$/i.test(handle)) {
    handle = 'guest';
  }
  res.send('<span class="handle">@' + handle + '</span>');
});

module.exports = app;
