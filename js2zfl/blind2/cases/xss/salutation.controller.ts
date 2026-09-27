import { Controller, Get, Header, Query } from '@nestjs/common';
import * as he from 'he';

@Controller('salutation')
export class SalutationController {
  @Get()
  @Header('Content-Type', 'text/html; charset=utf-8')
  greet(@Query('name') name: string): string {
    const display = he.encode(name ?? 'guest');
    return `<h1>Welcome, ${display}</h1><p>Glad to have you here.</p>`;
  }
}
