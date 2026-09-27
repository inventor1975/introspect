import * as path from 'node:path';

export class OutsideSandboxError extends Error {
  readonly status = 403;
  constructor(readonly attempted: string) {
    super(`refusing to touch ${attempted}`);
  }
}

export class Sandbox {
  private readonly root: string;

  constructor(root: string) {
    this.root = path.resolve(root);
  }

  locate(relative: string): string {
    const target = path.resolve(this.root, relative);
    const rel = path.relative(this.root, target);
    if (rel === '' || rel.startsWith('..') || path.isAbsolute(rel)) {
      throw new OutsideSandboxError(relative);
    }
    return target;
  }

  get base(): string {
    return this.root;
  }
}
