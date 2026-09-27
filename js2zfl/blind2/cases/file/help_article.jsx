const express = require('express');
const fs = require('fs');
const path = require('path');
const React = require('react');
const { renderToStaticMarkup } = require('react-dom/server');

const ARTICLES_DIR = path.join(__dirname, 'help');
const TOPICS = ['billing', 'accounts', 'shipping', 'returns'];

function Article({ topic, text }) {
  return (
    <main className="help">
      <h1>{topic}</h1>
      <pre>{text}</pre>
    </main>
  );
}

const router = express.Router();

router.get('/help/:topic', (req, res) => {
  const topic = req.params.topic;
  if (!TOPICS.includes(topic)) {
    return res.status(404).send(renderToStaticMarkup(<p>Unknown topic {topic}</p>));
  }
  const text = fs.readFileSync(path.join(ARTICLES_DIR, `${topic}.txt`), 'utf8');
  res.send(renderToStaticMarkup(<Article topic={topic} text={text} />));
});

module.exports = router;
