# 🦴 基于Voronoi镶嵌的交互式仿生骨支架生成器

[![Python](https://img.shields.io/badge/Python-3.7+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Matplotlib](https://img.shields.io/badge/Matplotlib-3.3+-orange.svg)](https://matplotlib.org/)
[![Status](https://img.shields.io/badge/Status-Active-success.svg)]()
[![GitHub Stars](https://img.shields.io/github/stars/Qizaifadacai/biomimetic-bone-scaffold-generator-voronoi?style=social)](https://github.com/Qizaifadacai/biomimetic-bone-scaffold-generator-voronoi)

> **基于3D Voronoi镶嵌的交互式仿生骨支架生成工具，专为组织工程和再生医学研究设计**

**👨‍🔬 作者:** Siqi (Qizaifadacai) | **📧 联系:** fortyseven0629@gmail.com | **🏫 研究方向:** 组织工程 / 干细胞研究

---

## 🌟 核心特性

- 🎮 **交互式参数输入** - 通过文本框直接输入精确数值（无滑块！）
- 🎨 **彩色3D Voronoi可视化** - 30+种鲜艳颜色展示每个Voronoi单元
- 📸 **SEM风格支架渲染** - 仿真扫描电镜的灰度渲染效果
- 🔬 **仿生梯度结构** - 皮质骨→过渡层→松质骨（20:30:50比例）
- 💾 **一键导出** - STL文件（3D打印）+ 高分辨率可视化图（300 DPI）
- 📊 **实时分析** - 6个交互式图表实时显示梯度分析

---

## 🎬 效果展示

### 彩色3D Voronoi结构
<img src="examples/colorful_voronoi_3d.png" alt="彩色Voronoi" width="600"/>

*30+种颜色，清晰边界，种子点标记 - 专业的多面体渲染*

### SEM风格支架可视化
<img src="examples/realistic_scaffold.png" alt="SEM支架" width="600"/>

*4视角灰度渲染，动态光照 - 扫描电镜风格*

### 梯度分析图
<img src="examples/gradient_analysis.png" alt="梯度分析" width="600"/>

*实时梯度分析，6个交互式图表*

---

## 🚀 快速开始

### 安装

#### 方法1：克隆仓库
```bash
# 克隆仓库
git clone https://github.com/Qizaifadacai/biomimetic-bone-scaffold-generator-voronoi.git
cd biomimetic-bone-scaffold-generator-voronoi

# 安装依赖
pip install -r requirements.txt
```

#### 方法2：直接下载
1. 点击绿色 "Code" 按钮
2. 选择 "Download ZIP"
3. 解压到本地
4. 安装依赖：`pip install -r requirements.txt`

### 运行

#### 使用快速启动脚本（推荐）

**macOS/Linux:**
```bash
bash quick_start.sh
```

**Windows:**
```cmd
quick_start.bat
```

#### 手动运行
```bash
python3 demo.py
```

或使用快速启动脚本：
```bash
bash run.sh
```

---

## 📖 使用指南

### 1️⃣ 启动程序
运行后会看到欢迎界面，按Enter启动交互式界面

### 2️⃣ 设置参数
在文本框中输入数值：
- **皮质骨密度** (Cortical Density): 5,000 - 40,000 seeds/mm³
- **过渡层密度** (Transition Density): 3,000 - 25,000 seeds/mm³
- **松质骨密度** (Trabecular Density): 1,000 - 15,000 seeds/mm³
- **目标孔隙率** (Target Porosity): 40 - 85 %

**推荐参数（标准仿生骨）:**
- Cortical: 25,000
- Transition: 12,000
- Trabecular: 6,000
- Porosity: 68%

### 3️⃣ 生成支架
点击 **"Generate Scaffold"** 按钮，系统会：
- 生成3D Voronoi结构
- 计算梯度分布
- 显示6个实时图表
- 渲染彩色和SEM风格可视化

### 4️⃣ 保存结果
点击 **"Save Visuals"** 按钮，自动保存：
- `colorful_voronoi_3d_[时间戳].png` - 彩色3D Voronoi图
- `realistic_scaffold_[时间戳].png` - SEM风格4视角图
- `gradient_analysis_[时间戳].png` - 梯度分析图
- `scaffold_[时间戳].stl` - STL文件（3D打印）
- `scaffold_config_[时间戳].json` - 配置参数

所有文件保存在 `Voronoi scaffold/` 目录

---

## 🔬 科学原理

### Voronoi镶嵌
- 基于随机种子点生成Voronoi单元
- 模拟骨小梁的自然分布
- 创建互连的多孔网络

### 梯度结构
仿生骨的三层结构：
1. **皮质骨层** (20%) - 高密度，低孔隙率
2. **过渡层** (30%) - 中等密度
3. **松质骨层** (50%) - 低密度，高孔隙率

### 孔隙率控制
通过调整种子密度和Voronoi单元大小控制孔隙率，符合骨组织工程要求

---

## 📁 项目结构

```
biomimetic-bone-scaffold-generator-voronoi/
├── scaffold_generator.py              # Main program (core algorithm)
├── demo.py                            # Demo launcher
├── visualization.py                   # Advanced visualization tools
├── run.sh                             # Quick start script
├── git_init.sh                        # GitHub initialization
├── copy_screenshots.sh                # Screenshot copy tool
├── voronoi_scaffold_generator.py      # 基础生成器
├── advanced_visualization.py          # 高级可视化工具
├── test_all_features.py              # 功能测试
├── 启动器.py                          # 菜单启动器
├── interactive_demo.py                # 旧版演示
├── README.md                          # 英文文档
├── README_CN.md                       # 中文文档（本文件）
├── LICENSE                            # MIT许可证
├── requirements.txt                   # Python依赖
├── setup.py                           # 安装脚本
├── .gitignore                         # Git忽略规则
├── quick_start.sh                     # 快速启动（Unix）
├── quick_start.bat                    # 快速启动（Windows）
├── git_init.sh                        # GitHub初始化脚本
├── UPLOAD_GUIDE.md                    # 上传指南
├── GITHUB_SETUP.md                    # GitHub配置
├── PROJECT_OVERVIEW.md                # 项目概览
├── CHANGELOG.md                       # 更新日志
├── CONTRIBUTING.md                    # 贡献指南
├── docs/                              # 详细文档
│   ├── 使用指南_新版本.md
│   ├── 快速参考.md
│   ├── 视觉效果对比.md
│   └── 更新摘要.md
├── examples/                          # 示例图片
│   ├── colorful_voronoi_3d.png
│   ├── realistic_scaffold.png
│   └── gradient_analysis.png
├── .github/
│   └── workflows/
│       └── python-tests.yml          # 自动化测试
└── Voronoi scaffold/                  # 输出目录
    ├── *.stl                          # STL文件
    ├── *.png                          # 图片
    └── *.json                         # 配置文件
```

---

## 🛠️ 技术栈

- **Python 3.7+** - 核心编程语言
- **NumPy** - 数值计算
- **SciPy** - 科学计算（Voronoi算法）
- **Matplotlib** - 3D可视化和交互式界面
- **numpy-stl** - STL文件导出

---

## 💡 应用场景

### 研究应用
- 🔬 骨组织工程支架设计
- 🧬 干细胞培养基质
- 💊 药物释放系统
- 🦴 骨缺损修复材料

### 教育应用
- 📚 生物材料课程教学
- 🎓 组织工程实验演示
- 👨‍🎓 本科/研究生项目

### 工业应用
- 🖨️ 3D打印支架制造
- 🏭 定制化植入物设计
- 🔧 快速原型制作

---

## 🎯 系统要求

### 最低要求
- **操作系统**: Windows 7+, macOS 10.12+, Linux
- **Python**: 3.7 或更高版本
- **内存**: 4 GB RAM
- **显示**: 支持GUI的环境

### 推荐配置
- **操作系统**: Windows 10/11, macOS 12+, Ubuntu 20.04+
- **Python**: 3.9+
- **内存**: 8 GB RAM
- **显示**: 1920×1080 或更高分辨率

---

## 📊 性能参数

- **生成时间**: 通常 < 10秒（标准参数）
- **STL文件大小**: 1-50 MB（取决于复杂度）
- **图片分辨率**: 300 DPI（出版级质量）
- **最大种子数**: ~100,000（取决于内存）

---

## 🤝 贡献

欢迎贡献！请查看 [CONTRIBUTING.md](CONTRIBUTING.md) 了解详情。

### 如何贡献
1. Fork 本仓库
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启 Pull Request

---

## 📝 更新日志

查看 [CHANGELOG.md](CHANGELOG.md) 了解详细更新历史。

### 最新版本 - v2.0.0 (2025-10-29)
- ✨ 文本框输入替代滑块
- 🎨 彩色3D Voronoi可视化
- 📸 SEM风格支架渲染
- 💾 一键导出功能
- 📊 实时梯度分析

---

## ❓ 常见问题

### Q1: 如何调整孔隙率？
**A:** 通过调整种子密度。密度越高，孔隙率越低。

### Q2: STL文件可以直接3D打印吗？
**A:** 是的，导出的STL文件可以直接用于3D打印，但建议先在切片软件中检查。

### Q3: 如何生成更大的支架？
**A:** 修改代码中的 `x_size`, `y_size`, `z_size` 参数（单位：米）。

### Q4: 支持哪些文件格式？
**A:** 目前支持STL（3D打印）、PNG（图片）、JSON（配置）。

### Q5: 如何引用此工具？
**A:** 见下方"引用"部分的BibTeX格式。

---

## 📝 引用

如果在研究中使用此工具，请引用：

```bibtex
@software{biomimetic_scaffold_generator_voronoi,
  author = {Siqi (Qizaifadacai)},
  title = {Interactive Biomimetic Bone Scaffold Generator based on Voronoi Tessellation},
  year = {2025},
  url = {https://github.com/Qizaifadacai/biomimetic-bone-scaffold-generator-voronoi}
}
```

---

## 📄 许可证

本项目采用 MIT 许可证 - 详见 [LICENSE](LICENSE) 文件

这意味着您可以自由地：
- ✅ 商业使用
- ✅ 修改
- ✅ 分发
- ✅ 私人使用

但需要：
- 📌 包含版权声明
- 📌 包含许可证副本

---

## 🌐 相关链接

- 📚 [详细文档](docs/使用指南_新版本.md)
- 🎯 [快速参考](docs/快速参考.md)
- 📊 [视觉效果对比](docs/视觉效果对比.md)
- 🐛 [问题追踪](https://github.com/Qizaifadacai/biomimetic-bone-scaffold-generator-voronoi/issues)
- 💬 [讨论区](https://github.com/Qizaifadacai/biomimetic-bone-scaffold-generator-voronoi/discussions)

---

## 📧 联系方式

- **作者:** Siqi (Qizaifadacai)
- **邮箱:** fortyseven0629@gmail.com
- **GitHub:** [@Qizaifadacai](https://github.com/Qizaifadacai)
- **研究方向:** 组织工程 / 干细胞研究

---

## ⭐ Star历史

如果觉得这个项目有帮助，请考虑给它一个star！⭐

---

## 🙏 致谢

感谢所有为骨组织工程和开源科学做出贡献的研究者们。

---

<p align="center">
  用 ❤️ 制作，为骨组织工程研究服务
</p>

<p align="center">
  <strong>🦴 通过计算方法推进仿生支架设计 🔬</strong>
</p>

---

<p align="center">
  <a href="README.md">English</a> | <strong>中文</strong>
</p>
