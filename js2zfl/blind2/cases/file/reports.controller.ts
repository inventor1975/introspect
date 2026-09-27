import { Controller, Get, Header, NotFoundException, Param } from '@nestjs/common';
import { existsSync, readFileSync } from 'fs';
import { join } from 'path';

const REPORT_DIR = join(process.cwd(), 'var', 'reports');

@Controller('reports')
export class ReportsController {
  @Get(':name')
  @Header('Content-Type', 'text/csv')
  getReport(@Param('name') name: string): string {
    const location = join(REPORT_DIR, name);
    if (!existsSync(location)) {
      throw new NotFoundException(`Report ${name} does not exist`);
    }
    return readFileSync(location, 'utf8');
  }
}
