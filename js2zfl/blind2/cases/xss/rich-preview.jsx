import express from 'express';
import React from 'react';
import { renderToString } from 'react-dom/server';

function Preview({ markup }) {
  return (
    <div className="preview">
      <h4>Preview</h4>
      <div className="preview-body" dangerouslySetInnerHTML={{ __html: markup }} />
    </div>
  );
}

const app = express();
app.use(express.urlencoded({ extended: true }));

app.post('/editor/preview', (req, res) => {
  const html = renderToString(<Preview markup={req.body.content} />);
  res.send(`<!doctype html><html><body>${html}</body></html>`);
});

export default app;
