import { Controller, Get, Query } from '@nestjs/common';
import { getRepository } from 'typeorm';
import { Contact } from './entities/contact';

@Controller('crm/contacts')
export class ContactSearchController {
  @Get()
  async search(@Query('company') company: string) {
    const repo = getRepository(Contact);
    return repo.find({ where: { company }, take: 100 });
  }
}
