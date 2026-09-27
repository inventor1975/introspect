const QUEUE_NAME = /^[a-z][a-z0-9_]{0,31}$/;

export class ValidationError extends Error {
  status = 400;
}

export function requireQueueName(value: unknown): string {
  if (typeof value !== 'string' || !QUEUE_NAME.test(value)) {
    throw new ValidationError('invalid queue name');
  }
  return value;
}
