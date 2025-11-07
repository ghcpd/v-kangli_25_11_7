from pathlib import Path
p = Path('debug_touch.txt')
with p.open('w', encoding='utf-8') as f:
    f.write('debug')
print('wrote', p.resolve())
