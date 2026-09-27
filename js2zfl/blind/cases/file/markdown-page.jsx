import express from 'express';
import fs from 'fs';
import path from 'path';
import React from 'react';
import { renderToString } from 'react-dom/server';
import { marked } from 'marked';

const PAGES = path.join(__dirname, 'pages');

function Page({ title, html }) {
  return (
    <html>
      <head>
        <title>{title}</title>
      </head>
      <body>
        <main dangerouslySetInnerHTML={{ __html: html }} />
      </body>
    </html>
  );
}

const app = express();

app.get('/pages/view', (req, res) => {
  const slug = req.query.slug || 'home';
  const source = fs.readFileSync(path.join(PAGES, `${slug}.md`), 'utf8');
  const markup = renderToString(<Page title={slug} html={marked.parse(source)} />);
  res.type('html').send('<!doctype html>' + markup);
});

export default app;
