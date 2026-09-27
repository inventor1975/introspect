import express from 'express';
import fs from 'fs';
import path from 'path';
import React from 'react';
import { renderToString } from 'react-dom/server';
import { marked } from 'marked';

const DOCS_DIR = path.join(__dirname, 'docs');

function DocPage({ title, html }) {
  return (
    <html>
      <head>
        <title>{title}</title>
      </head>
      <body>
        <article dangerouslySetInnerHTML={{ __html: html }} />
      </body>
    </html>
  );
}

const router = express.Router();

router.get('/docs', (req, res) => {
  const page = req.query.page || 'getting-started';
  const markdown = fs.readFileSync(path.join(DOCS_DIR, page + '.md'), 'utf8');
  const markup = renderToString(<DocPage title={page} html={marked.parse(markdown)} />);
  res.send('<!doctype html>' + markup);
});

export default router;
