import { Controller, Get, Param } from '@nestjs/common';
import { DataSource } from 'typeorm';

@Controller('resources')
export class ResourceDetailController {
  constructor(private readonly ds: DataSource) {}

  @Get(':id')
  async detail(@Param('id') id: string) {
    return this.ds.query(`SELECT * FROM resources WHERE id = ${id}`);
  }
}
