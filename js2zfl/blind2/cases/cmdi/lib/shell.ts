export function shellEscape(value: string): string {
  return "'" + String(value).replace(/'/g, "'\\''") + "'";
}

export function shellJoin(args: string[]): string {
  return args.map(shellEscape).join(' ');
}
