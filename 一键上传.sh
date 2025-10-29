#!/bin/bash
# 一键上传到GitHub
# 作者：Qizaifadacai
# 仓库：biomimetic-bone-scaffold-generator-voronoi

echo "╔════════════════════════════════════════════════════════════╗"
echo "║        GitHub 一键上传脚本                                  ║"
echo "║        Biomimetic Bone Scaffold Generator                 ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""

# 颜色定义
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# GitHub信息
GITHUB_USER="Qizaifadacai"
REPO_NAME="biomimetic-bone-scaffold-generator-voronoi"
EMAIL="fortyseven0629@gmail.com"

echo -e "${BLUE}📋 项目信息：${NC}"
echo "   用户名: $GITHUB_USER"
echo "   仓库名: $REPO_NAME"
echo "   邮箱: $EMAIL"
echo ""

# 步骤1: 检查git是否安装
echo -e "${BLUE}[1/6] 检查Git安装...${NC}"
if ! command -v git &> /dev/null; then
    echo -e "${RED}❌ Git未安装，请先安装Git${NC}"
    exit 1
fi
echo -e "${GREEN}✓ Git已安装${NC}"
echo ""

# 步骤2: 初始化Git仓库
echo -e "${BLUE}[2/6] 初始化Git仓库...${NC}"
if [ ! -d ".git" ]; then
    git init
    echo -e "${GREEN}✓ Git仓库已初始化${NC}"
else
    echo -e "${YELLOW}⚠ Git仓库已存在${NC}"
fi
echo ""

# 步骤3: 配置Git用户信息
echo -e "${BLUE}[3/6] 配置Git用户信息...${NC}"
git config user.name "$GITHUB_USER"
git config user.email "$EMAIL"
echo -e "${GREEN}✓ 用户信息已配置${NC}"
echo ""

# 步骤4: 添加所有文件
echo -e "${BLUE}[4/6] 添加文件到Git...${NC}"
git add .
echo -e "${GREEN}✓ 文件已添加${NC}"
echo ""

# 步骤5: 提交更改
echo -e "${BLUE}[5/6] 提交更改...${NC}"
git commit -m "🎉 Initial commit: Interactive Biomimetic Bone Scaffold Generator

Features:
- 🎨 Colorful 3D Voronoi visualization with 30+ colors
- 📸 SEM-style realistic scaffold rendering (4 viewing angles)
- ✨ TextBox-based parameter input (no sliders)
- 💾 One-click export for STL files and high-resolution visualizations
- 🧬 Gradient density support (cortical, transition, trabecular)
- 🔬 Tissue engineering and stem cell research applications

Technologies:
- Python 3.7+
- NumPy, SciPy, Matplotlib
- 3D Voronoi tessellation
- Interactive GUI interface

Author: Qizaifadacai
License: MIT
"
echo -e "${GREEN}✓ 更改已提交${NC}"
echo ""

# 步骤6: 显示下一步操作
echo -e "${BLUE}[6/6] 准备推送到GitHub...${NC}"
echo ""
echo -e "${YELLOW}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${YELLOW}📌 重要提示：请在GitHub上手动创建仓库${NC}"
echo -e "${YELLOW}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""
echo -e "${GREEN}步骤 A: 在GitHub上创建新仓库${NC}"
echo "   1. 访问: https://github.com/new"
echo "   2. 仓库名称: $REPO_NAME"
echo "   3. 描述: Interactive Biomimetic Bone Scaffold Generator with Voronoi Tessellation"
echo "   4. 选择: Public (公开仓库)"
echo "   5. ❌ 不要勾选任何初始化选项 (README, .gitignore, license)"
echo "   6. 点击 'Create repository'"
echo ""
echo -e "${GREEN}步骤 B: 复制以下命令并执行${NC}"
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""
echo "git remote add origin https://github.com/$GITHUB_USER/$REPO_NAME.git"
echo "git branch -M main"
echo "git push -u origin main"
echo ""
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""
echo -e "${YELLOW}或者，如果您已经创建了仓库，现在就运行：${NC}"
echo ""
read -p "是否现在推送到GitHub? (y/n): " -n 1 -r
echo ""
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo -e "${BLUE}正在添加远程仓库...${NC}"
    
    # 检查远程仓库是否已存在
    if git remote | grep -q "^origin$"; then
        echo -e "${YELLOW}⚠ 远程仓库已存在，正在更新...${NC}"
        git remote set-url origin https://github.com/$GITHUB_USER/$REPO_NAME.git
    else
        git remote add origin https://github.com/$GITHUB_USER/$REPO_NAME.git
    fi
    
    echo -e "${BLUE}正在推送到GitHub...${NC}"
    git branch -M main
    git push -u origin main
    
    if [ $? -eq 0 ]; then
        echo ""
        echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
        echo -e "${GREEN}✅ 成功上传到GitHub！${NC}"
        echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
        echo ""
        echo -e "${BLUE}🎉 您的仓库地址：${NC}"
        echo "   https://github.com/$GITHUB_USER/$REPO_NAME"
        echo ""
        echo -e "${BLUE}📝 下一步操作：${NC}"
        echo "   1. 访问仓库页面"
        echo "   2. 添加Topics: python, voronoi, tissue-engineering, 3d-visualization, scaffold"
        echo "   3. 在About中添加网站和描述"
        echo "   4. 上传示例图片到 examples/ 目录"
        echo "   5. Star ⭐ 您自己的项目！"
        echo ""
    else
        echo ""
        echo -e "${RED}❌ 推送失败${NC}"
        echo -e "${YELLOW}可能的原因：${NC}"
        echo "   1. GitHub仓库尚未创建"
        echo "   2. 网络连接问题"
        echo "   3. 需要Git凭据认证"
        echo ""
        echo -e "${YELLOW}请先在GitHub上创建仓库，然后手动执行上述命令${NC}"
    fi
else
    echo ""
    echo -e "${YELLOW}稍后可以手动运行以下命令：${NC}"
    echo "   git remote add origin https://github.com/$GITHUB_USER/$REPO_NAME.git"
    echo "   git branch -M main"
    echo "   git push -u origin main"
fi

echo ""
echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${GREEN}🎊 本地Git仓库已准备就绪！${NC}"
echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""
