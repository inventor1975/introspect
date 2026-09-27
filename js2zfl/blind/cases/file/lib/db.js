'use strict';
const { Pool } = require('pg');

const pool = new Pool({ connectionString: process.env.DATABASE_URL });

async function findUser(id) {
  const { rows } = await pool.query('SELECT id, name, avatar FROM users WHERE id = $1', [id]);
  return rows[0] || null;
}

async function setUserAvatar(id, avatar) {
  await pool.query('UPDATE users SET avatar = $1 WHERE id = $2', [avatar, id]);
}

async function insertUpload(record) {
  await pool.query(
    'INSERT INTO uploads (id, storage_key, original_name, mime) VALUES ($1, $2, $3, $4)',
    [record.id, record.storageKey, record.originalName, record.mime]
  );
}

async function findUpload(id) {
  const { rows } = await pool.query(
    'SELECT id, storage_key AS "storageKey", original_name AS "originalName", mime FROM uploads WHERE id = $1',
    [id]
  );
  return rows[0] || null;
}

module.exports = { findUser, setUserAvatar, insertUpload, findUpload };
