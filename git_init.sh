#!/bin/bash

# 🚀 GitHub初始化和上传脚本
# Interactive Biomimetic Bone Scaffold Generator based on Voronoi Tessellation
# Author: Siqi (Qizaifadacai)
# Usage: bash git_init.sh

set -e  # 遇到错误立即退出

# 颜色定义
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${BLUE}╔════════════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║   GitHub 仓库初始化脚本                                    ║${NC}"
echo -e "${BLUE}║   Biomimetic Bone Scaffold Generator (Voronoi)             ║${NC}"
echo -e "${BLUE}╚════════════════════════════════════════════════════════════╝${NC}"
echo ""

# 预设信息
USERNAME="Qizaifadacai"
REPO_NAME="biomimetic-bone-scaffold-generator-voronoi"
GIT_NAME="Siqi"
GIT_EMAIL="fortyseven0629@gmail.com"

echo -e "${GREEN}✓ GitHub用户名: $USERNAME${NC}"
echo -e "${GREEN}✓ 仓库名称: $REPO_NAME${NC}"
echo -e "${GREEN}✓ 作者: $GIT_NAME${NC}"
echo -e "${GREEN}✓ 邮箱: $GIT_EMAIL${NC}"
echo ""

# 步骤1: 检查git是否安装
echo -e "${BLUE}[1/6] 检查Git安装...${NC}"
if ! command -v git &> /dev/null; then
    echo -e "${RED}✗ Git未安装，请先安装Git${NC}"
    exit 1
fi
echo -e "${GREEN}✓ Git已安装${NC}"
echo ""

# 步骤2: 初始化git仓库
echo -e "${BLUE}[2/6] 初始化Git仓库...${NC}"
if [ -d ".git" ]; then
    echo -e "${YELLOW}⚠ Git仓库已存在，跳过初始化${NC}"
else
    git init
    echo -e "${GREEN}✓ Git仓库初始化完成${NC}"
fi
echo ""

# 步骤3: 配置git用户信息
echo -e "${BLUE}[3/6] 配置Git用户信息...${NC}"
git config user.name "$GIT_NAME"
git config user.email "$GIT_EMAIL"
echo -e "${GREEN}✓ Git配置完成${NC}"
echo -e "  用户名: $(git config user.name)"
echo -e "  邮箱: $(git config user.email)"
echo ""

# 步骤4: 添加文件
echo -e "${BLUE}[4/6] 添加文件到Git...${NC}"
git add .
echo -e "${GREEN}✓ 文件已添加${NC}"

# 显示将要提交的文件
echo -e "${YELLOW}将要提交的文件:${NC}"
git status --short | head -20
echo ""

# 步骤5: 提交
echo -e "${BLUE}[5/6] 提交更改...${NC}"
git commit -m "Initial commit: Interactive Biomimetic Bone Scaffold Generator v2.0

🦴 Biomimetic Bone Scaffold Generator based on Voronoi Tessellation

Features:
- ✨ TextBox-based parameter input for precise numerical control
- 🎨 Colorful 3D Voronoi visualization with 30+ vibrant colors
- 📸 SEM-style scaffold rendering with realistic grayscale and dynamic lighting
- 💾 One-click export with timestamp naming (STL + PNG)
- 📊 Real-time gradient analysis with 6 interactive plots
- 🔬 Biomimetic gradient structure (cortical-transition-trabecular: 20:30:50)
- 🖼️ High-quality visualization outputs (300 DPI)
- 🖨️ STL export for 3D printing and fabrication

Author: Siqi (Qizaifadacai)
Field: Tissue Engineering / Stem Cell Research"
echo -e "${GREEN}✓ 提交完成${NC}"
echo ""

# 步骤6: 添加远程仓库并推送
echo -e "${BLUE}[6/6] 连接到GitHub...${NC}"
REPO_URL="https://github.com/$USERNAME/$REPO_NAME.git"

# 检查远程仓库是否已存在
if git remote | grep -q "origin"; then
    echo -e "${YELLOW}⚠ 远程仓库'origin'已存在${NC}"
    echo -e "${YELLOW}当前远程仓库: $(git remote get-url origin)${NC}"
    echo -e "${YELLOW}是否要更新远程仓库地址? (y/n)${NC}"
    read update_remote
    if [ "$update_remote" = "y" ]; then
        git remote set-url origin $REPO_URL
        echo -e "${GREEN}✓ 远程仓库地址已更新${NC}"
    fi
else
    git remote add origin $REPO_URL
    echo -e "${GREEN}✓ 远程仓库已添加${NC}"
fi

echo -e "${GREEN}✓ 远程仓库: $REPO_URL${NC}"
echo ""

# 设置主分支
echo -e "${BLUE}设置主分支为 main...${NC}"
git branch -M main
echo -e "${GREEN}✓ 主分支设置完成${NC}"
echo ""

# 推送提示
echo -e "${BLUE}════════════════════════════════════════════════════════════${NC}"
echo -e "${YELLOW}准备推送到GitHub！${NC}"
echo -e "${BLUE}════════════════════════════════════════════════════════════${NC}"
echo ""
echo -e "${YELLOW}在推送之前，请确保:${NC}"
echo -e "  1. 已在GitHub上创建仓库: $REPO_NAME"
echo -e "  2. 仓库可见性设置正确（Public/Private）"
echo -e "  3. 已设置GitHub认证（SSH密钥或Personal Access Token）"
echo ""
echo -e "${YELLOW}是否现在推送到GitHub? (y/n)${NC}"
read push_now

if [ "$push_now" = "y" ]; then
    echo -e "${BLUE}正在推送到GitHub...${NC}"
    if git push -u origin main; then
        echo -e "${GREEN}✓ 推送成功！${NC}"
        echo ""
        echo -e "${BLUE}════════════════════════════════════════════════════════════${NC}"
        echo -e "${GREEN}🎉 恭喜！项目已成功上传到GitHub！${NC}"
        echo -e "${BLUE}════════════════════════════════════════════════════════════${NC}"
        echo ""
        echo -e "${YELLOW}下一步:${NC}"
        echo -e "  1. 访问: https://github.com/$USERNAME/$REPO_NAME"
        echo -e "  2. 添加示例图片到 examples/ 目录"
        echo -e "  3. 添加Topics标签"
        echo -e "  4. 创建第一个Release (v2.0.0)"
        echo -e "  5. 分享你的项目！"
        echo ""
        echo -e "${GREEN}查看详细的后续步骤，请阅读 GITHUB_发布指南.md${NC}"
        echo ""
    else
        echo -e "${RED}✗ 推送失败${NC}"
        echo ""
        echo -e "${YELLOW}可能的原因:${NC}"
        echo -e "  1. GitHub仓库尚未创建"
        echo -e "  2. 认证失败（需要配置SSH或Token）"
        echo -e "  3. 网络连接问题"
        echo ""
        echo -e "${YELLOW}手动推送命令:${NC}"
        echo -e "  git push -u origin main"
        echo ""
    fi
else
    echo -e "${YELLOW}已跳过推送${NC}"
    echo ""
    echo -e "${YELLOW}手动推送命令:${NC}"
    echo -e "  git push -u origin main"
    echo ""
fi

echo -e "${BLUE}════════════════════════════════════════════════════════════${NC}"
echo -e "${GREEN}Git初始化完成！${NC}"
echo -e "${BLUE}════════════════════════════════════════════════════════════${NC}"
