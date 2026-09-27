import express, { Request, Response } from 'express';
import React from 'react';
import { renderToString } from 'react-dom/server';

type CommentProps = { author: string; text: string };

function Comment({ author, text }: CommentProps) {
  return (
    <li className="comment">
      <strong>{author}</strong>
      <p>{text}</p>
    </li>
  );
}

const app = express();

app.get('/thread/preview', (req: Request, res: Response) => {
  const author = String(req.query.author ?? 'anonymous');
  const text = String(req.query.text ?? '');
  const markup = renderToString(
    <ul className="thread">
      <Comment author={author} text={text} />
    </ul>
  );
  res.send(`<!doctype html><html><body>${markup}</body></html>`);
});

export default app;
