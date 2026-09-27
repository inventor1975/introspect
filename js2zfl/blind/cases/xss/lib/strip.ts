const SCRIPT_BLOCK = /<script\b[^>]*>[\s\S]*?<\/script>/gi;

export function stripScripts(markup: string): string {
  return markup.replace(SCRIPT_BLOCK, '');
}

export function collapseWhitespace(text: string): string {
  return text.replace(/\s+/g, ' ').trim();
}
