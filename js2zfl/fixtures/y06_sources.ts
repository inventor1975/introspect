import { Controller, Get, Query } from '@nestjs/common';
@Controller('x')
export class X {
  @Get() find(@Query('q') q: string, res: any) { res.send('<p>' + q + '</p>'); }    // EXPECT: REFUTED
}
export const h = ({ query: { name } }, res) => { res.send('<p>' + name + '</p>'); }  // EXPECT: REFUTED
export const m = (req, res) => { res.send('<p>' + req.category + '</p>'); }          // EXPECT: OPEN (set by a middleware)
