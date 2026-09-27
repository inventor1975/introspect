import express from 'express';
import React from 'react';
import { renderToString } from 'react-dom/server';

function Preview({ source }) {
  return (
    <div className="preview">
      <h4>Preview</h4>
      <pre className="preview-body">{source}</pre>
    </div>
  );
}

const app = express();
app.use(express.urlencoded({ extended: true }));

app.post('/markdown/preview', (req, res) => {
  const html = renderToString(<Preview source={req.body.content} />);
  res.send(`<!doctype html><html><body>${html}</body></html>`);
});

export default app;
