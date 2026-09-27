import express, { Request, Response } from 'express';
import { readFile } from 'node:fs/promises';
import path from 'node:path';
import React from 'react';
import { renderToStaticMarkup } from 'react-dom/server';

const ARTICLES = path.join(__dirname, 'articles');
const SLUG = /^[a-z0-9]+(?:-[a-z0-9]+)*$/;

type ArticleProps = { slug: string; body: string };

const Article: React.FC<ArticleProps> = ({ slug, body }) => (
  <article data-slug={slug}>
    <pre>{body}</pre>
  </article>
);

const app = express();

app.get('/articles/:slug', async (req: Request, res: Response) => {
  const slug = req.params.slug.toLowerCase();
  if (!SLUG.test(slug)) {
    res.status(404).send('Not found');
    return;
  }
  const body = await readFile(path.join(ARTICLES, `${slug}.txt`), 'utf8');
  res.type('html').send(renderToStaticMarkup(<Article slug={slug} body={body} />));
});

export default app;
