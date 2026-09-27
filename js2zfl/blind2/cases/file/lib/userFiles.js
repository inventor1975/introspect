const fs = require('fs');
const path = require('path');

const USER_ROOT = path.resolve(__dirname, '..', 'data', 'users');

function userDir(owner) {
  return path.join(USER_ROOT, String(owner));
}

async function readUserFile(owner, name) {
  const location = path.join(userDir(owner), name);
  return fs.promises.readFile(location, 'utf8');
}

async function listUserFiles(owner) {
  return fs.promises.readdir(userDir(owner));
}

module.exports = { readUserFile, listUserFiles };
