const { exec } = require('child_process');

const EXPORT_DIR = '/var/exports';

function buildTarCommand(bundleName, sourceDir) {
  return `tar -czf ${EXPORT_DIR}/${bundleName}.tar.gz -C ${sourceDir} .`;
}

function createBundle(bundleName, sourceDir) {
  const command = buildTarCommand(bundleName, sourceDir);
  return new Promise((resolve, reject) => {
    exec(command, (err, stdout, stderr) => {
      if (err) return reject(new Error(stderr || err.message));
      resolve(`${EXPORT_DIR}/${bundleName}.tar.gz`);
    });
  });
}

module.exports = { createBundle };
