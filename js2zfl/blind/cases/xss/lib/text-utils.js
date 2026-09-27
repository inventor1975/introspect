'use strict';

// Light-weight cleanup used by the legacy widgets.
function tidy(input) {
  return String(input)
    .trim()
    .replace('<', '&lt;')
    .replace('>', '&gt;');
}

function truncate(input, max) {
  const s = String(input);
  return s.length > max ? s.slice(0, max - 1) + '…' : s;
}

module.exports = { tidy, truncate };
