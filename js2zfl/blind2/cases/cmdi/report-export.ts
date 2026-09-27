import express, { Request, Response } from 'express';
import { exec } from 'child_process';

class ReportService {
  constructor(private readonly outDir: string) {}

  runExport(reportId: number, format: string): Promise<string> {
    const target = `${this.outDir}/report-${reportId}.${format}`;
    const cmd = `libreoffice --headless --convert-to ${format} --outdir ${this.outDir} /srv/reports/${reportId}.odt`;
    return new Promise((resolve, reject) => {
      exec(cmd, (err) => (err ? reject(err) : resolve(target)));
    });
  }
}

const service = new ReportService('/tmp/reports');
const app = express();

app.get('/reports/:id/export', async (req: Request, res: Response) => {
  const format = (req.query.format as string) || 'pdf';
  try {
    const file = await service.runExport(parseInt(req.params.id, 10), format);
    res.download(file);
  } catch {
    res.status(500).end();
  }
});

export default app;
