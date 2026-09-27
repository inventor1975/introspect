import { Controller, Get, Query, ParseIntPipe, DefaultValuePipe } from '@nestjs/common';
import { exec } from 'child_process';
import { promisify } from 'util';

const execAsync = promisify(exec);

@Controller('logs')
export class LogTailController {
  @Get('tail')
  async tail(
    @Query('lines', new DefaultValuePipe(50), ParseIntPipe) lines: number,
  ): Promise<{ lines: string[] }> {
    const { stdout } = await execAsync(`tail -n ${lines} /var/log/app/current.log`);
    return { lines: stdout.split('\n') };
  }
}
