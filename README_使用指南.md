# 交互式梯度Voronoi支架生成器 - 使用指南

## 📋 功能概述

这是一个用于生成仿生骨支架的交互式工具，具有以下特点：

- ✅ **交互式参数调整**：实时调整种子密度和孔隙率
- ✅ **彩色3D Voronoi可视化**：按梯度着色的3D结构图
- ✅ **仿真支架图**：多角度、多切面的真实支架展示
- ✅ **梯度分析**：自动分析仿生骨结构特性
- ✅ **STL导出**：支持3D打印的STL文件导出

## 🚀 快速开始

### 方法1: 交互式界面（推荐）

```bash
python interactive_demo.py
```

或直接运行主脚本并选择模式1：

```bash
python 支持梯度的Voronoi支架生成器.py
# 输入: 1
```

### 方法2: 直接生成（使用默认参数）

```bash
python 支持梯度的Voronoi支架生成器.py
# 输入: 2
```

## 🎮 交互式界面使用

### 界面布局

交互式界面包含以下部分：

1. **3D种子分布图**（左上）
   - 显示按层着色的种子点分布
   - 红色：皮质骨层（0-20%）
   - 橙色：过渡层（20-50%）
   - 蓝色：松质骨层（50-100%）

2. **3D Voronoi结构图**（右上）
   - 彩色3D Voronoi单元
   - 展示梯度孔隙结构

3. **密度分布图**（下方左）
   - 各层种子密度柱状图

4. **孔隙分析图**（下方中左）
   - 各层平均孔隙大小

5. **梯度曲线图**（下方中右）
   - Z方向孔隙大小变化趋势

6. **统计信息面板**（下方右）
   - 支架参数和统计数据

### 控制滑块

- **Cortical Density (皮质骨密度)**
  - 范围: 5,000 - 40,000 seeds/mm³
  - 控制外层（皮质骨）的种子密度
  - 密度越高，孔隙越小

- **Transition Density (过渡层密度)**
  - 范围: 3,000 - 25,000 seeds/mm³
  - 控制中间层的种子密度

- **Trabecular Density (松质骨密度)**
  - 范围: 1,000 - 15,000 seeds/mm³
  - 控制内层（松质骨）的种子密度
  - 密度越低，孔隙越大

- **Target Porosity (目标孔隙率)**
  - 范围: 40% - 85%
  - 控制整体孔隙率

### 操作按钮

- **Generate Scaffold（绿色）**
  - 根据当前滑块参数生成新的支架
  - 自动更新所有可视化图

- **Save STL（蓝色）**
  - 保存当前支架为STL文件
  - 同时保存配置JSON文件
  - 文件名包含时间戳

## 📊 高级可视化

### 使用高级可视化工具

```python
from 支持梯度的Voronoi支架生成器 import GradientVoronoiScaffoldGenerator
from advanced_visualization import create_realistic_scaffold_visualization, create_cross_section_views

# 创建生成器
generator = GradientVoronoiScaffoldGenerator(
    x_size=800e-6,
    y_size=800e-6,
    z_size=100e-6,
    target_porosity=0.68
)

# 生成支架
generator.generate_seeds_with_gradient()
generator.compute_voronoi()
generator.extract_interior_cells()
generator.compute_cell_statistics()
generator.analyze_gradient_properties()

# 生成高级可视化
create_realistic_scaffold_visualization(
    generator, 
    output_path='realistic_scaffold.png',
    max_cells=60  # 显示更多单元
)

# 生成横截面视图
create_cross_section_views(
    generator,
    output_path='cross_sections.png'
)
```

### 多角度3D Voronoi图

高级可视化工具会生成6个视角的支架图：
- 4个透视图（不同旋转角度）
- 1个俯视图
- 1个侧视图

每个单元都根据其Z位置着色，形成平滑的颜色梯度。

## 🎨 自定义参数示例

### 示例1: 高密度皮质骨支架

```python
generator = InteractiveGradientScaffoldGenerator(
    x_size=800e-6,
    y_size=800e-6,
    z_size=100e-6,
    target_porosity=0.55  # 较低孔隙率
)

# 在交互界面中设置：
# - Cortical Density: 35000
# - Transition Density: 20000
# - Trabecular Density: 10000
```

