# -*- coding: utf-8 -*-
"""临时脚本：找出 md 中含 CJK 字符的 KaTeX 公式（发布前自检用）"""
import re
import sys

path = sys.argv[1]
s = open(path, encoding='utf-8').read()
pat = re.compile(r'(?<!\\)(\$\$[\s\S]*?\$\$|\$[^$\n]*?\$)')
found = 0
for m in pat.finditer(s):
    t = m.group(0)
    if re.search(r'[\u4e00-\u9fff]', t):
        line = s[:m.start()].count('\n') + 1
        found += 1
        print('LINE', line, ':', t[:150])
print('total CJK-in-math:', found)
