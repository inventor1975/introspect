'use strict';
const path = require('path');

class PathEscapeError extends Error {
  constructor(p) {
    super(`path escapes base directory: ${p}`);
    this.name = 'PathEscapeError';
    this.status = 403;
  }
}

function safeJoin(base, userPath) {
  const root = path.resolve(base);
  const target = path.resolve(root, String(userPath));
  if (target !== root && !target.startsWith(root + path.sep)) {
    throw new PathEscapeError(userPath);
  }
  return target;
}

module.exports = { safeJoin, PathEscapeError };
