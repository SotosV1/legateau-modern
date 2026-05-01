import json
import os
import re
import hashlib
import mimetypes
import time
from pathlib import Path
from urllib.parse import urlparse, unquote

import requests

RESULTS_DIR = Path('/home/ubuntu/.mcp/tool-results')
OUT_DIR = Path('/home/ubuntu/webdev-static-assets/legateau-original-site')
OUT_DIR.mkdir(parents=True, exist_ok=True)

IMAGE_RE = re.compile(r'https?://[^\s\"\'\)<>]+?\.(?:jpg|jpeg|png|webp|gif)(?:\?[^\s\"\'\)<>]*)?', re.IGNORECASE)
CSS_URL_RE = re.compile(r"url\(['\"]?(https?://[^'\")]+\.(?:jpg|jpeg|png|webp|gif)(?:\?[^'\")]+)?)['\"]?\)", re.IGNORECASE)

urls = set()
source_files = []
for path in RESULTS_DIR.glob('*firecrawl*.json'):
    try:
        text = path.read_text(encoding='utf-8')
    except Exception:
        continue
    if 'legateau' not in text:
        continue
    source_files.append(str(path))
    for match in IMAGE_RE.findall(text):
        urls.add(match.replace('\\/', '/'))
    for match in CSS_URL_RE.findall(text):
        urls.add(match.replace('\\/', '/'))

# Add key visible assets identified during browser inspection / Firecrawl scraping.
seed_urls = [
    'http://legateau.gr/storage/logo-2.png',
    'http://legateau.gr/storage/e-bannerespaetpa460x60.jpg',
    'http://legateau.gr/storage/slideshow/slideshow.jpg',
    'http://legateau.gr/storage/slideshow/slideshow2.jpg',
    'http://legateau.gr/storage/slideshow/slideshow3.jpg',
]
urls.update(seed_urls)

# Exclude obvious non-photo UI/legal banners from gallery set but keep logo/banner metadata separately.
photo_exts = {'.jpg', '.jpeg', '.png', '.webp'}
records = []
seen_hashes = set()
headers = {'User-Agent': 'Mozilla/5.0 (compatible; Manus redesign asset collector)'}

for i, url in enumerate(sorted(urls), start=1):
    parsed = urlparse(url)
    ext = Path(parsed.path).suffix.lower()
    if ext not in photo_exts:
        continue
    original_name = unquote(Path(parsed.path).name) or f'asset-{i}{ext}'
    safe_stem = re.sub(r'[^a-zA-Z0-9._-]+', '-', Path(original_name).stem).strip('-').lower()[:80] or f'asset-{i}'
    safe_ext = '.jpg' if ext == '.jpeg' else ext
    digest = hashlib.sha1(url.encode('utf-8')).hexdigest()[:8]
    local_path = OUT_DIR / f'{safe_stem}-{digest}{safe_ext}'
    try:
        response = requests.get(url.replace('http://', 'https://'), headers=headers, timeout=20)
        if response.status_code >= 400:
            response = requests.get(url, headers=headers, timeout=20)
        response.raise_for_status()
        content = response.content
        content_hash = hashlib.sha256(content).hexdigest()
        duplicate = content_hash in seen_hashes
        if not duplicate:
            local_path.write_bytes(content)
            seen_hashes.add(content_hash)
        records.append({
            'url': url,
            'local_path': str(local_path),
            'filename': local_path.name,
            'bytes': len(content),
            'content_type': response.headers.get('content-type', mimetypes.guess_type(str(local_path))[0] or ''),
            'duplicate_content': duplicate,
            'category_hint': '/'.join(parsed.path.split('/')[-3:-1]),
        })
        time.sleep(0.05)
    except Exception as exc:
        records.append({
            'url': url,
            'local_path': '',
            'filename': '',
            'bytes': 0,
            'content_type': '',
            'duplicate_content': False,
            'category_hint': '/'.join(parsed.path.split('/')[-3:-1]),
            'error': str(exc),
        })

manifest = {
    'source_files': source_files,
    'total_urls_found': len(urls),
    'downloaded_unique_files': sum(1 for r in records if r.get('local_path') and not r.get('duplicate_content')),
    'records': records,
}
manifest_path = OUT_DIR / 'asset_manifest.json'
manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding='utf-8')
print(json.dumps({
    'manifest': str(manifest_path),
    'total_urls_found': len(urls),
    'downloaded_unique_files': manifest['downloaded_unique_files'],
    'record_count': len(records),
    'errors': sum(1 for r in records if r.get('error')),
}, ensure_ascii=False, indent=2))
