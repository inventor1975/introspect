const express = require('express');
const { exec } = require('child_process');

const router = express.Router();

router.param('container', (req, res, next, value) => {
  req.containerName = value;
  next();
});

router.get('/containers/:container/logs', (req, res) => {
  const tail = 100;
  exec(`docker logs --tail ${tail} ${req.params.container}`, (err, stdout, stderr) => {
    if (err) return res.status(404).send(stderr);
    res.type('text').send(stdout);
  });
});

module.exports = router;
