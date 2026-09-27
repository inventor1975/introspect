import { Controller, Post, Headers, HttpCode, BadRequestException } from '@nestjs/common';
import { execSync } from 'child_process';

@Controller('tenants')
export class TenantProvisionController {
  @Post('provision')
  @HttpCode(202)
  provision(@Headers('x-tenant-id') tenantId: string) {
    if (!tenantId) {
      throw new BadRequestException('missing tenant header');
    }
    const schema = `tenant_${tenantId}`;
    execSync(`createdb -T template_tenant ${schema}`, { stdio: 'ignore' });
    return { schema };
  }
}
