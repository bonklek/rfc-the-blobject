from pathlib import Path
import re
import cairosvg
src=Path('docs/assets/figures/figure-06-storage-admission-model.svg').read_text(encoding='utf-8')
src=re.sub(r'<tspan baseline-shift="sub" font-size="\d+">([^<]+)</tspan>',r'_\1',src)
src=src.replace('≲','&lt;~')
p=Path('audits/visual-qa/final/figure-06-portable-preview.svg')
p.write_text(src,encoding='utf-8')
cairosvg.svg2png(url=str(p),write_to=str(p.with_suffix('.png')))
