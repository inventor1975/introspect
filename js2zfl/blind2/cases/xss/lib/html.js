'use strict';

const ENTITIES = {
  '&': '&amp;',
  '<': '&lt;',
  '>': '&gt;',
  '"': '&quot;',
  "'": '&#39;',
};

function escapeHtml(value) {
  return String(value).replace(/[&<>"']/g, (ch) => ENTITIES[ch]);
}

function stripTags(value) {
  return String(value).replace(/<[^>]*>/g, '');
}

function layout(title, body) {
  return (
    '<!doctype html><html><head><meta charset="utf-8"><title>' +
    title +
    '</title><link rel="stylesheet" href="/static/site.css"></head><body>' +
    body +
    '</body></html>'
  );
}

module.exports = { escapeHtml, stripTags, layout };
