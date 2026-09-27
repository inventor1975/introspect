import { Controller, Get, Injectable, Module, Query } from '@nestjs/common';
import { readFile } from 'fs/promises';
import { join } from 'path';

export class FileRepository<T> {
  constructor(private readonly dir: string) {}

  async load(key: string): Promise<T> {
    const raw = await readFile(join(this.dir, `${key}.json`), 'utf8');
    return JSON.parse(raw) as T;
  }
}

interface PublicProfile {
  displayName: string;
  bio: string;
}

@Injectable()
export class ProfileService {
  private readonly repo = new FileRepository<PublicProfile>(join(process.cwd(), 'data', 'profiles'));

  find(handle: string): Promise<PublicProfile> {
    return this.repo.load(handle);
  }
}

@Controller('profiles')
export class ProfileController {
  constructor(private readonly profiles: ProfileService) {}

  @Get('lookup')
  lookup(@Query('handle') handle: string): Promise<PublicProfile> {
    return this.profiles.find(handle);
  }
}

@Module({ controllers: [ProfileController], providers: [ProfileService] })
export class ProfileModule {}
