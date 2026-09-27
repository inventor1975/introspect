import express, { Request, Response } from 'express';

class PageBuilder {
  private parts: string[] = [];

  heading(text: string): this {
    this.parts.push(`<h1>${text}</h1>`);
    return this;
  }

  paragraph(text: string): this {
    this.parts.push(`<p>${text}</p>`);
    return this;
  }

  build(): string {
    return `<main>${this.parts.join('\n')}</main>`;
  }
}

const app = express();
app.use(express.urlencoded({ extended: true }));

app.post('/guestbook/preview', (req: Request, res: Response) => {
  const page = new PageBuilder().heading('Preview').paragraph(req.body.entry);
  res.send(page.build());
});

export default app;
