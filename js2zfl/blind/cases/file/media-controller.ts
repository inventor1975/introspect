import { Request, Response, Router } from 'express';
import * as fs from 'node:fs';
import * as path from 'node:path';

export class MediaController {
  private readonly root = path.join(process.cwd(), 'media', 'library');

  private sanitize(name: string): string {
    return path.basename(name.replace(/\0/g, ''));
  }

  stream = (req: Request, res: Response): void => {
    const requested = String(req.params.file);
    const file = path.join(this.root, this.sanitize(requested));
    fs.stat(file, (err, st) => {
      if (err || !st.isFile()) {
        res.status(404).json({ error: `no media named ${requested}` });
        return;
      }
      res.setHeader('Content-Length', st.size);
      fs.createReadStream(file).pipe(res);
    });
  };

  mount(router: Router): Router {
    router.get('/media/:file', this.stream);
    return router;
  }
}

export default new MediaController().mount(Router());
