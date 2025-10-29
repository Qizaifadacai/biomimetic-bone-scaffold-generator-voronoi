#!/usr/bin/env python3
"""
新版本演示 - 输入框交互 + 彩色Voronoi + SEM仿真支架
"""

import sys
import os

def main():
    print("╔════════════════════════════════════════════════════════════╗")
    print("║   交互式仿生骨支架生成器 - 新版本                          ║")
    print("║   Interactive Biomimetic Scaffold Generator v2.0          ║")
    print("╚════════════════════════════════════════════════════════════╝")
    print()
    print("新特性:")
    print("  ✨ 输入框交互 - 直接输入精确数值，无需滑块")
    print("  🎨 彩色3D Voronoi - 30+种颜色的多彩多面体")
    print("  📸 SEM仿真支架 - 灰度渲染的4视角扫描电镜效果")
    print("  💾 一键保存 - 自动生成3种高清可视化图")
    print()
    print("操作方法:")
    print("  1️⃣  在输入框中直接输入数值")
    print("  2️⃣  按Enter键确认")
    print("  3️⃣  点击 'Generate Scaffold' 生成")
    print("  4️⃣  点击 'Save Visuals' 保存图片")
    print()
    print("参数范围:")
    print("  • 皮质骨密度: 5,000 - 40,000 seeds/mm³")
    print("  • 过渡层密度: 3,000 - 25,000 seeds/mm³")
    print("  • 松质骨密度: 1,000 - 15,000 seeds/mm³")
    print("  • 目标孔隙率: 40 - 85 %")
    print()
    print("推荐参数（标准仿生骨）:")
    print("  Cortical: 25000, Transition: 12000, Trabecular: 6000, Porosity: 68%")
    print()
    
    input("按 Enter 启动交互式界面...")
    
    try:
        from 支持梯度的Voronoi支架生成器 import InteractiveGradientScaffoldGenerator
        
        generator = InteractiveGradientScaffoldGenerator(
            x_size=800e-6,
            y_size=800e-6,
            z_size=100e-6,
            target_porosity=0.68
        )
        
        print("\n[INFO] 正在启动交互式界面...")
        print("       • 界面包含6个实时更新的图表")
        print("       • 输入数值后按Enter确认")
        print("       • 点击按钮生成或保存\n")
        
        generator.create_interactive_interface()
        
    except Exception as e:
        print(f"\n❌ 启动失败: {e}")
        print("\n可能的原因:")
        print("  1. 缺少依赖包: pip install numpy scipy matplotlib numpy-stl")
        print("  2. 无法导入主模块: 检查文件路径")
        print("  3. 显示环境问题: 确保在有GUI的环境中运行")
        
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