### 示例2: 高孔隙松质骨支架

```python
generator = InteractiveGradientScaffoldGenerator(
    x_size=800e-6,
    y_size=800e-6,
    z_size=100e-6,
    target_porosity=0.75  # 较高孔隙率
)

# 在交互界面中设置：
# - Cortical Density: 15000
# - Transition Density: 8000
# - Trabecular Density: 3000
```

### 示例3: 更大尺寸支架

```python
generator = InteractiveGradientScaffoldGenerator(
    x_size=1500e-6,   # 1.5 mm
    y_size=1500e-6,   # 1.5 mm
    z_size=300e-6,    # 300 μm
    target_porosity=0.68
)
```

## 📁 输出文件

所有输出文件保存在：
```
/Users/kiki/Desktop/bone scaffold/ Voronoi scaffold/
```

### 文件类型

1. **STL文件** (`*.stl`)
   - 3D打印用的网格文件
   - 可在Meshmixer、Blender等软件中打开

2. **配置文件** (`*.json`)
   - 包含所有参数和统计信息
   - 便于追溯和复现

3. **可视化图片** (`*.png`)
   - 高分辨率（300 DPI）
   - 适合论文和报告使用

### 生成的图片

- `scaffold_structure_analysis.png` - 基础结构分析
- `biomimetic_gradient_analysis.png` - 梯度结构详细分析
- `3d_gradient_voronoi_structure.png` - 彩色3D Voronoi图
- `3d_voronoi_cells.png` - 基础3D单元图
- `realistic_scaffold.png` - 高级多视角真实支架图（需手动调用）
- `cross_sections.png` - 横截面视图（需手动调用）

## 🔬 仿生学参数建议

根据天然骨结构，推荐的参数范围：

| 层级 | 密度 (seeds/mm³) | 孔隙大小 | 特点 |
|------|-----------------|---------|------|
| 皮质骨层 | 20,000 - 35,000 | 小 (10-30 μm) | 高密度，高强度 |
| 过渡层 | 10,000 - 18,000 | 中 (30-60 μm) | 中等密度 |
| 松质骨层 | 4,000 - 10,000 | 大 (60-150 μm) | 低密度，高孔隙 |

### 孔隙梯度比

理想的孔隙梯度比（松质骨/皮质骨）应在 **2.0 - 5.0** 之间，以模拟天然骨的特性。

## ⚙️ 技术细节

### 仿生骨结构分层

```
Z方向分层（从底部到顶部）:
├─ 0-20%   : 皮质骨层（Cortical Layer）
├─ 20-50%  : 过渡层（Transition Layer）
└─ 50-100% : 松质骨层（Trabecular Layer）
```

### 颜色编码

- **红色 (#FF4444)**: 皮质骨层 - 高密度，小孔隙
- **橙色 (#FF8844)**: 过渡层 - 中等密度
- **蓝色 (#4488FF)**: 松质骨层 - 低密度，大孔隙

## 🐛 常见问题

### Q1: 生成的支架孔隙梯度不明显？

**A**: 增大各层密度的差异，例如：
- 皮质骨: 30000
- 过渡层: 15000
- 松质骨: 5000

### Q2: 程序运行缓慢？

**A**: 
- 减小支架尺寸
- 降低种子密度
- 减少可视化显示的单元数量（max_cells参数）

### Q3: STL文件无法打开？

**A**: 确保已正确生成STL文件，检查：
```python
generator.generate_stl_mesh()  # 必须先调用此方法
generator.save_stl(filename)
```

### Q4: 可视化图片不够清晰？

**A**: 使用高级可视化工具，并增加DPI：
```python
plt.savefig(output_path, dpi=600, bbox_inches='tight')
```

## 📞 技术支持

如有问题，请检查：
1. 是否正确安装了所有依赖包（numpy, scipy, matplotlib等）
2. 是否正确导入了 `voronoi_scaffold_generator` 模块
3. 输出目录是否存在并有写入权限

## 🎓 引用与参考

本工具基于Voronoi算法生成仿生骨支架，适用于：
- 骨组织工程研究
- 3D打印支架设计
- 仿生材料结构优化

---

**版本**: 1.0  
**更新日期**: 2025-10-26  
**作者**: Kiki
