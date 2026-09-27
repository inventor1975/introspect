import { Controller, Get, Param, Res } from '@nestjs/common';
import { Response } from 'express';
import escapeHtml from 'escape-html';

@Controller('welcome')
export class WelcomeController {
  @Get(':team')
  show(@Param('team') team: string, @Res() res: Response): void {
    const heading = `<h1>Welcome to team ${escapeHtml(team)}</h1>`;
    res.set('Content-Type', 'text/html');
    res.send(heading + '<p>Your onboarding checklist is below.</p>');
  }
}
