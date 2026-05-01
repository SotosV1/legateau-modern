import json
import re
from pathlib import Path

assets_dir = Path('/home/ubuntu/webdev-static-assets/legateau-original-site')
manifest = json.loads((assets_dir / 'asset_manifest.json').read_text(encoding='utf-8'))
upload_text = (assets_dir / 'uploaded_assets.txt').read_text(encoding='utf-8')

upload_map = {}
for line in upload_text.splitlines():
    m = re.match(r'\[SUCCESS\] \./(.+?) -> (/.+)$', line.strip())
    if m:
        upload_map[m.group(1)] = m.group(2)
# fallback parse pair order if summary truncated for any reason
current = None
for line in upload_text.splitlines():
    m = re.search(r'Uploading file \(webdev private\): \./(.+?) ', line)
    if m:
        current = m.group(1)
    m = re.search(r'Storage Path: (/.+)$', line)
    if m and current:
        upload_map.setdefault(current, m.group(1))
        current = None

records = []
for rec in manifest['records']:
    filename = rec.get('filename')
    if not filename or rec.get('duplicate_content') or filename not in upload_map:
        continue
    src = upload_map[filename]
    orig = rec.get('url', '')
    hint = rec.get('category_hint', '')
    lower = (filename + ' ' + hint + ' ' + orig).lower()
    if 'logo-2' in lower:
        category = 'brand'
        title = 'Le Gateau'
    elif 'espa' in lower:
        category = 'brand'
        title = 'ESPA'
    elif 'slideshow' in lower:
        category = 'slideshow'
        title = 'Στιγμή Le Gateau'
    elif 'wedding' in lower or 'gamos' in lower or 'p1100049' in lower or 'p1090984' in lower or 'dsc-2873' in lower:
        category = 'Γάμος'
        title = 'Γάμος'
    elif 'birthdays' in lower or 'genethlia' in lower:
        category = 'Γενέθλια'
        title = 'Γενέθλια'
    elif 'vaftisi' in lower or 'muffin' in lower or 'wp-' in lower:
        category = 'Βάφτιση'
        title = 'Βάφτιση'
    elif 'christmas' in lower or 'p1080351' in lower or 'christ' in lower:
        category = 'Χριστούγεννα'
        title = 'Χριστούγεννα'
    elif 'pastes' in lower or '1574' in lower or '1569' in lower or '1227' in lower or '123919' in lower:
        category = 'Πάστες'
        title = 'Πάστες'
    elif 'tartes' in lower:
        category = 'Τάρτες'
        title = 'Τάρτες'
    elif 'siropiasta' in lower or '59062' in lower:
        category = 'Σιροπιαστά'
        title = 'Σιροπιαστά'
    elif 'sokolatakia' in lower:
        category = 'Σοκολατάκια'
        title = 'Σοκολατάκια'
    elif 'pastakia' in lower:
        category = 'Παστάκια'
        title = 'Παστάκια'
    elif 'pagwto' in lower:
        category = 'Παγωτό'
        title = 'Παγωτό'
    elif 'almyra' in lower:
        category = 'Αλμυρά'
        title = 'Αλμυρά'
    elif 'tourtes' in lower:
        category = 'Τούρτες'
        title = 'Τούρτες'
    elif 'about-us' in lower:
        category = 'Ιστορία'
        title = 'Το εργαστήριο μας'
    else:
        category = 'Le Gateau'
        title = 'Δημιουργία Le Gateau'
    records.append({
        'src': src,
        'originalUrl': orig,
        'filename': filename,
        'category': category,
        'title': title,
        'bytes': rec.get('bytes', 0),
    })

# Sort: brand first in constants, gallery excludes brand/espa/background duplicates.
brand = [r for r in records if r['category'] == 'brand']
photos = [r for r in records if r['category'] != 'brand']

featured_order = ['Τούρτες','Γάμος','Γενέθλια','Βάφτιση','Πάστες','Τάρτες','Παγωτό','Σοκολατάκια','Παστάκια','Σιροπιαστά','Αλμυρά','Χριστούγεννα']
category_representatives = []
seen = set()
for cat in featured_order:
    for r in photos:
        if r['category'] == cat and cat not in seen:
            category_representatives.append(r)
            seen.add(cat)
            break

# Pick an editorial strip of strong images from original photos.
editorial = []
for wanted in ['slideshow','Ιστορία','Τούρτες','Γάμος','Βάφτιση','Γενέθλια']:
    for r in photos:
        if r['category'] == wanted:
            editorial.append(r)
            break

