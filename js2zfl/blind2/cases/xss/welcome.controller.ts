import { Controller, Get, Header, Query } from '@nestjs/common';

@Controller('welcome')
export class WelcomeController {
  @Get()
  @Header('Content-Type', 'text/html; charset=utf-8')
  greet(@Query('name') name: string): string {
    return `<h1>Welcome, ${name}</h1><p>Glad to have you here.</p>`;
  }
}
