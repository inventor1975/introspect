import { Controller, Get, Query, InternalServerErrorException } from '@nestjs/common';
import { exec } from 'child_process';

@Controller('repo')
export class RepoHistoryController {
  private readonly repoDir = '/var/lib/app/repo';

  @Get('history')
  history(@Query('branch') branch: string, @Query('limit') limit = '20'): Promise<string[]> {
    const cmd = 'git -C ' + this.repoDir + ' log --oneline -n ' + limit + ' ' + branch;
    return new Promise((resolve, reject) => {
      exec(cmd, (err, stdout) => {
        if (err) {
          return reject(new InternalServerErrorException('git failed'));
        }
        resolve(stdout.split('\n').filter(Boolean));
      });
    });
  }
}
