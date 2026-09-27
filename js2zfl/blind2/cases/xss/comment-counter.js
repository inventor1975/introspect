const express = require('express');

const app = express();
app.use(express.urlencoded({ extended: false }));

app.post('/comments/count', (req, res) => {
  const comment = String(req.body.comment || '');
  const words = comment.trim().split(/\s+/).filter(Boolean);
  res.send(
    `<p>Your comment has ${comment.length} characters and ${words.length} words.</p>`
  );
});

module.exports = app;
