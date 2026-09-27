const express = require('express');

const app = express();

app.get('/dashboard', (req, res) => {
  const view = req.query.view || 'summary';
  let html;
  switch (view) {
    case 'summary':
      html = '<h2>Summary</h2>';
      break;
    case 'details':
      html = '<h2>Details</h2>';
      break;
    default:
      html = `<p class="warn">Unknown view: ${view}</p>`;
  }
  res.send(html);
});

module.exports = app;
