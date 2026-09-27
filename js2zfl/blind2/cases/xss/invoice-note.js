const express = require('express');
const ejs = require('ejs');

const app = express();
app.use(express.urlencoded({ extended: false }));

const NOTE_TEMPLATE = `
<div class="invoice-note">
  <h4><%= heading %></h4>
  <p><%= note %></p>
</div>`;

app.post('/invoices/note/preview', (req, res) => {
  const html = ejs.render(NOTE_TEMPLATE, {
    heading: req.body.heading || 'Note',
    note: req.body.note,
  });
  res.send(html);
});

module.exports = app;
