#!/bin/bash
# GitHub 全自动部署脚本 — 只需先 gh auth login 一次
set -e

REPO="ghstar-2026"
DIR="$HOME/idiom-roguelike"

echo "🚀 GitHub 涨星榜 一键部署"
echo "=========================="

# 1. 检查 gh 认证
if ! gh auth status &>/dev/null; then
    echo "❌ 请先运行: gh auth login"
    echo "   然后选 GitHub.com → SSH → 浏览器登录"
    exit 1
fi
echo "✅ gh 已认证"

# 2. 创建仓库
if ! gh repo view "Vir-Limerence/$REPO" &>/dev/null; then
    echo "📦 创建仓库 $REPO..."
    gh repo create "$REPO" --public --description "GitHub 涨星排行榜" --source "$DIR" --push
else
    echo "✅ 仓库已存在"
fi

# 3. 推代码
cd "$DIR"
git add -A
git commit -m "更新涨星榜 $(date +%Y-%m-%d)" 2>/dev/null || true
git push origin main

# 4. 开启 Pages
echo "🌐 开启 GitHub Pages..."
gh api repos/Vir-Limerence/$REPO/pages -X POST -f "source[branch]=main" -f "source[path]=/" 2>/dev/null || true

echo ""
echo "🎉 完成！访问: https://vir-limerence.github.io/$REPO/star-rank.html"
