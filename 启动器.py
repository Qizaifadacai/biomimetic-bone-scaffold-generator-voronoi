#!/usr/bin/env python3
"""
一键启动脚本 - 选择你想要的功能
"""

import sys
import os

def print_menu():
    """显示菜单"""
    print("\n" + "╔" + "="*58 + "╗")
    print("║" + " "*10 + "仿生骨支架生成器 - 主菜单" + " "*10 + "║")
    print("╚" + "="*58 + "╝\n")
    
    print("请选择功能:\n")
    print("  [1] 🎮 交互式界面")
    print("      → 实时调整参数，可视化预览")
    print("      → 推荐用于参数调试和探索\n")
    
    print("  [2] 🚀 快速生成")
    print("      → 使用默认参数直接生成")
    print("      → 生成所有可视化图和STL文件\n")
    
    print("  [3] 🧪 功能测试")
    print("      → 测试所有功能是否正常")
    print("      → 生成测试文件\n")
    
    print("  [4] 📖 查看使用指南")
    print("      → 打开详细的使用文档\n")
    
    print("  [0] ❌ 退出\n")
    print("-" * 60)


def run_interactive():
    """运行交互式界面"""
    print("\n🎮 启动交互式界面...")
    print("=" * 60)
    
    try:
        from 支持梯度的Voronoi支架生成器 import InteractiveGradientScaffoldGenerator
        
        generator = InteractiveGradientScaffoldGenerator(
            x_size=800e-6,
            y_size=800e-6,
            z_size=100e-6,
            target_porosity=0.68
        )
        
        print("\n使用说明:")
        print("  • 使用滑块调整参数")
        print("  • 点击 'Generate Scaffold' 生成新支架")
        print("  • 点击 'Save STL' 保存当前支架")
        print("  • 关闭窗口退出\n")
        
        generator.create_interactive_interface()
        
    except Exception as e:
        print(f"❌ 启动失败: {e}")
        import traceback
        traceback.print_exc()


def run_quick_generation():
    """快速生成支架"""
    print("\n🚀 快速生成模式...")
    print("=" * 60)
    
    try:
        from 支持梯度的Voronoi支架生成器 import GradientVoronoiScaffoldGenerator
        
        # 创建生成器
        print("\n[1/8] 创建生成器...")
        generator = GradientVoronoiScaffoldGenerator(
            x_size=800e-6,
            y_size=800e-6,
            z_size=100e-6,
            target_porosity=0.68
        )
        
        # 生成梯度种子
        print("[2/8] 生成梯度种子...")
        generator.generate_seeds_with_gradient()
        
        # 计算Voronoi
        print("[3/8] 计算Voronoi结构...")
        generator.compute_voronoi()
        generator.extract_interior_cells()
        generator.compute_cell_statistics()
        
        # 分析梯度
        print("[4/8] 分析梯度特性...")
        generator.analyze_gradient_properties()
        
        # 生成STL
        print("[5/8] 生成STL网格...")
        generator.generate_stl_mesh()
        
        # 保存文件
        output_dir = "/Users/kiki/Desktop/bone scaffold/ Voronoi scaffold"
        
        print("[6/8] 保存文件...")
        stl_file = output_dir + "/voronoi_scaffold_gradient.stl"
        config_file = output_dir + "/scaffold_gradient_config.json"
        generator.save_stl(stl_file)
        generator.export_config_json(config_file)
        
        # 生成可视化
        print("[7/8] 生成可视化图...")
        
        structure_fig = output_dir + "/scaffold_structure_analysis.png"
        generator.visualize_scaffold_structure(structure_fig)
        
        gradient_fig = output_dir + "/biomimetic_gradient_analysis.png"
        generator.visualize_gradient_structure(gradient_fig)
        
        voronoi_3d = output_dir + "/3d_gradient_voronoi_structure.png"
        generator.visualize_3d_gradient_voronoi(voronoi_3d, max_cells=35)
        
        # 完成
        print("[8/8] 完成!")
        print("\n" + "=" * 60)
        print("✅ 支架生成成功!")
        print("=" * 60)
        print(f"\n输出目录: {output_dir}")
        print("\n生成的文件:")
        print(f"  • {stl_file}")
        print(f"  • {config_file}")
        print(f"  • {structure_fig}")
        print(f"  • {gradient_fig}")
        print(f"  • {voronoi_3d}")
        
    except Exception as e:
        print(f"\n❌ 生成失败: {e}")
        import traceback
        traceback.print_exc()


def run_tests():
    """运行测试"""
    print("\n🧪 运行功能测试...")
    print("=" * 60)
    
    try:
        import test_all_features
        test_all_features.main()
        
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()


def show_guide():
    """显示使用指南"""
    print("\n📖 使用指南")
    print("=" * 60)
    
    guide_path = "/Users/kiki/Desktop/bone scaffold/README_使用指南.md"
    
    if os.path.exists(guide_path):
        print(f"\n使用指南路径: {guide_path}")
        print("\n你可以:")
        print("  1. 在文本编辑器中打开该文件")
        print("  2. 使用Markdown阅读器查看（推荐）")
        
        # 尝试打开文件
        try:
            if sys.platform == 'darwin':  # macOS
                os.system(f'open "{guide_path}"')
                print("\n✓ 已在默认应用中打开使用指南")
            else:
                print(f"\n请手动打开: {guide_path}")
        except:
            print(f"\n请手动打开: {guide_path}")
    else:
        print(f"\n❌ 找不到使用指南: {guide_path}")
        print("\n基本使用:")
        print("  1. 运行交互式界面调整参数")
        print("  2. 或使用快速生成模式")
        print("  3. 生成的文件保存在 Voronoi scaffold 目录")


def main():
    """主函数"""
    while True:
        print_menu()
        
        try:
            choice = input("请输入选项 [0-4]: ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\n\n👋 再见!")
            break
        
        if choice == '1':
            run_interactive()
        elif choice == '2':
            run_quick_generation()
        elif choice == '3':
            run_tests()
        elif choice == '4':
            show_guide()
        elif choice == '0':
            print("\n👋 再见!")
            break
        else:
            print("\n⚠️  无效选项，请输入 0-4")
        
        if choice != '0':
            input("\n按 Enter 继续...")


if __name__ == "__main__":
    main()
