const express = require('express');
const { exec } = require('child_process');

const app = express();
app.use(express.urlencoded({ extended: false }));

app.post('/admin/backup', (req, res) => {
  let database;
  if (req.body.scope === 'all') {
    database = '--all-databases';
  } else {
    database = req.body.database;
  }
  const stamp = new Date().toISOString().slice(0, 10);
  exec(`mysqldump ${database} > /backups/${stamp}.sql`, (err) => {
    if (err) return res.status(500).send('backup failed');
    res.send('ok');
  });
});

module.exports = app;
