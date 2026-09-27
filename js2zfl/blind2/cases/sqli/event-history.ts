import { Controller, Get, Query } from '@nestjs/common';
import { PrismaClient, Prisma } from '@prisma/client';

const prisma = new PrismaClient();

@Controller('events')
export class EventHistoryController {
  @Get()
  async list(@Query('type') type: string) {
    return prisma.$queryRaw(
      Prisma.sql`SELECT id, type, at FROM events WHERE type = ${type} ORDER BY at DESC`
    );
  }
}
