import { Controller, Get, Param } from '@nestjs/common';
import { DataSource } from 'typeorm';

@Controller('documents')
export class DocumentFetchController {
  constructor(private readonly ds: DataSource) {}

  @Get(':id')
  async fetch(@Param('id') id: string) {
    return this.ds
      .createQueryBuilder()
      .select('d')
      .from('documents', 'd')
      .where('d.id = :id', { id })
      .getRawOne();
  }
}
