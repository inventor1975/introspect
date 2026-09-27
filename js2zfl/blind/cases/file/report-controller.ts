import { Request, Response, Router } from 'express';
import * as path from 'node:path';

interface ReportOptions {
  root: string;
  defaultReport: string;
}

export class ReportController {
  constructor(private readonly opts: ReportOptions) {}

  private buildPath(report: string, year: string): string {
    return path.join(this.opts.root, year, report);
  }

  show = (req: Request, res: Response): void => {
    const report = (req.query.report as string) || this.opts.defaultReport;
    const year = (req.query.year as string) || String(new Date().getFullYear());
    const file = this.buildPath(report, year);
    res.sendFile(file, (err) => {
      if (err) res.status(404).json({ error: 'report not available' });
    });
  };

  register(router: Router): void {
    router.get('/reports', this.show);
  }
}

const controller = new ReportController({ root: '/srv/reports', defaultReport: 'summary.pdf' });
export const reportsRouter = Router();
controller.register(reportsRouter);
