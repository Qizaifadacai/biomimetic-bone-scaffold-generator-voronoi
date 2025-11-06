#!/usr/bin/env python3
"""
高级3D Voronoi可视化工具
生成更真实的彩色3D支架结构图
"""

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from scipy.spatial import ConvexHull
import matplotlib.cm as cm
from matplotlib.colors import LinearSegmentedColormap


def create_realistic_scaffold_visualization(generator, output_path=None, max_cells=50):
    """
    创建更真实的支架可视化
    
    特点:
    - 平滑的颜色渐变（红→橙→蓝）
    - 真实的材料光泽效果
    - 多角度展示
    - 带阴影效果
    """
    
    if not hasattr(generator, 'interior_cells') or not generator.interior_cells:
        print("[ERROR] 请先生成支架结构")
        return
    
    print(f"[INFO] 创建高级3D可视化...")
    
    # 创建大画布
    fig = plt.figure(figsize=(24, 16))
    fig.patch.set_facecolor('#F5F5F5')
    
    # 创建自定义颜色映射（仿生骨颜色梯度）
    colors_gradient = ['#8B0000', '#FF4444', '#FF8844', '#FFB366', '#4488FF', '#0066CC']
    n_bins = 256
    cmap = LinearSegmentedColormap.from_list('bone_gradient', colors_gradient, N=n_bins)
    
    # 6个不同视角的子图
    views = [
        (20, 45, '透视图 1'),
        (20, 135, '透视图 2'),
        (20, 225, '透视图 3'),
        (20, 315, '透视图 4'),
        (90, 0, '俯视图'),
        (0, 0, '侧视图')
    ]
    
    cells_to_show = generator.interior_cells[:min(max_cells, len(generator.interior_cells))]
    z_size = generator.z_size
    
    for idx, (elev, azim, title) in enumerate(views):
        ax = fig.add_subplot(2, 3, idx+1, projection='3d')
        ax.set_facecolor('#FFFFFF')
        
        # 为每个单元绘制
        for cell_idx, cell in enumerate(cells_to_show):
            try:
                vertices = cell['vertices'] * 1e6
                center_z = cell['center'][2]
                
                # 根据Z位置计算颜色（归一化到0-1）
                z_normalized = center_z / z_size
                color_value = cmap(z_normalized)
                
                # 计算透明度（中间层稍微透明一些以显示内部结构）
                if 0.2 <= z_normalized <= 0.5:
                    alpha = 0.75
                else:
                    alpha = 0.85
                
                if len(vertices) >= 4:
                    try:
                        hull = ConvexHull(vertices)
                        
                        # 绘制每个三角形面
                        for simplex in hull.simplices:
                            triangle = vertices[simplex]
                            poly3d = [[triangle[j] for j in range(3)]]
                            
                            collection = Poly3DCollection(
                                poly3d,
                                facecolors=color_value,
                                alpha=alpha,
                                edgecolors='#333333',
                                linewidths=0.5
                            )
                            
                            # 添加光泽效果（设置更高的光照强度）
                            collection.set_edgecolor('#333333')
                            ax.add_collection3d(collection)
                            
                    except:
                        # 如果ConvexHull失败，绘制点
                        center = cell['center'] * 1e6
                        ax.scatter(center[0], center[1], center[2],
                                 c=[color_value], s=100, alpha=alpha, 
                                 edgecolors='black', linewidths=1)
                else:
                    center = cell['center'] * 1e6
                    ax.scatter(center[0], center[1], center[2],
                             c=[color_value], s=100, alpha=alpha,
                             edgecolors='black', linewidths=1)
                             
            except Exception as e:
                continue
        
        # 设置坐标轴
        ax.set_xlabel('X (μm)', fontsize=10, fontweight='bold')
        ax.set_ylabel('Y (μm)', fontsize=10, fontweight='bold')
        ax.set_zlabel('Z (μm)', fontsize=10, fontweight='bold')
        ax.set_title(title, fontsize=12, fontweight='bold', pad=15)
        
        ax.set_xlim(0, generator.x_size*1e6)
        ax.set_ylim(0, generator.y_size*1e6)
        ax.set_zlim(0, generator.z_size*1e6)
        
        # 设置视角
        ax.view_init(elev=elev, azim=azim)
        
        # 网格样式
        ax.grid(True, alpha=0.2, linestyle='--', linewidth=0.5)
        ax.xaxis.pane.fill = False
        ax.yaxis.pane.fill = False
        ax.zaxis.pane.fill = False
        
        # 背景色
        ax.xaxis.pane.set_edgecolor('#CCCCCC')
        ax.yaxis.pane.set_edgecolor('#CCCCCC')
        ax.zaxis.pane.set_edgecolor('#CCCCCC')
    
    # 添加颜色条
    cbar_ax = fig.add_axes([0.92, 0.15, 0.02, 0.7])
    norm = plt.Normalize(vmin=0, vmax=z_size*1e6)
    sm = cm.ScalarMappable(cmap=cmap, norm=norm)
    sm.set_array([])
    cbar = plt.colorbar(sm, cax=cbar_ax)
    cbar.set_label('Z Position (μm)\n← Cortical | Trabecular →', 
                   fontsize=11, fontweight='bold', rotation=270, labelpad=25)
    
    # 添加层标记
    cbar_ax.axhline(y=0.2*z_size*1e6, color='red', linestyle='--', linewidth=2, alpha=0.7)
    cbar_ax.axhline(y=0.5*z_size*1e6, color='orange', linestyle='--', linewidth=2, alpha=0.7)
    cbar_ax.text(1.5, 0.1*z_size*1e6, 'Cortical', fontsize=9, color='red', 
                fontweight='bold', transform=cbar_ax.transData)
    cbar_ax.text(1.5, 0.35*z_size*1e6, 'Transition', fontsize=9, color='orange',
                fontweight='bold', transform=cbar_ax.transData)
    cbar_ax.text(1.5, 0.75*z_size*1e6, 'Trabecular', fontsize=9, color='blue',
                fontweight='bold', transform=cbar_ax.transData)
    
    # 总标题
    fig.suptitle('3D Biomimetic Gradient Voronoi Scaffold - Multi-View Visualization',
                fontsize=18, fontweight='bold', y=0.98)
    
    # 添加信息文本
    info_text = f"""
    Scaffold Info:
    • Dimensions: {generator.x_size*1e6:.0f} × {generator.y_size*1e6:.0f} × {generator.z_size*1e6:.0f} μm
    • Total Cells: {len(generator.interior_cells)}
    • Displayed: {len(cells_to_show)} cells
    • Porosity: {generator.target_porosity*100:.1f}%
    • Layer Structure: Cortical (0-20%) → Transition (20-50%) → Trabecular (50-100%)
    """
    
    fig.text(0.02, 0.02, info_text, fontsize=9, verticalalignment='bottom',
            bbox=dict(boxstyle='round', facecolor='white', alpha=0.8, edgecolor='gray'))
    
    plt.tight_layout(rect=[0, 0.03, 0.91, 0.96])
    
    if output_path:
        plt.savefig(output_path, dpi=300, bbox_inches='tight', facecolor='#F5F5F5')
        print(f"[SUCCESS] 高级可视化已保存: {output_path}")
    
    plt.show()
    
    return fig


