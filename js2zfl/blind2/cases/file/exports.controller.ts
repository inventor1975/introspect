import { Controller, Get, Param, Res, StreamableFile } from '@nestjs/common';
import type { Response } from 'express';
import { createReadStream } from 'fs';
import { join } from 'path';

@Controller('exports')
export class ExportsController {
  @Get('download/:file')
  download(@Param('file') file: string, @Res({ passthrough: true }) res: Response): StreamableFile {
    const stream = createReadStream(join(process.cwd(), 'exports', file));
    res.set({
      'Content-Type': 'application/octet-stream',
      'Content-Disposition': `attachment; filename="${encodeURIComponent(file)}"`,
    });
    return new StreamableFile(stream);
  }
}
