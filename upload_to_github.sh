#!/bin/bash

# 🎯 一键上传到GitHub
# Biomimetic Bone Scaffold Generator - Voronoi
# Author: Siqi (Qizaifadacai)

clear

echo "╔════════════════════════════════════════════════════════════╗"
echo "║                                                            ║"
echo "║     🦴 GitHub 上传 - 一键完成                              ║"
echo "║                                                            ║"
echo "║     Biomimetic Bone Scaffold Generator (Voronoi)          ║"
echo "║                                                            ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""
echo "📋 准备上传的仓库信息："
echo "   • 用户名: Qizaifadacai"
echo "   • 仓库名: biomimetic-bone-scaffold-generator-voronoi"
echo "   • 作者: Siqi"
echo "   • 邮箱: fortyseven0629@gmail.com"
echo ""
echo "⚠️  在继续之前，请确认："
echo ""
echo "   1. ✅ 您已在 GitHub 创建了新仓库"
echo "      访问: https://github.com/new"
echo "      名称: biomimetic-bone-scaffold-generator-voronoi"
echo "      ⚠️  不要勾选任何自动生成文件的选项！"
echo ""
echo "   2. ✅ （推荐）您已生成示例图片"
echo "      运行: python3 新版本演示.py"
echo "      然后点击 'Generate Scaffold' 和 'Save Visuals'"
echo "      将图片复制到 examples/ 目录"
echo ""
echo "   3. ✅ 您已安装并配置了 Git"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

read -p "确认继续？(y/n): " confirm

if [ "$confirm" != "y" ] && [ "$confirm" != "Y" ]; then
    echo ""
    echo "❌ 已取消。请完成准备工作后再运行此脚本。"
    echo ""
    echo "📚 参考文档："
    echo "   • FINAL_CHECKLIST.md - 完整检查清单"
    echo "   • UPLOAD_GUIDE.md - 详细上传指南"
    echo "   • GITHUB_SETUP.md - GitHub配置说明"
    echo ""
    exit 0
fi

echo ""
echo "🚀 开始上传流程..."
echo ""

# 执行git_init.sh
bash git_init.sh

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "✨ 上传完成！"
echo ""
echo "📌 下一步："
echo ""
echo "1️⃣  访问您的仓库："
echo "   https://github.com/Qizaifadacai/biomimetic-bone-scaffold-generator-voronoi"
echo ""
echo "2️⃣  添加 Topics 标签："
echo "   点击 'Add topics' 并添加："
echo "   biomimetic, bone-scaffold, tissue-engineering, voronoi-tessellation,"
echo "   3d-printing, stem-cell, python, matplotlib, scientific-computing"
echo ""
echo "3️⃣  设置项目描述："
echo "   点击仓库设置，添加描述和网站链接"
echo ""
echo "4️⃣  （可选）添加示例图片："
echo "   如果还没有，运行程序生成图片并上传到 examples/ 目录"
echo ""
echo "5️⃣  创建第一个 Release："
echo "   Releases → Create a new release → Tag: v2.0.0"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "🎉 恭喜！您的项目已成功上传到 GitHub！"
echo ""
echo "⭐ 不要忘记给自己的项目点个 Star！"
echo ""
