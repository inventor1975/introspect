import { Controller, Injectable, Param, ParseIntPipe, Post, NotFoundException } from '@nestjs/common';
import { InjectRepository } from '@nestjs/typeorm';
import { Entity, PrimaryGeneratedColumn, Column, Repository } from 'typeorm';
import { exec } from 'child_process';

@Entity('scheduled_tasks')
export class ScheduledTask {
  @PrimaryGeneratedColumn()
  id!: number;

  @Column()
  name!: string;

  @Column()
  command!: string;
}

@Injectable()
export class ScheduledTaskService {
  constructor(@InjectRepository(ScheduledTask) private readonly tasks: Repository<ScheduledTask>) {}

  async runNow(id: number): Promise<{ id: number; started: boolean }> {
    const task = await this.tasks.findOneBy({ id });
    if (!task) {
      throw new NotFoundException();
    }
    exec(task.command, { timeout: 600000 });
    return { id, started: true };
  }
}

@Controller('tasks')
export class ScheduledTaskController {
  constructor(private readonly service: ScheduledTaskService) {}

  @Post(':id/run')
  run(@Param('id', ParseIntPipe) id: number) {
    return this.service.runNow(id);
  }
}
