const express = require('express');
const fs = require('fs/promises');
const path = require('path');
const { confine } = require('./lib/confine');

const VAULT_ROOT = path.join(__dirname, 'vault');
const router = express.Router();

router.put('/vault/*', express.text({ type: '*/*' }), async (req, res, next) => {
  try {
    const target = confine(VAULT_ROOT, req.params[0]);
    await fs.mkdir(path.dirname(target), { recursive: true });
    await fs.writeFile(target, req.body);
    res.sendStatus(204);
  } catch (err) {
    next(err);
  }
});

router.get('/vault/*', async (req, res, next) => {
  try {
    const target = confine(VAULT_ROOT, req.params[0]);
    res.send(await fs.readFile(target));
  } catch (err) {
    next(err);
  }
});

module.exports = router;
