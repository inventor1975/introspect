export interface Note {
  id: string;
  author: string;
  body: string;
  createdAt: number;
}

const notes = new Map<string, Note>();

export function saveNote(note: Note): void {
  notes.set(note.id, note);
}

export function findNote(id: string): Note | undefined {
  return notes.get(id);
}
