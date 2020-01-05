#!/usr/bin/env python
import cmarkgfm
import sys


fname = sys.argv[1];
f = open(fname, 'r');
md_text = f.read();
html = cmarkgfm.github_flavored_markdown_to_html(md_text).encode('utf8')
print(html);
