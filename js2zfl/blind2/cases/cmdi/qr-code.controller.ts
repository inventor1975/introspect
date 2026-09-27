import { Controller, Get, Injectable, Param, ParseUUIDPipe, Res } from '@nestjs/common';
import type { Response } from 'express';
import { execSync } from 'child_process';

@Injectable()
export class QrCodeService {
  private readonly baseUrl = 'https://tickets.example.org/t/';

  render(ticketId: string): Buffer {
    return execSync(`qrencode -o - -s 6 "${this.baseUrl}${ticketId}"`);
  }
}

@Controller('tickets')
export class QrCodeController {
  constructor(private readonly qr: QrCodeService) {}

  @Get(':id/qr.png')
  qrCode(@Param('id', new ParseUUIDPipe({ version: '4' })) id: string, @Res() res: Response) {
    const png = this.qr.render(id);
    res.type('png').send(png);
  }
}
