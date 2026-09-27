// parsecheck.js — every corpus file must parse with @babel/parser, with the plugins js2zfl/jsast.js uses
// (and errorRecovery OFF, so a file that only parses "with recovery" is reported).
//   node js2zfl/blind/parsecheck.js <file>...      -> one line per failure; exit 1 if any
const parser = require(require.resolve("@babel/parser", { paths: [__dirname + "/.."] }));
const fs = require("fs");
let bad = 0;
for (const f of process.argv.slice(2)) {
  try {
    parser.parse(fs.readFileSync(f, "utf8"), {
      sourceType: "unambiguous", errorRecovery: false,
      plugins: ["jsx", "typescript", "classProperties", "classPrivateMethods", "optionalChaining",
                "nullishCoalescingOperator", "objectRestSpread", "decorators-legacy", "dynamicImport"],
    });
  } catch (e) { bad++; console.log(`PARSE ERROR ${f}: ${e.message}`); }
}
console.log(`${process.argv.length - 2 - bad} parsed, ${bad} failed`);
process.exit(bad ? 1 : 0);
