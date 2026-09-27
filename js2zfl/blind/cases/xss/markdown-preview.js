const express = require('express');
const { marked } = require('marked');

const app = express();
app.use(express.urlencoded({ extended: false }));

app.post('/markdown/preview', (req, res) => {
  const source = req.body.markdown || '';
  const html = marked.parse(source);
  res.send(`<div class="markdown-body">${html}</div>`);
});

module.exports = app;
