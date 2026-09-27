import { Body, Controller, Header, HttpCode, Post } from '@nestjs/common';
import { NewsletterService, SignupDto } from './lib/newsletter.service';

@Controller('newsletter')
export class NewsletterController {
  constructor(private readonly newsletter: NewsletterService) {}

  @Post('signup')
  @HttpCode(201)
  @Header('Content-Type', 'text/html')
  signup(@Body() dto: SignupDto): string {
    return this.newsletter.register(dto);
  }
}
