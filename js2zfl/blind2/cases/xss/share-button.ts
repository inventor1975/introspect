import express from 'express';
import { escapeHtml } from './lib/html';

const app = express();

app.get('/share', (req, res) => {
  const title = String(req.query.title || 'Untitled');
  const safeTitle = escapeHtml(title);
  res.send(`<button type="button" onclick="shareItem('${safeTitle}')">Share</button>`);
});

export default app;
