import { Request, Response, Router } from 'express';

class ReportView {
  private readonly title: string;
  private readonly rows: string[];

  constructor(title: string, rows: string[]) {
    this.title = title;
    this.rows = rows;
  }

  toHtml(): string {
    const items = this.rows.map((r) => `<tr><td>${r}</td></tr>`).join('');
    return `<h2>${this.title}</h2><table>${items}</table>`;
  }
}

export class ReportController {
  show(req: Request, res: Response): void {
    const title = (req.query.title as string) || 'Monthly report';
    const view = new ReportView(title, ['Revenue', 'Costs', 'Margin']);
    res.send(view.toHtml());
  }
}

const controller = new ReportController();
export const reports = Router();
reports.get('/reports', controller.show.bind(controller));
