import express from 'express';
import * as fs from 'node:fs';

const UPLOAD = '/srv/gallery/uploads';

const app = express();
app.use(express.json({ limit: '10mb' }));

type UploadBody = { folder: string; name: string; data: string };

app.post('/gallery/upload', (req, res) => {
  const { folder, name, data } = req.body as UploadBody;
  if (!name || !data) {
    return res.status(400).json({ error: 'name and data required' });
  }
  const dir = `${UPLOAD}/${folder || 'misc'}`;
  fs.mkdirSync(dir, { recursive: true });
  fs.writeFileSync(`${dir}/${name}`, Buffer.from(data, 'base64'));
  return res.status(201).json({ path: `${folder}/${name}` });
});

export default app;
