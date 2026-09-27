import { Request, Response, Router } from 'express';
import escapeHtml from 'escape-html';

class InvoiceView {
  constructor(private readonly customer: string, private readonly reference: string) {}

  render(): string {
    return `<header><h2>Invoice for ${escapeHtml(this.customer)}</h2><p>Ref: ${escapeHtml(this.reference)}</p></header>`;
  }
}

export class InvoiceController {
  preview = (req: Request, res: Response): void => {
    const view = new InvoiceView(String(req.query.customer ?? ''), String(req.query.ref ?? ''));
    res.send(view.render());
  };
}

const controller = new InvoiceController();
export const invoices = Router();
invoices.get('/invoices/preview', controller.preview);
