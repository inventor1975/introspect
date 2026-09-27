const express = require('express');
const { marked } = require('marked');
const DOMPurify = require('isomorphic-dompurify');

const app = express();
app.use(express.urlencoded({ extended: false }));

app.post('/docs/preview', (req, res) => {
  const source = req.body.markdown || '';
  const rendered = marked.parse(source);
  const clean = DOMPurify.sanitize(rendered);
  res.send(`<div class="markdown-body">${clean}</div>`);
});

module.exports = app;
