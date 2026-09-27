import React from 'react';
import { Pool } from 'pg';

const pool = new Pool();

async function loadRoster(teamId) {
  'use server';
  const result = await pool.query(
    'SELECT id, name, role FROM roster WHERE team_id = $1 ORDER BY name',
    [teamId]
  );
  return result.rows;
}

export default async function TeamRoster({ teamId }) {
  const members = await loadRoster(teamId);
  return (
    <div className="roster">
      {members.map((m) => (
        <span key={m.id}>{m.name}</span>
      ))}
    </div>
  );
}
