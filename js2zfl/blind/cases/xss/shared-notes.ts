import express, { Request, Response } from 'express';
import { randomUUID } from 'crypto';
import { saveNote, findNote } from './lib/notes-store';

const app = express();
app.use(express.json());

app.post('/notes', (req: Request, res: Response) => {
  const id = randomUUID();
  saveNote({ id, author: String(req.body.author || 'anon'), body: String(req.body.body || ''), createdAt: Date.now() });
  res.status(201).json({ id });
});

app.get('/notes/:id', (req: Request, res: Response) => {
  const note = findNote(req.params.id);
  if (!note) {
    res.status(404).send('<p>Note not found.</p>');
    return;
  }
  res.send(`<article><h3>Note</h3><div>${note.body}</div></article>`);
});

export default app;
