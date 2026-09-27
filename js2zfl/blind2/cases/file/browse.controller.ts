import { Controller, Get, Query } from '@nestjs/common';
import { readdir, stat } from 'fs/promises';
import { join } from 'path';

interface Entry {
  name: string;
  size: number;
  directory: boolean;
}

@Controller('browse')
export class BrowseController {
  private readonly root = join(process.cwd(), 'shared');

  @Get()
  async list(@Query('dir') dir = ''): Promise<Entry[]> {
    const base = join(this.root, dir);
    const names = await readdir(base);
    const entries: Entry[] = [];
    for (const name of names) {
      const info = await stat(join(base, name));
      entries.push({ name, size: info.size, directory: info.isDirectory() });
    }
    return entries;
  }
}
