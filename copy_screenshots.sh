#!/bin/bash

# 📸 自动复制最新生成的截图到examples目录
# Biomimetic Bone Scaffold Generator

echo "╔════════════════════════════════════════════════════════════╗"
echo "║   📸 截图自动复制工具                                      ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""

# 创建examples目录（如果不存在）
mkdir -p examples

# 检查Voronoi scaffold目录
if [ ! -d "Voronoi scaffold" ]; then
    echo "❌ 错误: 'Voronoi scaffold' 目录不存在"
    echo ""
    echo "请先运行程序生成图片："
    echo "  python3 新版本演示.py"
    echo ""
    exit 1
fi

echo "📂 查找最新生成的图片..."
echo ""

# 查找最新的colorful_voronoi_3d文件
COLORFUL=$(ls -t "Voronoi scaffold"/colorful_voronoi_3d_*.png 2>/dev/null | head -1)
REALISTIC=$(ls -t "Voronoi scaffold"/realistic_scaffold_*.png 2>/dev/null | head -1)
GRADIENT=$(ls -t "Voronoi scaffold"/gradient_analysis_*.png 2>/dev/null | head -1)

# 计数成功复制的文件
SUCCESS=0
TOTAL=0

# 复制colorful voronoi
if [ -n "$COLORFUL" ]; then
    echo "✅ 找到: $COLORFUL"
    cp "$COLORFUL" "examples/colorful_voronoi_3d.png"
    echo "   → 已复制到: examples/colorful_voronoi_3d.png"
    SUCCESS=$((SUCCESS + 1))
else
    echo "⚠️  未找到: colorful_voronoi_3d_*.png"
fi
TOTAL=$((TOTAL + 1))

# 复制realistic scaffold
if [ -n "$REALISTIC" ]; then
    echo "✅ 找到: $REALISTIC"
    cp "$REALISTIC" "examples/realistic_scaffold.png"
    echo "   → 已复制到: examples/realistic_scaffold.png"
    SUCCESS=$((SUCCESS + 1))
else
    echo "⚠️  未找到: realistic_scaffold_*.png"
fi
TOTAL=$((TOTAL + 1))

# 复制gradient analysis
if [ -n "$GRADIENT" ]; then
    echo "✅ 找到: $GRADIENT"
    cp "$GRADIENT" "examples/gradient_analysis.png"
    echo "   → 已复制到: examples/gradient_analysis.png"
    SUCCESS=$((SUCCESS + 1))
else
    echo "⚠️  未找到: gradient_analysis_*.png"
fi
TOTAL=$((TOTAL + 1))

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# 检查interactive_interface.png
if [ -f "examples/interactive_interface.png" ]; then
    echo "✅ 界面截图已存在: examples/interactive_interface.png"
else
    echo "⚠️  缺少界面截图: examples/interactive_interface.png"
    echo ""
    echo "💡 提示: 请手动保存界面截图为此文件名"
fi

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "📊 总结: 成功复制 $SUCCESS/$TOTAL 个程序生成的图片"
echo ""

# 显示examples目录内容
echo "📁 examples/ 目录内容:"
echo ""
ls -lh examples/*.png 2>/dev/null || echo "   (暂无图片)"

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

if [ $SUCCESS -eq 3 ] && [ -f "examples/interactive_interface.png" ]; then
    echo "🎉 太棒了！所有4张截图都已准备就绪！"
    echo ""
    echo "📤 下一步: 提交到Git"
    echo ""
    echo "   git add examples/*.png"
    echo "   git commit -m \"Add example visualizations\""
    echo "   git push"
    echo ""
elif [ $SUCCESS -eq 0 ]; then
    echo "❌ 未找到任何生成的图片"
    echo ""
    echo "请先运行程序："
    echo "  1. python3 新版本演示.py"
    echo "  2. 点击 'Generate Scaffold'"
    echo "  3. 点击 'Save Visuals'"
    echo "  4. 再次运行此脚本"
    echo ""
else
    echo "⚠️  部分图片已准备就绪"
    echo ""
    echo "还需要的文件:"
    [ ! -f "examples/colorful_voronoi_3d.png" ] && echo "  • colorful_voronoi_3d.png"
    [ ! -f "examples/realistic_scaffold.png" ] && echo "  • realistic_scaffold.png"
    [ ! -f "examples/gradient_analysis.png" ] && echo "  • gradient_analysis.png"
    [ ! -f "examples/interactive_interface.png" ] && echo "  • interactive_interface.png (手动截图)"
    echo ""
fi

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
