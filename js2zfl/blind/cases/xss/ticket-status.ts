import express, { Request, Response, NextFunction } from 'express';

const app = express();

const TICKET_ID = /^[A-Z]{2,5}-\d{1,6}$/;

function requireTicketId(req: Request, res: Response, next: NextFunction) {
  if (!TICKET_ID.test(req.params.ticket)) {
    res.status(400).send('<p>Malformed ticket id.</p>');
    return;
  }
  next();
}

app.get('/tickets/:ticket', requireTicketId, (req: Request, res: Response) => {
  const ticket = req.params.ticket;
  res.send(`<h1>Ticket ${ticket}</h1><p>Status: open</p>`);
});

export default app;
