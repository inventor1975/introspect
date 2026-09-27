const express = require('express');
const path = require('path');

const LEGAL_DIR = path.join(__dirname, 'legal');
const DOCUMENTS = {
  terms: 'terms-of-service-2026.pdf',
  privacy: 'privacy-policy-2026.pdf',
  dpa: 'data-processing-addendum.pdf',
};

const app = express();

app.get('/legal/:doc', (req, res) => {
  const key = req.params.doc;
  if (!Object.hasOwn(DOCUMENTS, key)) {
    return res.status(404).send('Unknown document');
  }
  const file = DOCUMENTS[key];
  res.download(path.join(LEGAL_DIR, file));
});

module.exports = app;
