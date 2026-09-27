'use strict';

const { escapeHtml } = require('./html');

module.exports = {
  plain(value) {
    return escapeHtml(value);
  },
  upper(value) {
    return escapeHtml(String(value).toUpperCase());
  },
  code(value) {
    return '<code>' + escapeHtml(value) + '</code>';
  },
  raw(value) {
    return String(value);
  },
};