hero_generated = {
    'hero': 'https://d2xsxph8kpxj0f.cloudfront.net/310519663452251579/JTzhiMxd3CenxAByqdzrbz/legateau-editorial-hero-PkVupqiJoZfKus2nFjiLkW.webp',
    'paper': 'https://d2xsxph8kpxj0f.cloudfront.net/310519663452251579/JTzhiMxd3CenxAByqdzrbz/legateau-paper-texture-hXKKSsTNjCyqcFzUseAVgx.webp',
    'flourish': 'https://d2xsxph8kpxj0f.cloudfront.net/310519663452251579/JTzhiMxd3CenxAByqdzrbz/legateau-flourish-divider-VQ8X2fZpYUVwmxjyLQNcQZ.webp',
}

out = Path('/home/ubuntu/legateau-modern/client/src/data/siteData.ts')
out.parent.mkdir(parents=True, exist_ok=True)
ts_content = """// Design philosophy reminder: Contemporary Pâtisserie Editorial — warm craft, asymmetrical editorial rhythm, tactile product cards, refined Greek content, and subtle pastry-box interactions.
// This file centralizes scraped Firecrawl content and durable uploaded image paths so components can preserve every discovered site photo without storing media inside the project.

export const generatedAssets = __GENERATED__ as const;

export const brandAssets = __BRAND__ as const;

export const allSitePhotos = __PHOTOS__ as const;

export const categoryRepresentatives = __CATEGORIES__ as const;

export const editorialPhotos = __EDITORIAL__ as const;

export const productCategories = [
  { name: 'Τούρτες', note: 'Custom cakes and celebration centrepieces' },
  { name: 'Τάρτες', note: 'Fruit, cream, and crisp pastry textures' },
  { name: 'Πάστες', note: 'Individual patisserie pieces for everyday rituals' },
  { name: 'Σοκολατάκια', note: 'Chocolate bites and refined treats' },
  { name: 'Γάμος', note: 'Wedding sweets and dessert tables' },
  { name: 'Βάφτιση', note: 'Baptism celebrations and playful details' },
  { name: 'Γενέθλια', note: 'Birthday cakes made to be remembered' },
  { name: 'Παστάκια', note: 'Small-format sweets for sharing' },
  { name: 'Σιροπιαστά', note: 'Traditional syrup sweets' },
  { name: 'Παγωτό', note: 'Cold desserts for warm days' },
  { name: 'Αλμυρά', note: 'Savory pastry selections' },
  { name: 'Χριστούγεννα', note: 'Seasonal festive craft' },
] as const;

export const contactDetails = {
  phone: '2381021555',
  email: 'legateauedessa@gmail.com',
  addressShort: 'Αναπαύσεως 3, Έδεσσα 58200',
  addressOriginalHome: 'Αναλήψεως 3, 58200, Έδεσσα',
  hoursWeekdays: 'Δευτέρα–Παρασκευή: 7:30–22:30',
  hoursWeekend: 'Σάββατο–Κυριακή: 8:00–22:30',
  instagram: 'https://www.instagram.com/legateauedessa/',
  facebook: 'https://www.facebook.com/Le-gateau-%CE%96%CE%B1%CF%87%CE%B1%CF%81%CE%BF%CF%80%CE%BB%CE%B1%CF%83%CF%84%CE%B5%CE%AF%CE%BF-K%CE%B1%CF%86%CE%AD-253904914784263/',
};
"""
ts_content = ts_content.replace('__GENERATED__', json.dumps(hero_generated, ensure_ascii=False, indent=2))
ts_content = ts_content.replace('__BRAND__', json.dumps(brand, ensure_ascii=False, indent=2))
ts_content = ts_content.replace('__PHOTOS__', json.dumps(photos, ensure_ascii=False, indent=2))
ts_content = ts_content.replace('__CATEGORIES__', json.dumps(category_representatives, ensure_ascii=False, indent=2))
ts_content = ts_content.replace('__EDITORIAL__', json.dumps(editorial, ensure_ascii=False, indent=2))
out.write_text(ts_content, encoding='utf-8')

print(json.dumps({
    'records': len(records),
    'photos': len(photos),
    'brand': len(brand),
    'categoryRepresentatives': len(category_representatives),
    'editorial': len(editorial),
    'missingUploads': len([r for r in manifest['records'] if r.get('filename') and not r.get('duplicate_content') and r.get('filename') not in upload_map]),
    'out': str(out),
}, ensure_ascii=False, indent=2))
