import { Router, Request, Response } from 'express';

const TEMPLATE = `
<table class="invite">
  <tr><td>Hi {{name}},</td></tr>
  <tr><td>{{inviter}} invited you to join the workspace.</td></tr>
</table>`;

export const invitePreview = Router();

invitePreview.get('/invites/preview', (req: Request, res: Response) => {
  const name = String(req.query.name ?? 'there');
  const inviter = String(req.query.inviter ?? 'A teammate');
  const html = TEMPLATE.replace('{{name}}', name).replace('{{inviter}}', inviter);
  res.send(html);
});
