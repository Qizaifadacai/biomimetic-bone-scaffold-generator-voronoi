#!/usr/bin/env python3
"""
快速测试脚本 - 验证所有功能
"""

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

def test_basic_generation():
    """测试基本生成功能"""
    print("\n" + "="*60)
    print("测试1: 基本支架生成")
    print("="*60)
    
    from 支持梯度的Voronoi支架生成器 import GradientVoronoiScaffoldGenerator
    
    generator = GradientVoronoiScaffoldGenerator(
        x_size=800e-6,
        y_size=800e-6,
        z_size=100e-6,
        target_porosity=0.68
    )
    
    print("✓ 生成器创建成功")
    
    # 生成梯度种子
    generator.generate_seeds_with_gradient({
        'surface_density': 25000,
        'middle_density': 12000,
        'core_density': 6000
    })
    print("✓ 梯度种子生成成功")
    
    # 计算Voronoi
    generator.compute_voronoi()
    print("✓ Voronoi计算成功")
    
    generator.extract_interior_cells()
    print("✓ 内部单元提取成功")
    
    generator.compute_cell_statistics()
    print("✓ 单元统计完成")
    
    generator.analyze_gradient_properties()
    print("✓ 梯度分析完成")
    
    return generator


def test_visualization(generator):
    """测试可视化功能"""
    print("\n" + "="*60)
    print("测试2: 可视化功能")
    print("="*60)
    
    import matplotlib
    matplotlib.use('Agg')  # 非交互式后端
    
    output_dir = "/Users/kiki/Desktop/bone scaffold/ Voronoi scaffold"
    
    # 测试梯度结构图
    try:
        gradient_fig_path = output_dir + "/test_gradient_analysis.png"
        generator.visualize_gradient_structure(gradient_fig_path)
        print("✓ 梯度结构图生成成功")
    except Exception as e:
        print(f"✗ 梯度结构图失败: {e}")
    
    # 测试3D Voronoi图
    try:
        voronoi_3d_path = output_dir + "/test_3d_voronoi.png"
        generator.visualize_3d_gradient_voronoi(voronoi_3d_path, max_cells=20)
        print("✓ 3D Voronoi图生成成功")
    except Exception as e:
        print(f"✗ 3D Voronoi图失败: {e}")


def test_stl_export(generator):
    """测试STL导出"""
    print("\n" + "="*60)
    print("测试3: STL导出")
    print("="*60)
    
    output_dir = "/Users/kiki/Desktop/bone scaffold/ Voronoi scaffold"
    
    try:
        generator.generate_stl_mesh()
        print("✓ STL网格生成成功")
        
        stl_file = output_dir + "/test_scaffold.stl"
        generator.save_stl(stl_file)
        print(f"✓ STL文件保存成功: {stl_file}")
        
        config_file = output_dir + "/test_config.json"
        generator.export_config_json(config_file)
        print(f"✓ 配置文件保存成功: {config_file}")
        
    except Exception as e:
        print(f"✗ STL导出失败: {e}")


def test_interactive_class():
    """测试交互式类的创建"""
    print("\n" + "="*60)
    print("测试4: 交互式类")
    print("="*60)
    
    try:
        from 支持梯度的Voronoi支架生成器 import InteractiveGradientScaffoldGenerator
        
        interactive = InteractiveGradientScaffoldGenerator(
            x_size=800e-6,
            y_size=800e-6,
            z_size=100e-6,
            target_porosity=0.68
        )
        print("✓ 交互式生成器类创建成功")
        print("  (注意: 实际交互界面需要在有GUI的环境中运行)")
        
    except Exception as e:
        print(f"✗ 交互式类创建失败: {e}")


def test_advanced_visualization():
    """测试高级可视化"""
    print("\n" + "="*60)
    print("测试5: 高级可视化工具")
    print("="*60)
    
    try:
        from advanced_visualization import create_realistic_scaffold_visualization
        from advanced_visualization import create_cross_section_views
        print("✓ 高级可视化模块导入成功")
        
    except Exception as e:
        print(f"✗ 高级可视化模块导入失败: {e}")


def main():
    """运行所有测试"""
    print("\n" + "╔" + "="*58 + "╗")
    print("║" + " "*15 + "支架生成器功能测试" + " "*15 + "║")
    print("╚" + "="*58 + "╝")
    
    try:
        # 测试1: 基本生成
        generator = test_basic_generation()
        
        # 测试2: 可视化
        test_visualization(generator)
        
        # 测试3: STL导出
        test_stl_export(generator)
        
        # 测试4: 交互式类
        test_interactive_class()
        
        # 测试5: 高级可视化
        test_advanced_visualization()
        
        print("\n" + "="*60)
        print("✅ 所有测试完成!")
        print("="*60)
        print("\n现在你可以:")
        print("  1. 运行 'python interactive_demo.py' 启动交互式界面")
        print("  2. 运行 '支持梯度的Voronoi支架生成器.py' 直接生成支架")
        print("  3. 查看生成的测试文件在 Voronoi scaffold 目录")
        
    except Exception as e:
        print(f"\n❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
