import { literal } from 'sequelize';
app.get('/q', async (req, res) => {
  await prisma.$queryRawUnsafe(`SELECT * FROM t WHERE n = '${req.query.n}'`);   // EXPECT: REFUTED
  await knex('t').whereRaw(`age > ${req.query.age}`);                           // EXPECT: REFUTED
  db.all('SELECT * FROM t WHERE k = ' + req.query.k, cb);                        // EXPECT: REFUTED (sqlite3)
  await Model.findAll({ where: literal('d < ' + req.query.r) });                 // EXPECT: REFUTED
  await knex('t').where({ id: req.query.id });                                   // clean: an object binds values
  await conn.query('SELECT * FROM t WHERE n = ' + conn.escape(req.query.n));     // clean: mysql2 escape
});