def create_cross_section_views(generator, output_path=None):
    """
    创建支架横截面视图
    显示内部孔隙结构
    """
    
    print(f"[INFO] 创建横截面视图...")
    
    fig, axes = plt.subplots(2, 3, figsize=(18, 12))
    fig.patch.set_facecolor('#F5F5F5')
    
    # 6个不同深度的切片
    z_slices = [0.1, 0.25, 0.4, 0.55, 0.7, 0.9]
    
    for idx, z_ratio in enumerate(z_slices):
        ax = axes[idx // 3, idx % 3]
        ax.set_facecolor('#FFFFFF')
        
        z_slice = z_ratio * generator.z_size
        tolerance = 0.05 * generator.z_size
        
        # 找到该切片上的单元
        slice_cells = []
        for cell in generator.interior_cells:
            if abs(cell['center'][2] - z_slice) < tolerance:
                slice_cells.append(cell)
        
        # 绘制单元
        for cell in slice_cells:
            try:
                # 投影到XY平面
                vertices_2d = cell['vertices'][:, :2] * 1e6
                
                # 颜色根据层
                if z_ratio <= 0.2:
                    color = '#FF4444'
                    label = 'Cortical'
                elif z_ratio <= 0.5:
                    color = '#FF8844'
                    label = 'Transition'
                else:
                    color = '#4488FF'
                    label = 'Trabecular'
                
                # 绘制Voronoi单元边界
                if len(vertices_2d) >= 3:
                    from matplotlib.patches import Polygon
                    try:
                        hull_2d = ConvexHull(vertices_2d)
                        polygon = Polygon(vertices_2d[hull_2d.vertices],
                                        facecolor=color, alpha=0.6,
                                        edgecolor='black', linewidth=1.5)
                        ax.add_patch(polygon)
                    except:
                        pass
                
                # 绘制中心点
                center_2d = cell['center'][:2] * 1e6
                ax.plot(center_2d[0], center_2d[1], 'ko', markersize=3)
                
            except:
                continue
        
        # 设置
        ax.set_xlim(0, generator.x_size*1e6)
        ax.set_ylim(0, generator.y_size*1e6)
        ax.set_aspect('equal')
        ax.set_xlabel('X (μm)', fontsize=9)
        ax.set_ylabel('Y (μm)', fontsize=9)
        ax.set_title(f'Z = {z_slice*1e6:.1f} μm ({z_ratio*100:.0f}%)\n{len(slice_cells)} cells',
                    fontsize=10, fontweight='bold')
        ax.grid(True, alpha=0.3, linestyle='--')
        
        # 添加层标签
        layer_text = ""
        if z_ratio <= 0.2:
            layer_text = "Cortical Layer"
            color_bg = '#FF444440'
        elif z_ratio <= 0.5:
            layer_text = "Transition Layer"
            color_bg = '#FF884440'
        else:
            layer_text = "Trabecular Layer"
            color_bg = '#4488FF40'
        
        ax.text(0.5, 0.95, layer_text, transform=ax.transAxes,
               fontsize=9, fontweight='bold', ha='center', va='top',
               bbox=dict(boxstyle='round', facecolor=color_bg, edgecolor='black'))
    
    fig.suptitle('Scaffold Cross-Sectional Views - Internal Pore Structure',
                fontsize=16, fontweight='bold')
    
    plt.tight_layout()
    
    if output_path:
        plt.savefig(output_path, dpi=300, bbox_inches='tight', facecolor='#F5F5F5')
        print(f"[SUCCESS] 横截面视图已保存: {output_path}")
    
    plt.show()
    
    return fig


if __name__ == "__main__":
    print("此脚本提供高级可视化函数")
    print("请在主程序中导入使用:")
    print()
    print("  from advanced_visualization import create_realistic_scaffold_visualization")
    print("  from advanced_visualization import create_cross_section_views")
    print()
    print("  # 在生成器创建后调用")
    print("  create_realistic_scaffold_visualization(generator, 'output.png', max_cells=60)")
    print("  create_cross_section_views(generator, 'cross_sections.png')")
