import * as path from 'node:path';

export const THEMES_ROOT = path.resolve(__dirname, '..', 'themes');

/**
 * Resolve a theme-relative asset path under the given base directory.
 */
export function resolveUnder(base: string, relative: string): string {
  const cleaned = relative.trim().replace(/\\/g, '/');
  return path.join(base, cleaned);
}

export function extensionOf(file: string): string {
  return path.extname(file).toLowerCase();
}
