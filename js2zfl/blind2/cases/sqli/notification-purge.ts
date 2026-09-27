import { Controller, Delete, Query } from '@nestjs/common';
import { PrismaClient } from '@prisma/client';

const prisma = new PrismaClient();

@Controller('notifications')
export class NotificationPurgeController {
  @Delete('purge')
  async purge(@Query('before') before: string) {
    const affected = await prisma.$executeRawUnsafe(
      `DELETE FROM notifications WHERE created_at < '${before}'`
    );
    return { affected };
  }
}
