const express = require('express');
const { execSync } = require('child_process');

const app = express();
app.use(express.json());

app.post('/notes/sign', (req, res) => {
  const note = JSON.stringify(req.body.note);
  const signature = execSync(`echo ${note} | gpg --clearsign --batch --local-user notes@internal`, {
    encoding: 'utf8',
  });
  res.type('text/plain').send(signature);
});

module.exports = app;
