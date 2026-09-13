function q(db, id) { db.query('SELECT * FROM u WHERE id=' + id); }  // id -> sql
module.exports = { q };
