import express, { Request, Response } from 'express';
import { promises as fs } from 'fs';
import * as path from 'path';

class MarkdownStore {
  private static readonly SLUG = /^[a-z0-9]+(?:-[a-z0-9]+)*$/;

  constructor(private readonly root: string) {}

  private locate(slug: string): string {
    if (!MarkdownStore.SLUG.test(slug)) {
      throw new Error(`invalid slug: ${slug}`);
    }
    return path.join(this.root, `${slug}.md`);
  }

  async read(slug: string): Promise<string> {
    return fs.readFile(this.locate(slug), 'utf8');
  }

  async save(slug: string, body: string): Promise<void> {
    await fs.writeFile(this.locate(slug), body, 'utf8');
  }
}

const store = new MarkdownStore(path.join(__dirname, 'wiki'));
const app = express();
app.use(express.json());

app.get('/wiki/:slug', async (req: Request, res: Response) => {
  try {
    res.type('text/markdown').send(await store.read(req.params.slug));
  } catch (e) {
    res.status(404).json({ error: (e as Error).message });
  }
});

app.put('/wiki/:slug', async (req: Request, res: Response) => {
  try {
    await store.save(req.params.slug, String(req.body.content));
    res.sendStatus(204);
  } catch (e) {
    res.status(400).json({ error: (e as Error).message });
  }
});

export default app;
