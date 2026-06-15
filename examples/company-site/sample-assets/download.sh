#!/usr/bin/env bash
# 批量下载示例素材（Unsplash 公共图床，~20 张高清图，约 6-8 MB）
# 用法： bash sample-assets/download.sh

set -euo pipefail
cd "$(dirname "$0")"

mkdir -p products news

UNSPLASH="https://images.unsplash.com"
PARAMS="auto=format&fit=crop&w=1600&q=80"

dl() {
  # dl <photo_id> <out_path>
  local id="$1"
  local out="$2"
  if [ -f "$out" ]; then
    echo "  skip  $out"
    return
  fi
  echo "  fetch $out"
  curl -fsSL "${UNSPLASH}/${id}?${PARAMS}" -o "$out"
}

echo "→ products/"
dl photo-1592750475338-74b7b21085ab products/phone-pro-16-cover.jpg
dl photo-1511707171634-5f897ff02aa9 products/phone-pro-16-1.jpg
dl photo-1574944985070-8f3ebc6b79d2 products/phone-pro-16-2.jpg
dl photo-1605236453806-6ff36851218e products/phone-pro-16-3.jpg

dl photo-1567581935884-3349723552ca products/phone-16-cover.jpg
dl photo-1556656793-08538906a9f8   products/phone-16-1.jpg

dl photo-1561154464-82e9adf32764   products/tab-pro-13-cover.jpg
dl photo-1544244015-0df4b3ffc6b0   products/tab-pro-13-1.jpg
dl photo-1542751110-97427bbecf20   products/tab-pro-13-2.jpg

dl photo-1623126908029-58cb08a2b272 products/tab-air-cover.jpg

dl photo-1517336714731-489689fd1ca8 products/book-pro-15-cover.jpg
dl photo-1496181133206-80ce9b88a853 products/book-pro-15-1.jpg
dl photo-1611186871348-b1ce696e52c9 products/book-pro-15-2.jpg

dl photo-1541807084-5c52b6b3adef   products/book-air-13-cover.jpg

dl photo-1606220588913-b3aacb4d2f46 products/pods-pro-cover.jpg
dl photo-1572569511254-d8f925fe2cbb products/pods-pro-1.jpg

dl photo-1546435770-a3e426bf472b   products/watch-cover.jpg
dl photo-1579586337278-3befd40fd17a products/watch-1.jpg

echo "→ news/"
dl photo-1605236453806-6ff36851218e news/phone-pro-16-launch.jpg
dl photo-1542751110-97427bbecf20   news/tab-pro-tandem-oled.jpg
dl photo-1531973576160-7125cd663d86 news/ces-recap-2026.jpg
dl photo-1542601906990-b4d3fb778b09 news/sustainability-2026.jpg
dl photo-1515378791036-0648a3ef77b2 news/developer-conference-invite.jpg

echo
echo "✅ Done. 总文件数：$(find products news -type f | wc -l | tr -d ' ')"
echo "总大小：$(du -sh . | cut -f1)"
