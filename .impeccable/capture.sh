#!/bin/bash
# GTM page capture — desktop/mobile × light/dark via headless Chrome
set -e
CHROME="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
URL="http://127.0.0.1:4793/GTM/"
OUT="/Users/allengaller/Documents/GitHub/allengaller/allengaller.github.io/.impeccable/review"
mkdir -p "$OUT"

shoot () {
  local name="$1" w="$2" h="$3"; shift 3
  "$CHROME" --headless=new --disable-gpu --no-sandbox --hide-scrollbars \
    --force-color-profile=srgb --window-size="${w},${h}" \
    --virtual-time-budget=6000 \
    "$@" \
    --screenshot="${OUT}/${name}.png" \
    "$URL" 2>/dev/null
  echo "captured ${name}.png"
}

LIGHT="--blink-settings=preferredColorScheme=light"
DARK="--blink-settings=preferredColorScheme=dark"

shoot desktop-light 1440 7200 $LIGHT
shoot desktop-dark  1440 7200 $DARK
shoot mobile-light  390  9600 $LIGHT
shoot mobile-dark   390  9600 $DARK

echo "DONE"
