const path = require('path');

class PathEscapeError extends Error {
  constructor(rel) {
    super(`path escapes root: ${rel}`);
    this.status = 403;
  }
}

function confine(root, rel) {
  const base = path.resolve(root);
  const target = path.resolve(base, String(rel));
  if (target !== base && !target.startsWith(base + path.sep)) {
    throw new PathEscapeError(rel);
  }
  return target;
}

module.exports = { confine, PathEscapeError };
