import { Controller, Get, Query, Res } from '@nestjs/common';
import { Response } from 'express';

@Controller('greetings')
export class GreetingController {
  @Get()
  greet(@Query('to') to: string, @Res() res: Response): void {
    const recipient = to ?? 'world';
    res.set('Content-Type', 'text/html');
    res.send(`<h1>Greetings, ${recipient}!</h1>`);
  }
}
