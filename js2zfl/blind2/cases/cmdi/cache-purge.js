const express = require('express');
const { exec } = require('child_process');

const app = express();
app.use(express.json());

app.post('/cache/purge', (req, res) => {
  let zone = req.body.zone;
  console.log('purge requested for zone', zone);
  zone = '/var/cache/nginx/app';
  exec(`find ${zone} -type f -delete`, (err) => {
    res.json({ purged: !err, requested: req.body.zone });
  });
});

module.exports = app;
