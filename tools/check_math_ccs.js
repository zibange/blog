const fs = require('fs');
const katex = require('katex');
const path = process.argv[2];
const md = fs.readFileSync(path, 'utf8');
// 与 article.js 完全相同的正则
const re = /(?<!\\)(\$\$[\s\S]*?\$\$|\$[^$\n]*?\$)/g;
let m, arr = [], errs = [];
while ((m = re.exec(md)) !== null) arr.push(m[1]);
for (const t of arr) {
  const dm = t.startsWith('$$');
  const tex = dm ? t.slice(2, -2) : t.slice(1, -1);
  try { katex.renderToString(tex, { throwOnError: true, displayMode: dm }); }
  catch (e) { errs.push({ tex, msg: e.message }); }
}
// 占位符保护往返一致性
let spans = [];
let src = md.replace(re, mm => { spans.push(mm); return `MATHBLOCKTOKEN${spans.length - 1}MATHBLOCKTOKEN`; });
let restored = src.replace(/MATHBLOCKTOKEN(\d+)MATHBLOCKTOKEN/g, (mm, i) => spans[+i]);
const rtOk = restored === md;
const residualDollar = /\$/.test(src);
console.log('formulas:', arr.length, '| errors:', errs.length, '| roundtrip:', rtOk, '| residual$:', residualDollar);
errs.forEach(e => console.log('ERR:', e.msg, '||', e.tex));
