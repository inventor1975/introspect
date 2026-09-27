const express = require('express');
const fs = require('fs');
const path = require('path');

const UPLOAD_DIR = path.join(__dirname, 'incoming');
const app = express();
app.use(express.json({ limit: '10mb' }));

function decodePayload(body) {
  return {
    name: body.filename,
    data: Buffer.from(body.contentBase64 || '', 'base64'),
  };
}

app.post('/api/files', (req, res) => {
  const upload = decodePayload(req.body);
  if (!upload.name || upload.data.length === 0) {
    return res.status(422).json({ error: 'filename and content required' });
  }
  fs.writeFileSync(path.join(UPLOAD_DIR, upload.name), upload.data);
  res.status(201).json({ stored: upload.name, bytes: upload.data.length });
});

module.exports = app;
