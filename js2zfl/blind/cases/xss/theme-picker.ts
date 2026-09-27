import express from 'express';
import escapeHtml from 'escape-html';

const app = express();

app.get('/dashboard', (req, res) => {
  const theme = escapeHtml(String(req.query.theme || 'light'));
  const user = escapeHtml(String(req.query.user || ''));
  res.send(`<body class=${theme}><header>Signed in as ${user}</header></body>`);
});

export default app;
