const { exec } = require('child_process');

const REBUILD_CMD = 'npm run --prefix /srv/app build:cache';

function rebuildCache(reason, cb) {
  console.info(`[maintenance] cache rebuild requested: ${reason}`);
  exec(REBUILD_CMD, { timeout: 300000 }, (err, stdout) => cb(err, stdout));
}

module.exports = { rebuildCache };
