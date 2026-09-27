const express = require('express');
const passport = require('passport');
const path = require('path');

const EXPORT_DIR = '/var/lib/accounts/exports';
const router = express.Router();

router.get(
  '/account/export',
  passport.authenticate('jwt', { session: false }),
  (req, res) => {
    const inline = req.query.inline === '1';
    const archive = path.join(EXPORT_DIR, `${req.user.id}.zip`);
    if (inline) {
      return res.sendFile(archive);
    }
    res.download(archive, 'my-data.zip');
  }
);

module.exports = router;
