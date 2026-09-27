const express = require('express');

const router = express.Router();

router.get('/articles', (req, res) => {
  const filter = req.query.filter || '';
  const pageNo = Number.parseInt(req.query.p, 10) || 1;
  const q = encodeURIComponent(filter);
  res.send(`
    <nav id="pager"></nav>
    <script>
      var pagerFilter = '${q}';
      var pagerPage = ${pageNo};
      window.renderPager(document.getElementById('pager'), pagerFilter, pagerPage);
    </script>`);
});

module.exports = router;
