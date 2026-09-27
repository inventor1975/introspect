'use strict';

function toLabel(raw) {
  return String(raw || '')
    .replace(/[^\w\s-]/g, '')
    .replace(/\s+/g, ' ')
    .trim()
    .slice(0, 64);
}

module.exports = { toLabel };
