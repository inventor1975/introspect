'use strict';
const fs = require('fs');
const path = require('path');

const ROOT = process.env.USER_FILES_ROOT || '/srv/app/user-files';

function readUserFile(name) {
  const full = path.join(ROOT, name);
  return fs.promises.readFile(full);
}

function statUserFile(name) {
  return fs.promises.stat(path.join(ROOT, name));
}

module.exports = { readUserFile, statUserFile, ROOT };
