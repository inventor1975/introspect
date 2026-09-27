import { Controller, Get, Header, ParseEnumPipe, Query } from '@nestjs/common';
import { readFile } from 'fs/promises';
import { join } from 'path';

export enum ChartKind {
  Revenue = 'revenue',
  Churn = 'churn',
  Signups = 'signups',
}

@Controller('charts')
export class ChartsController {
  private readonly svgDir = join(__dirname, '..', 'assets', 'charts');

  @Get()
  @Header('Content-Type', 'image/svg+xml')
  async chart(@Query('kind', new ParseEnumPipe(ChartKind)) kind: ChartKind): Promise<string> {
    return readFile(join(this.svgDir, `${kind}.svg`), 'utf8');
  }
}
