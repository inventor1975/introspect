import { Injectable } from '@nestjs/common';

export interface SignupDto {
  email: string;
  firstName: string;
}

@Injectable()
export class NewsletterService {
  private readonly signups: SignupDto[] = [];

  register(dto: SignupDto): string {
    this.signups.push(dto);
    return this.confirmationPage(dto.firstName, dto.email);
  }

  private confirmationPage(firstName: string, email: string): string {
    return [
      '<section class="confirm">',
      `<h2>Thanks, ${firstName}!</h2>`,
      `<p>We sent a confirmation link to ${email}.</p>`,
      '</section>',
    ].join('');
  }
}
