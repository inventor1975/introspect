import express from 'express';
import React from 'react';
import { renderToString } from 'react-dom/server';
import { execSync } from 'child_process';

function BuildInfo({ tag, sha }) {
  return (
    <section className="build-info">
      <h2>Build {tag}</h2>
      <code>{sha}</code>
    </section>
  );
}

const app = express();

app.get('/builds/describe', (req, res) => {
  const ref = req.query.ref || 'HEAD';
  const sha = execSync('git rev-parse ' + ref, { cwd: '/srv/app' }).toString().trim();
  const tag = execSync(`git describe --tags ${ref}`, { cwd: '/srv/app' }).toString().trim();
  res.send('<!doctype html>' + renderToString(<BuildInfo tag={tag} sha={sha} />));
});

export default app;
