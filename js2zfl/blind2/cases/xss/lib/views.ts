import { escapeHtml } from './html';

export function noticeBox(message: string, level: 'info' | 'warn' = 'info'): string {
  return `<div class="notice notice-${level}">${message}</div>`;
}

export function alertBox(message: string, dismissible = true): string {
  const button = dismissible ? '<button class="close" aria-label="Close">&times;</button>' : '';
  return `<div class="alert" role="alert">${escapeHtml(message)}${button}</div>`;
}

export function tableRow(cells: string[]): string {
  return '<tr>' + cells.map((c) => `<td>${c}</td>`).join('') + '</tr>';
}
