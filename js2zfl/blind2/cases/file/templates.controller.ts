import { Body, Controller, Post, UsePipes, ValidationPipe } from '@nestjs/common';
import { IsString, Length, Matches } from 'class-validator';
import { writeFile } from 'fs/promises';
import { join } from 'path';

export class CreateTemplateDto {
  @IsString()
  @Matches(/^[a-z0-9][a-z0-9-]{0,62}$/)
  name!: string;

  @IsString()
  @Length(1, 100000)
  body!: string;
}

@Controller('templates')
export class TemplatesController {
  private readonly dir = join(process.cwd(), 'templates');

  @Post()
  @UsePipes(new ValidationPipe({ whitelist: true, forbidNonWhitelisted: true }))
  async create(@Body() dto: CreateTemplateDto): Promise<{ saved: string }> {
    await writeFile(join(this.dir, `${dto.name}.hbs`), dto.body, 'utf8');
    return { saved: dto.name };
  }
}
