import { Controller, Get, Query } from '@nestjs/common';
import { DataSource } from 'typeorm';

@Controller('articles')
export class ArticleQueryController {
  constructor(private readonly dataSource: DataSource) {}

  @Get('by-tag')
  async byTag(@Query('tag') tag: string) {
    return this.dataSource
      .createQueryBuilder()
      .select('a')
      .from('articles', 'a')
      .where('a.tag = ' + "'" + tag + "'")
      .orderBy('a.published_at', 'DESC')
      .getRawMany();
  }
}
