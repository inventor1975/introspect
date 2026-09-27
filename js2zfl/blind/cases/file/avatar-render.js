const express = require('express');
const path = require('path');
const db = require('./lib/db');

const AVATAR_DIR = path.join(__dirname, 'static', 'avatars');
const router = express.Router();
router.use(express.json());

router.put('/users/:id/avatar', async (req, res) => {
  if (!req.user || String(req.user.id) !== req.params.id) return res.sendStatus(403);
  await db.setUserAvatar(req.params.id, req.body.avatar);
  res.sendStatus(204);
});

router.get('/users/:id/avatar', async (req, res) => {
  const user = await db.findUser(req.params.id);
  if (!user || !user.avatar) {
    return res.sendFile(path.join(AVATAR_DIR, 'default.png'));
  }
  res.sendFile(path.join(AVATAR_DIR, user.avatar));
});

module.exports = router;
