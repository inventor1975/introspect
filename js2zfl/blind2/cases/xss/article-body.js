const express = require('express');
const createDOMPurify = require('dompurify');
const { JSDOM } = require('jsdom');

const window = new JSDOM('').window;
const DOMPurify = createDOMPurify(window);

const app = express();
app.use(express.urlencoded({ extended: true }));

app.post('/articles/preview', (req, res) => {
  const clean = DOMPurify.sanitize(req.body.body);
  res.send(`<article class="post">${clean}</article>`);
});

module.exports = app;
