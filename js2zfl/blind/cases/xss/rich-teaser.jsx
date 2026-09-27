import express from 'express';
import React from 'react';
import { renderToString } from 'react-dom/server';

function Teaser({ html }) {
  return <div className="teaser" dangerouslySetInnerHTML={{ __html: html }} />;
}

const app = express();

app.get('/teaser', (req, res) => {
  const markup = renderToString(<Teaser html={req.query.snippet} />);
  res.send(`<!doctype html><html><body>${markup}</body></html>`);
});

export default app;
