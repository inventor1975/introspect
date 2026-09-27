import { Body, Controller, Post, UsePipes, ValidationPipe } from '@nestjs/common';
import { IsIn, IsInt, Min, Max } from 'class-validator';
import { execSync } from 'child_process';

export class ConvertAudioDto {
  @IsIn(['mp3', 'ogg', 'flac', 'wav'])
  format!: string;

  @IsInt()
  @Min(0)
  @Max(1000000)
  trackId!: number;
}

@Controller('audio')
export class AudioConvertController {
  @Post('convert')
  @UsePipes(new ValidationPipe({ whitelist: true, forbidNonWhitelisted: true, transform: true }))
  convert(@Body() dto: ConvertAudioDto) {
    const src = `/srv/audio/${dto.trackId}.wav`;
    const out = `/srv/audio/out/${dto.trackId}.${dto.format}`;
    execSync(`ffmpeg -y -loglevel error -i ${src} ${out}`);
    return { out };
  }
}
