'use strict';

const MAP = {
  '&': '&amp;',
  '<': '&lt;',
  '>': '&gt;',
  '"': '&quot;',
  "'": '&#39;',
};

function encodeEntities(value) {
  return String(value == null ? '' : value).replace(/[&<>"']/g, (ch) => MAP[ch]);
}

module.exports = { encodeEntities };
