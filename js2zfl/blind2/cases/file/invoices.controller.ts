import { Controller, Get, NotFoundException, Param, ParseIntPipe, StreamableFile } from '@nestjs/common';
import { createReadStream, existsSync } from 'fs';
import { join } from 'path';

@Controller('invoices')
export class InvoicesController {
  private readonly storage = join(process.cwd(), 'storage', 'invoices');

  @Get(':number/pdf')
  pdf(@Param('number', ParseIntPipe) invoiceNumber: number): StreamableFile {
    const file = join(this.storage, `INV-${invoiceNumber}.pdf`);
    if (!existsSync(file)) {
      throw new NotFoundException();
    }
    return new StreamableFile(createReadStream(file), { type: 'application/pdf' });
  }
}
