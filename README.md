# 🦴 Interactive Biomimetic Bone Scaffold Generator based on Voronoi Tessellation

[![Python](https://img.shields.io/badge/Python-3.7+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Matplotlib](https://img.shields.io/badge/Matplotlib-3.3+-orange.svg)](https://matplotlib.org/)
[![Status](https://img.shields.io/badge/Status-Active-success.svg)]()
[![GitHub Stars](https://img.shields.io/github/stars/Qizaifadacai/biomimetic-bone-scaffold-generator-voronoi?style=social)](https://github.com/Qizaifadacai/biomimetic-bone-scaffold-generator-voronoi)

> **基于3D Voronoi镶嵌的交互式仿生骨支架生成工具 | An interactive tool for generating biomimetic bone scaffolds with gradient porous structures using 3D Voronoi tessellation**

**👨‍🔬 Author:** Siqi (Qizaifadacai) | **📧 Contact:** fortyseven0629@gmail.com | **🏫 Field:** Tissue Engineering / Stem Cell Research

[English](#english) | [中文](#chinese)

---

<a name="english"></a>
## 📖 English Documentation

### 🌟 Features

- 🎮 **Interactive Parameter Input** - Direct numerical input via textboxes (no sliders!)
- 🎨 **Colorful 3D Voronoi Visualization** - 30+ vibrant colors for each Voronoi cell
- 📸 **SEM-Style Scaffold Rendering** - Realistic grayscale rendering simulating scanning electron microscopy
- 🔬 **Biomimetic Gradient Structure** - Cortical → Transition → Trabecular layers (20:30:50 ratio)
- 💾 **One-Click Export** - STL files for 3D printing + high-resolution visualizations (300 DPI)
- 📊 **Real-Time Analysis** - Live gradient analysis with 6 interactive plots

### 🎬 Demo

#### Interactive Interface
<img src="examples/interactive_interface.png" alt="Interactive Interface" width="800"/>

*Real-time interactive interface - 6 live plots with direct numerical input (textboxes)*

#### Colorful 3D Voronoi Structure
<img src="examples/colorful_voronoi_3d.png" alt="Colorful Voronoi" width="600"/>

*30+ colors, clear boundaries, seed markers - professional multi-faceted rendering*

#### SEM-Style Scaffold Visualization
<img src="examples/realistic_scaffold.png" alt="SEM Scaffold" width="600"/>

*4-view grayscale rendering with dynamic lighting - scanning electron microscope style*

#### Gradient Analysis
<img src="examples/gradient_analysis.png" alt="Gradient Analysis" width="600"/>

*Complete gradient analysis with density distribution, pore size, and gradient curves*

### 🚀 Quick Start

#### Installation

```bash
# Clone the repository
git clone https://github.com/Qizaifadacai/biomimetic-bone-scaffold-generator-voronoi.git
cd biomimetic-bone-scaffold-generator-voronoi

# Install dependencies
pip install -r requirements.txt
```

#### Run Interactive Interface

```bash
python3 demo.py
```

Or use the quick start script:

```bash
bash run.sh
```

```bash
python 支持梯度的Voronoi支架生成器.py
# Then select option: 1
```

**Interactive Interface Preview:**

<img src="examples/interactive_interface.png" alt="Interactive Interface" width="800"/>

*Real-time interactive interface with 6 live plots and direct numerical input*

---

### 🎮 How to Use

#### Step 1: Input Parameters
```
Enter values directly in the textboxes:
  Cortical Density (seeds/mm³):   [25000] ← Type & press Enter
  Transition Density (seeds/mm³): [12000] ← Type & press Enter
  Trabecular Density (seeds/mm³): [6000]  ← Type & press Enter
  Target Porosity (%):            [68]    ← Type & press Enter
```

#### Step 2: Generate
```
Click the "Generate Scaffold" button
→ 6 real-time plots will update automatically
```

#### Step 3: Save
```
• "Save STL" → Export 3D printable mesh + config JSON
• "Save Visuals" → Generate 3 high-quality images:
  1. colorful_voronoi_3d_*.png (colorful 3D Voronoi)
  2. realistic_scaffold_*.png (4-view SEM-style)
  3. gradient_analysis_*.png (complete gradient analysis)
```

### 📊 Parameter Ranges

| Parameter | Range | Recommended | Description |
|-----------|-------|-------------|-------------|
| Cortical Density | 5,000 - 40,000 | 25,000 | Outer dense layer |
| Transition Density | 3,000 - 25,000 | 12,000 | Middle transition layer |
| Trabecular Density | 1,000 - 15,000 | 6,000 | Inner porous layer |
| Target Porosity | 40 - 85 % | 68 % | Overall porosity |

### 💡 Recommended Parameter Sets

#### Standard Biomimetic Bone (Recommended)
```python
Cortical: 25000 seeds/mm³
Transition: 12000 seeds/mm³
Trabecular: 6000 seeds/mm³
Porosity: 68%
# Gradient ratio: ~3.0 (biomimetically optimal)
```

#### High-Strength Scaffold
```python
Cortical: 35000 seeds/mm³
Transition: 20000 seeds/mm³
Trabecular: 10000 seeds/mm³
Porosity: 55%
# For load-bearing applications
```

#### High-Porosity Scaffold
```python
Cortical: 15000 seeds/mm³
Transition: 8000 seeds/mm³
Trabecular: 3000 seeds/mm³
Porosity: 75%
# For nutrient diffusion
```

### 📁 Project Structure

```
biomimetic-scaffold-generator/
├── 支持梯度的Voronoi支架生成器.py  # Main program
├── 新版本演示.py                    # Quick demo launcher
├── voronoi_scaffold_generator.py   # Base generator (required)
├── requirements.txt                # Python dependencies
├── README.md                       # This file
├── LICENSE                         # MIT License
├── docs/                           # Documentation
│   ├── 使用指南_新版本.md          # Detailed guide (Chinese)
│   ├── 快速参考.md                # Quick reference (Chinese)
│   └── 视觉效果对比.md            # Visual comparison
├── examples/                      # Example outputs
│   ├── colorful_voronoi_3d.png
│   ├── realistic_scaffold.png
│   └── gradient_analysis.png
└── Voronoi scaffold/              # Output directory (auto-created)
    ├── *.stl                      # 3D printable meshes
    ├── *.json                     # Configuration files
    └── *.png                      # Visualization images
```

### 🔬 Technical Details

#### Biomimetic Structure
```
Z-direction gradient (bottom to top):
│
├─ 100% ┐
│       │ Trabecular Layer (50%)
│       │ • Low density: 4K-10K seeds/mm³
├─ 50%  ┤ • Large pores: 60-150 μm
│       │ • High porosity
│       │
│       │ Transition Layer (30%)
├─ 20%  ┤ • Medium density: 10K-18K seeds/mm³
│       │ • Medium pores: 30-60 μm
│       │
│       │ Cortical Layer (20%)
│       │ • High density: 20K-35K seeds/mm³
├─ 0%   ┘ • Small pores: 10-30 μm
│         • High strength
```

#### Color Schemes

**Colorful Voronoi Visualization:**
- 30+ vibrant colors (auto-cycled)
- 90% opacity
- Dark boundaries (2px, #2C3E50)
- Black seed markers (white outline)
- Light gray background (#F0F0F0)

**SEM-Style Scaffold:**
- Grayscale rendering (0.3-0.9 intensity)
- Normal-based dynamic lighting
- Black background (#1A1A1A)
- White axes and text
- 4 viewing angles (2×2 layout)

### 🎨 Visualization Outputs

When you click **"Save Visuals"**, three images are generated:

1. **Colorful 3D Voronoi** (`colorful_voronoi_3d_*.png`)
   - Multi-colored polyhedral cells
   - Clear boundaries and seed markers
   - Professional 3D rendering

2. **SEM-Style Scaffold** (`realistic_scaffold_*.png`)
   - 4 viewing angles
   - Grayscale with lighting effects
   - Scanning electron microscope aesthetics

3. **Gradient Analysis** (`gradient_analysis_*.png`)
   - 8 subplots with complete statistics
   - Seed distribution, pore analysis
   - Gradient curves and layer information

### 🛠️ Dependencies

```
numpy >= 1.19.0
scipy >= 1.5.0
matplotlib >= 3.3.0
numpy-stl >= 2.16.0
```

### 📝 Citation

If you use this tool in your research, please cite:

```bibtex
@software{biomimetic_scaffold_generator,
  author = {Kiki},
  title = {Interactive Biomimetic Scaffold Generator},
  year = {2025},
  url = {https://github.com/yourusername/biomimetic-scaffold-generator}
}
```

### 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

### 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

### 🙏 Acknowledgments

- Based on Voronoi tessellation algorithms
- Inspired by natural bone structure
- Built with Python scientific computing stack

---

<a name="chinese"></a>
## 📖 中文文档

### 🌟 功能特点

- 🎮 **输入框交互** - 直接输入精确数值，无需拖动滑块
- 🎨 **彩色3D Voronoi可视化** - 30+种鲜艳颜色的多面体单元
- 📸 **SEM风格支架渲染** - 模拟扫描电镜的灰度真实渲染
- 🔬 **仿生梯度结构** - 皮质骨→过渡层→松质骨 (20:30:50比例)
- 💾 **一键导出** - 3D打印STL文件 + 高清可视化图 (300 DPI)
- 📊 **实时分析** - 6个交互图表实时更新

### 🚀 快速开始

#### 安装

```bash
# 克隆仓库
git clone https://github.com/yourusername/biomimetic-scaffold-generator.git
cd biomimetic-scaffold-generator

# 安装依赖
pip install -r requirements.txt
```

#### 运行交互式界面

```bash
python 新版本演示.py
```

### 🎮 使用方法

#### 第1步：输入参数
```
在输入框中直接输入数值：
  皮质骨密度 (seeds/mm³):   [25000] ← 输入后按Enter
  过渡层密度 (seeds/mm³):   [12000] ← 输入后按Enter
  松质骨密度 (seeds/mm³):   [6000]  ← 输入后按Enter
  目标孔隙率 (%):           [68]    ← 输入后按Enter
```

#### 第2步：生成支架
```
点击 "Generate Scaffold" 按钮
→ 6个图表自动更新
```

#### 第3步：保存文件
```
• "Save STL" → 导出3D打印网格 + 配置JSON
• "Save Visuals" → 生成3张高清图片：
  1. colorful_voronoi_3d_*.png (彩色3D Voronoi)
  2. realistic_scaffold_*.png (4视角SEM风格)
  3. gradient_analysis_*.png (完整梯度分析)
```

### 📊 参数范围

| 参数 | 范围 | 推荐值 | 说明 |
|------|------|--------|------|
| 皮质骨密度 | 5,000 - 40,000 | 25,000 | 外层致密区 |
| 过渡层密度 | 3,000 - 25,000 | 12,000 | 中间过渡区 |
| 松质骨密度 | 1,000 - 15,000 | 6,000 | 内层疏松区 |
| 目标孔隙率 | 40 - 85 % | 68 % | 整体孔隙率 |

### 💡 推荐参数组合

#### 标准仿生骨（推荐）
```python
皮质骨: 25000 seeds/mm³
过渡层: 12000 seeds/mm³
松质骨: 6000 seeds/mm³
孔隙率: 68%
# 孔隙梯度比: ~3.0 (符合仿生学)
```

#### 高强度支架
```python
皮质骨: 35000 seeds/mm³
过渡层: 20000 seeds/mm³
松质骨: 10000 seeds/mm³
孔隙率: 55%
# 适合承重应用
```

#### 高孔隙支架
```python
皮质骨: 15000 seeds/mm³
过渡层: 8000 seeds/mm³
松质骨: 3000 seeds/mm³
孔隙率: 75%
# 适合营养扩散
```

### 🔬 技术细节

#### 仿生骨结构
```
Z方向梯度（从下到上）:
│
├─ 100% ┐
│       │ 松质骨层 (50%)
│       │ • 低密度: 4K-10K seeds/mm³
├─ 50%  ┤ • 大孔隙: 60-150 μm
│       │ • 高孔隙率
│       │
│       │ 过渡层 (30%)
├─ 20%  ┤ • 中密度: 10K-18K seeds/mm³
│       │ • 中孔隙: 30-60 μm
│       │
│       │ 皮质骨层 (20%)
│       │ • 高密度: 20K-35K seeds/mm³
├─ 0%   ┘ • 小孔隙: 10-30 μm
│         • 高强度
```

### 🎨 可视化输出

点击 **"Save Visuals"** 后生成3张图片：

1. **彩色3D Voronoi** (`colorful_voronoi_3d_*.png`)
   - 多彩多面体单元
   - 清晰边界和种子标记
   - 专业3D渲染

2. **SEM风格支架** (`realistic_scaffold_*.png`)
   - 4个视角
   - 灰度光照效果
   - 扫描电镜美学

3. **梯度分析** (`gradient_analysis_*.png`)
   - 8个子图完整统计
   - 种子分布、孔隙分析
   - 梯度曲线和层级信息

### 📝 引用

如果在研究中使用此工具，请引用：

```bibtex
@software{biomimetic_scaffold_generator_voronoi,
  author = {Siqi (Qizaifadacai)},
  title = {Interactive Biomimetic Bone Scaffold Generator based on Voronoi Tessellation},
  year = {2025},
  url = {https://github.com/Qizaifadacai/biomimetic-bone-scaffold-generator-voronoi}
}
```

### 📄 许可证

本项目采用 MIT 许可证 - 详见 [LICENSE](LICENSE) 文件

---

## 🌐 Links

- 📚 [Detailed Documentation (Chinese)](docs/使用指南_新版本.md)
- 🎯 [Quick Reference (Chinese)](docs/快速参考.md)
- 📊 [Visual Comparison (Chinese)](docs/视觉效果对比.md)
- 🐛 [Issue Tracker](https://github.com/Qizaifadacai/biomimetic-bone-scaffold-generator-voronoi/issues)
- 💬 [Discussions](https://github.com/Qizaifadacai/biomimetic-bone-scaffold-generator-voronoi/discussions)

## 📧 Contact

- **Author:** Siqi (Qizaifadacai)
- **Email:** fortyseven0629@gmail.com
- **GitHub:** [@Qizaifadacai](https://github.com/Qizaifadacai)
- **Research Field:** Tissue Engineering / Stem Cell Research

---

## ⭐ Star History

If you find this project helpful, please consider giving it a star! ⭐

---

<p align="center">
  Made with ❤️ for bone tissue engineering research
</p>

<p align="center">
  <strong>🦴 Advancing Biomimetic Scaffold Design through Computational Methods 🔬</strong>
</p>
  <a href="#top">Back to Top ⬆️</a>
</p>
