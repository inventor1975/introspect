import { Controller, Delete, HttpCode, Param, ParseUUIDPipe } from '@nestjs/common';
import { unlink } from 'fs/promises';
import { join } from 'path';

@Controller('snapshots')
export class SnapshotsController {
  private readonly dir = join(process.cwd(), 'var', 'snapshots');

  @Delete(':id')
  @HttpCode(204)
  async remove(@Param('id', new ParseUUIDPipe({ version: '4' })) id: string): Promise<void> {
    await unlink(join(this.dir, `${id}.snap`));
  }
}
