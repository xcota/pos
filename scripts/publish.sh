#!/bin/bash
# publish.sh — push Camomile to both public remotes.
#   GitHub (remote "github", branch main): English README in front.
#   Gitee  (remote "gitee",  branch master): same tree, Chinese README in front
#           (built as a throwaway local branch "gitee" and force-pushed, because it is
#            a derived mirror branch, not a place where anyone commits).
# Usage: scripts/publish.sh [--tunnel]   # --tunnel routes the Gitee push via socks5 127.0.0.1:18080
set -e
cd "$(dirname "$0")/.."
if ! git diff --quiet || ! git diff --cached --quiet; then echo "uncommitted changes — commit first"; exit 1; fi
[ "$(git rev-parse --abbrev-ref HEAD)" = "main" ] || { echo "run from branch main"; exit 1; }
PROXY=""; [ "$1" = "--tunnel" ] && PROXY="-c http.proxy=socks5h://127.0.0.1:18080"

# Visible build stamp on the site (entry page + three presentations): date · short hash of the
# content commit. Anyone can see at a glance whether the site has rebuilt — no trust required.
STAMP="$(date +%F) · $(git rev-parse --short HEAD)"
for f in docs/index.html docs/en/presentation.html docs/zh/presentation.html docs/ru/presentation.html; do
  sed -i '' "s|<span class=\"build\">[^<]*</span>|<span class=\"build\">$STAMP</span>|" "$f"
done
if ! git diff --quiet; then
  git add docs/index.html docs/en/presentation.html docs/zh/presentation.html docs/ru/presentation.html
  git commit -q -m "site: build stamp $STAMP" -m "Co-Authored-By: Claude Fable 5.1 <noreply@anthropic.com>"
fi
echo "== site stamp: $STAMP"
# Cache-busting: links from the entry page carry the build hash, so a browser never reuses an old copy of a presentation.
sed -i '' "s|presentation.html?v=[^\"]*\"|presentation.html?v=$(git rev-parse --short HEAD)\"|g" docs/index.html
if ! git diff --quiet; then git add docs/index.html; git commit -q -m "site: link versions $(git rev-parse --short HEAD)" -m "Co-Authored-By: Claude Fable 5.1 <noreply@anthropic.com>"; fi

echo "== GitHub: main"
timeout 120 git push github main:main

echo "== Gitee: master (Chinese README in front)"
git branch -f gitee main
git checkout -q gitee
cp README.md README.en.md
cp README.zh.md README.md
sed -i '' 's/\[English\](README.md)/[English](README.en.md)/' README.md
git add README.md README.en.md
git commit -q -m "gitee: Chinese README in front" -m "Co-Authored-By: Claude Fable 5.1 <noreply@anthropic.com>"
timeout 120 git $PROXY push -f gitee gitee:master
git checkout -q main
echo "== done: github/main=$(git rev-parse --short main) gitee/master=$(git rev-parse --short gitee)"
