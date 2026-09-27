const express = require('express');

const app = express();
app.use(express.json());

app.post('/checklist/render', (req, res) => {
  const items = Array.isArray(req.body.items) ? req.body.items : [];
  const html = [
    '<ul class="checklist">',
    ...items.map((item) => `<li><input type="checkbox"> ${item.label}</li>`),
    '</ul>',
  ].join('');
  res.send(html);
});

module.exports = app;
