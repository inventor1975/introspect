const express = require('express');
const ejs = require('ejs');

const app = express();
app.use(express.urlencoded({ extended: false }));

const SIGNATURE_TEMPLATE = `
<div class="signature">
  <strong><%= fullName %></strong><br>
  <span class="title"><%- jobTitle %></span>
</div>`;

app.post('/settings/signature/preview', (req, res) => {
  const html = ejs.render(SIGNATURE_TEMPLATE, {
    fullName: req.body.fullName,
    jobTitle: req.body.jobTitle,
  });
  res.send(html);
});

module.exports = app;
