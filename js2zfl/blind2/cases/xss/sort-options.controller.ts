import { BadRequestException, Controller, Get, Header, Query } from '@nestjs/common';

enum SortOrder {
  Newest = 'newest',
  Oldest = 'oldest',
  Popular = 'popular',
}

@Controller('listings')
export class ListingsController {
  @Get()
  @Header('Content-Type', 'text/html')
  list(@Query('sort') sort: string): string {
    if (!(Object.values(SortOrder) as string[]).includes(sort)) {
      throw new BadRequestException('Unknown sort order');
    }
    return `<p class="sort">Sorted by ${sort}</p>`;
  }
}
