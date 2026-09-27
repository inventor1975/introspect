import { Controller, Get, Req, Res } from '@nestjs/common';
import { Request, Response } from 'express';

@Controller('reports')
export class ReportController {
  @Get('title')
  preview(@Req() req: Request, @Res() res: Response) {
    const heading = req.query.heading as string;
    res.set('Content-Type', 'text/html');
    res.send(`<header class="report"><h2>${heading}</h2></header>`);
  }
}
