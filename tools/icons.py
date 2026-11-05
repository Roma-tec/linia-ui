"""Оригинальные пиктограммы и PUA-шрифт для передачи разработчику."""
from pathlib import Path
import json
from fontTools.fontBuilder import FontBuilder
from fontTools.pens.ttGlyphPen import TTGlyphPen

icons = {
 'brush': [[(3,18),(6,21),(20,7),(17,4)],[(2,20),(4,22),(1,23)]],
 'eraser': [[(3,15),(12,6),(21,15),(14,22),(10,22)]],
 'rectangle': [[(3,3),(21,3),(21,5),(3,5)],[(3,19),(21,19),(21,21),(3,21)],[(3,3),(5,3),(5,21),(3,21)],[(19,3),(21,3),(21,21),(19,21)]],
 'text': [[(3,3),(21,3),(21,6),(14,6),(14,21),(10,21),(10,6),(3,6)]],
 'plus': [[(10,3),(14,3),(14,10),(21,10),(21,14),(14,14),(14,21),(10,21),(10,14),(3,14),(3,10),(10,10)]],
 'layers': [[(2,8),(12,2),(22,8),(12,14)],[(2,13),(4,12),(12,17),(20,12),(22,13),(12,20)]],
 'export': [[(10,1),(14,1),(14,12),(18,8),(21,11),(12,20),(3,11),(6,8),(10,12)],[(2,21),(22,21),(22,24),(2,24)]],
 'close': [[(3,5),(5,3),(21,19),(19,21)],[(19,3),(21,5),(5,21),(3,19)]]
}
root=Path('assets/icons');root.mkdir(parents=True,exist_ok=True)
symbols=[]
for name,polys in icons.items():
    paths=''.join('<polygon points="'+' '.join(f'{x},{y}' for x,y in p)+'"/>' for p in polys)
    (root/(name+'.svg')).write_text(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor">{paths}</svg>',encoding='utf8')
    symbols.append(f'<symbol id="{name}" viewBox="0 0 24 24">{paths}</symbol>')
(root/'sprite.svg').write_text('<svg xmlns="http://www.w3.org/2000/svg">'+''.join(symbols)+'</svg>',encoding='utf8')
fb=FontBuilder(1000,isTTF=True);order=['.notdef']+list(icons);fb.setupGlyphOrder(order)
glyphs={'.notdef':TTGlyphPen(None).glyph()}
for name,polys in icons.items():
    pen=TTGlyphPen(None)
    for poly in polys:
        coords=[(round(x/24*1000),round((24-y)/24*1000)) for x,y in poly]
        pen.moveTo(coords[0])
        for point in coords[1:]:pen.lineTo(point)
        pen.closePath()
    glyphs[name]=pen.glyph()
fb.setupGlyf(glyphs);fb.setupHorizontalMetrics({n:(1000,0) for n in order});fb.setupHorizontalHeader(ascent=1000,descent=0)
fb.setupCharacterMap({0xE000+i:n for i,n in enumerate(icons)});fb.setupNameTable({'familyName':'Linia Icons','styleName':'Regular','uniqueFontIdentifier':'LiniaIcons1','fullName':'Linia Icons Regular','psName':'LiniaIcons-Regular'})
fb.setupOS2(sTypoAscender=1000,sTypoDescender=0,usWinAscent=1000,usWinDescent=0);fb.setupPost();fb.setupMaxp();fb.save(root/'linia-icons.ttf');fb.font.flavor='woff2';fb.font.save(root/'linia-icons.woff2')
(root/'map.json').write_text(json.dumps({n:f'U+{0xE000+i:04X}' for i,n in enumerate(icons)},indent=2),encoding='utf8')
print(len(icons),'icons, SVG sprite, TTF, WOFF2')
