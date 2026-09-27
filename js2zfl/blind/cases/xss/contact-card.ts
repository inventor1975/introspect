import express from 'express';
import escapeHtml from 'escape-html';

const app = express();

app.get('/contact-card', (req, res) => {
  const first = String(req.query.first ?? '');
  const last = String(req.query.last ?? '');
  const company = String(req.query.company ?? '');
  const displayFirst = escapeHtml(first);
  const displayCompany = escapeHtml(company);
  res.send(`<div class="vcard"><span>${displayFirst} ${last}</span><small>${displayCompany}</small></div>`);
});

export default app;
