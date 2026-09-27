const express = require('express');
const { exec } = require('child_process');

const app = express();
app.use(express.urlencoded({ extended: false }));

app.post('/feedback', (req, res) => {
  const message = req.body.message;
  const email = req.body.email;
  if (!message || message.length > 2000) {
    return res.status(400).send('Message missing or too long: ' + String(message).slice(0, 50));
  }
  require('fs').appendFileSync('/var/spool/feedback.jsonl', JSON.stringify({ email, message }) + '\n');
  exec('systemctl start feedback-digest.service', () => {
    res.redirect('/thanks');
  });
});

module.exports = app;
