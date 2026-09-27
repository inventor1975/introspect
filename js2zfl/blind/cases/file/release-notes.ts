import { Router } from 'express';
import path from 'node:path';

interface ReleaseEntry {
  version: string;
  file: string;
}

const NOTES_DIR = path.join(__dirname, '..', 'release-notes');
const MANIFEST: ReadonlyArray<ReleaseEntry> = [
  { version: '3.2.0', file: path.join(NOTES_DIR, '3.2.0.pdf') },
  { version: '3.1.4', file: path.join(NOTES_DIR, '3.1.4.pdf') },
  { version: '3.1.0', file: path.join(NOTES_DIR, '3.1.0.pdf') },
];

export const releaseNotes = Router();

releaseNotes.get('/releases/:version/notes', (req, res) => {
  const requested = req.params.version;
  const entry = MANIFEST.find((e) => e.version === requested);
  if (!entry) {
    res.status(404).json({ error: `no notes for ${requested}` });
    return;
  }
  res.download(entry.file, `release-notes-${entry.version}.pdf`);
});
