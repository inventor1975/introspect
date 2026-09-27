import { Pool, QueryResult } from 'pg';

const pool = new Pool({ connectionString: process.env.PG_URL });

// Inlines the caller-supplied predicate into the query text.
export async function runRawFilter(fragment: string): Promise<QueryResult> {
  const text = `SELECT ts, host, value FROM metrics WHERE ${fragment} ORDER BY ts DESC LIMIT 200`;
  return pool.query(text);
}

// Fixed statement text, values are bound positionally.
export async function runBoundQuery(text: string, params: unknown[]): Promise<QueryResult> {
  return pool.query(text, params);
}

export { pool };
