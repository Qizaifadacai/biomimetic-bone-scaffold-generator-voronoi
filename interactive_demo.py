#!/usr/bin/env python3
"""
交互式梯度Voronoi支架生成器 - 演示脚本
可实时调整种子密度、生成彩色3D Voronoi图和仿真支架
"""

import sys
import os

# 确保可以导入主模块
sys.path.insert(0, os.path.dirname(__file__))

from 支持梯度的Voronoi支架生成器 import InteractiveGradientScaffoldGenerator

def main():
    """主函数 - 启动交互式界面"""
    
    print("╔══════════════════════════════════════════════════════════╗")
    print("║     交互式仿生骨支架生成器 - 演示程序                     ║")
    print("║     Interactive Biomimetic Scaffold Generator            ║")
    print("╚══════════════════════════════════════════════════════════╝")
    print()
    print("功能特点:")
    print("  ✓ 实时调整种子密度分布（皮质骨、过渡层、松质骨）")
    print("  ✓ 动态调整目标孔隙率")
    print("  ✓ 彩色3D Voronoi结构可视化")
    print("  ✓ 实时孔隙分析和梯度曲线")
    print("  ✓ 一键保存STL文件")
    print()
    print("操作说明:")
    print("  1. 使用滑块调整参数")
    print("  2. 点击 'Generate Scaffold' 按钮生成支架")
    print("  3. 点击 'Save STL' 按钮保存当前支架")
    print()
    print("正在启动交互式界面...")
    print()
    
    # 创建交互式生成器
    generator = InteractiveGradientScaffoldGenerator(
        x_size=800e-6,      # 800 μm
        y_size=800e-6,      # 800 μm
        z_size=100e-6,      # 100 μm
        target_porosity=0.68  # 68% 孔隙率
    )
    
    # 启动交互式界面
    generator.create_interactive_interface()
    

if __name__ == "__main__":
    main()
