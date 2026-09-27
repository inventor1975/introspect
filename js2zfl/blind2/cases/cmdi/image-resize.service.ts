import { Injectable, Controller, Post, Body } from '@nestjs/common';
import { execSync } from 'child_process';

export class ResizeRequest {
  imageId!: string;
  width!: string;
  height!: string;
}

@Injectable()
export class ImageResizeService {
  resize(imageId: string, width: string, height: string): string {
    const input = `/srv/images/${imageId}.png`;
    const output = `/srv/images/${imageId}-${width}x${height}.png`;
    execSync(`magick ${input} -resize ${width}x${height}! ${output}`);
    return output;
  }
}

@Controller('images')
export class ImageResizeController {
  constructor(private readonly images: ImageResizeService) {}

  @Post('resize')
  resize(@Body() dto: ResizeRequest) {
    const path = this.images.resize(dto.imageId, dto.width, dto.height);
    return { path };
  }
}
