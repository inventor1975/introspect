'use strict';

function page(title, body) {
  return [
    '<!doctype html>',
    '<html><head><meta charset="utf-8"><title>' + title + '</title>',
    '<link rel="stylesheet" href="/static/app.css"></head>',
    '<body><main>' + body + '</main></body></html>',
  ].join('\n');
}

function card(heading, text) {
  return `<section class="card"><h3>${heading}</h3><p>${text}</p></section>`;
}

module.exports = { page, card };
