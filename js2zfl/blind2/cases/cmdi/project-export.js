const express = require('express');
const { createBundle } = require('./lib/archive');

const app = express();
app.use(express.json());

app.post('/projects/:id/export', async (req, res, next) => {
  try {
    const bundle = req.body.name || `project-${req.params.id}`;
    const file = await createBundle(bundle, `/data/projects/${Number(req.params.id)}`);
    res.json({ file });
  } catch (err) {
    next(err);
  }
});

module.exports = app;
