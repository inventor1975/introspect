import { Router } from 'express';
import { readFile } from 'node:fs/promises';
import { join, extname } from 'node:path';

const SNIPPETS = join(process.cwd(), 'snippets');
const LANG_BY_EXT = { '.js': 'javascript', '.py': 'python', '.go': 'go', '.rs': 'rust' };

const router = Router();

router.get('/snippets/:collection/:file', async (req, res, next) => {
  const { collection, file } = req.params;
  const location = join(SNIPPETS, collection, file);
  try {
    const code = await readFile(location, { encoding: 'utf8' });
    res.json({
      collection,
      file,
      language: LANG_BY_EXT[extname(file)] ?? 'text',
      lines: code.split('\n').length,
      code,
    });
  } catch (err) {
    next(err);
  }
});

export default router;
