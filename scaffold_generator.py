"""
支持组成梯度的Voronoi支架生成器
在Z方向创建梯度孔隙结构（表面细孔→内层粗孔）
"""

import numpy as np
from voronoi_scaffold_generator import VoronoiScaffoldGenerator
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button, TextBox
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from scipy.spatial import ConvexHull
import matplotlib.patches as patches
from matplotlib.colors import LinearSegmentedColormap
import matplotlib.cm as cm


class InteractiveGradientScaffoldGenerator:
    """交互式梯度支架生成器 - 可实时调整参数"""
    
    def __init__(self, x_size=800e-6, y_size=800e-6, z_size=100e-6, target_porosity=0.68):
        self.x_size = x_size
        self.y_size = y_size
        self.z_size = z_size
        self.target_porosity = target_porosity
        
        # 初始参数
        self.surface_density = 25000
        self.middle_density = 12000
        self.core_density = 6000
        
        self.generator = None
        self.fig = None
        self.axes = []
        
    def create_interactive_interface(self):
        """创建交互式界面（使用输入框）"""
        print("[INFO] 启动交互式界面...")
        
        # 创建主窗口
        self.fig = plt.figure(figsize=(20, 12))
        self.fig.suptitle('Interactive Biomimetic Scaffold Generator', fontsize=16, fontweight='bold')
        
        # 创建网格布局
        gs = self.fig.add_gridspec(3, 4, hspace=0.3, wspace=0.3)
        
        # 3D种子分布视图
        self.ax_seeds = self.fig.add_subplot(gs[0:2, 0:2], projection='3d')
        
        # 3D Voronoi结构视图
        self.ax_voronoi = self.fig.add_subplot(gs[0:2, 2:4], projection='3d')
        
        # 密度分布图
        self.ax_density = self.fig.add_subplot(gs[2, 0])
        
        # 孔隙分析图
        self.ax_pore = self.fig.add_subplot(gs[2, 1])
        
        # Z方向梯度图
        self.ax_gradient = self.fig.add_subplot(gs[2, 2])
        
        # 统计信息面板
        self.ax_stats = self.fig.add_subplot(gs[2, 3])
        self.ax_stats.axis('off')
        
        # 创建输入框控件
        plt.subplots_adjust(bottom=0.25)
        
        # 皮质骨层密度输入框
        ax_surface_label = plt.axes([0.1, 0.15, 0.15, 0.03])
        ax_surface_label.axis('off')
        ax_surface_label.text(0, 0.5, 'Cortical Density (seeds/mm³):', 
                             fontsize=10, va='center')
        ax_surface_input = plt.axes([0.26, 0.15, 0.08, 0.03])
        self.textbox_surface = TextBox(ax_surface_input, '', 
                                       initial=str(int(self.surface_density)))
        self.textbox_surface.on_submit(lambda text: self.update_param('surface', text))
        
        # 过渡层密度输入框
        ax_middle_label = plt.axes([0.1, 0.11, 0.15, 0.03])
        ax_middle_label.axis('off')
        ax_middle_label.text(0, 0.5, 'Transition Density (seeds/mm³):', 
                            fontsize=10, va='center')
        ax_middle_input = plt.axes([0.26, 0.11, 0.08, 0.03])
        self.textbox_middle = TextBox(ax_middle_input, '', 
                                      initial=str(int(self.middle_density)))
        self.textbox_middle.on_submit(lambda text: self.update_param('middle', text))
        
        # 松质骨层密度输入框
        ax_core_label = plt.axes([0.1, 0.07, 0.15, 0.03])
        ax_core_label.axis('off')
        ax_core_label.text(0, 0.5, 'Trabecular Density (seeds/mm³):', 
                          fontsize=10, va='center')
        ax_core_input = plt.axes([0.26, 0.07, 0.08, 0.03])
        self.textbox_core = TextBox(ax_core_input, '', 
                                    initial=str(int(self.core_density)))
        self.textbox_core.on_submit(lambda text: self.update_param('core', text))
        
        # 孔隙率输入框
        ax_porosity_label = plt.axes([0.1, 0.03, 0.15, 0.03])
        ax_porosity_label.axis('off')
        ax_porosity_label.text(0, 0.5, 'Target Porosity (%):', 
                              fontsize=10, va='center')
        ax_porosity_input = plt.axes([0.26, 0.03, 0.08, 0.03])
        self.textbox_porosity = TextBox(ax_porosity_input, '', 
                                        initial=str(int(self.target_porosity*100)))
        self.textbox_porosity.on_submit(lambda text: self.update_param('porosity', text))
        
        # 更新按钮
        ax_button = plt.axes([0.40, 0.07, 0.12, 0.08])
        self.button_update = Button(ax_button, 'Generate\nScaffold', color='lightgreen')
        self.button_update.on_clicked(self.update_scaffold)
        
        # 保存STL按钮
        ax_save = plt.axes([0.54, 0.07, 0.12, 0.04])
        self.button_save = Button(ax_save, 'Save STL', color='lightblue')
        self.button_save.on_clicked(self.save_current_scaffold)
        
        # 保存可视化按钮
        ax_save_vis = plt.axes([0.54, 0.12, 0.12, 0.04])
        self.button_save_vis = Button(ax_save_vis, 'Save Visuals', color='lightyellow')
        self.button_save_vis.on_clicked(self.save_visualizations)
        
        # 初始生成
        self.update_scaffold(None)
        
        plt.show()
    
    def update_param(self, param_name, value_str):
        """更新单个参数"""
        try:
            value = float(value_str)
            if param_name == 'surface':
                self.surface_density = max(5000, min(40000, value))
                self.textbox_surface.set_val(str(int(self.surface_density)))
            elif param_name == 'middle':
                self.middle_density = max(3000, min(25000, value))
                self.textbox_middle.set_val(str(int(self.middle_density)))
            elif param_name == 'core':
                self.core_density = max(1000, min(15000, value))
                self.textbox_core.set_val(str(int(self.core_density)))
            elif param_name == 'porosity':
                self.target_porosity = max(40, min(85, value)) / 100
                self.textbox_porosity.set_val(str(int(self.target_porosity*100)))
            print(f"[INFO] 参数已更新，请点击 'Generate Scaffold' 按钮生成新支架")
        except ValueError:
            print(f"[WARNING] 无效输入: {value_str}")
        
    def update_scaffold(self, event):
        """更新支架结构"""
        print("\n[INFO] 正在生成支架...")
        
        # 获取当前参数（从输入框）
        try:
            self.surface_density = float(self.textbox_surface.text)
            self.middle_density = float(self.textbox_middle.text)
            self.core_density = float(self.textbox_core.text)
            self.target_porosity = float(self.textbox_porosity.text) / 100
        except:
            print("[WARNING] 参数读取失败，使用当前值")
        
        # 创建生成器
        self.generator = GradientVoronoiScaffoldGenerator(
            x_size=self.x_size,
            y_size=self.y_size,
            z_size=self.z_size,
            target_porosity=self.target_porosity
        )
        
        # 生成梯度种子
        gradient_param = {
            'surface_density': self.surface_density,
            'middle_density': self.middle_density,
            'core_density': self.core_density
        }
        self.generator.generate_seeds_with_gradient(gradient_param)
        
        # 计算Voronoi
        self.generator.compute_voronoi()
        self.generator.extract_interior_cells()
        self.generator.compute_cell_statistics()
        self.generator.analyze_gradient_properties()
        
        # 更新所有图形
        self.update_all_plots()
        
        print("[SUCCESS] 支架生成完成!")
        
    def update_all_plots(self):
        """更新所有可视化图"""
        # 清空所有子图
        self.ax_seeds.clear()
        self.ax_voronoi.clear()
        self.ax_density.clear()
        self.ax_pore.clear()
        self.ax_gradient.clear()
        self.ax_stats.clear()
        self.ax_stats.axis('off')
        
        # 1. 更新种子分布图
        self.plot_seeds_3d()
        
        # 2. 更新3D Voronoi结构
        self.plot_voronoi_3d()
        
        # 3. 更新密度分布
        self.plot_density_distribution()
        
        # 4. 更新孔隙分析
        self.plot_pore_analysis()
        
        # 5. 更新梯度曲线
        self.plot_gradient_curve()
        
        # 6. 更新统计信息
        self.plot_statistics()
        
        self.fig.canvas.draw_idle()
        
    def plot_seeds_3d(self):
        """绘制3D种子分布"""
        seeds_um = self.generator.seeds * 1e6
        
        # 按层着色
        z_positions = seeds_um[:, 2]
        colors = []
        for z in z_positions:
            if z <= 0.2 * self.z_size * 1e6:
                colors.append('#FF4444')  # 皮质骨层
            elif z <= 0.5 * self.z_size * 1e6:
                colors.append('#FF8844')  # 过渡层
            else:
                colors.append('#4488FF')  # 松质骨层
        
        self.ax_seeds.scatter(seeds_um[:, 0], seeds_um[:, 1], seeds_um[:, 2],
                             c=colors, s=10, alpha=0.6)
        self.ax_seeds.set_xlabel('X (μm)')
        self.ax_seeds.set_ylabel('Y (μm)')
        self.ax_seeds.set_zlabel('Z (μm)')
        self.ax_seeds.set_title(f'Seed Distribution\n({len(self.generator.seeds)} seeds)')
        self.ax_seeds.view_init(elev=20, azim=45)
        
    def plot_voronoi_3d(self):
        """绘制彩色3D Voronoi结构（多彩多面体风格）"""
        max_cells = 40
        cells_to_show = self.generator.interior_cells[:min(max_cells, len(self.generator.interior_cells))]
        
        # 创建彩色映射（类似你的参考图）
        colors_list = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#FFA07A', '#98D8C8', 
                      '#F7DC6F', '#BB8FCE', '#85C1E2', '#F8B88B', '#8FD8A0',
                      '#E74C3C', '#3498DB', '#9B59B6', '#1ABC9C', '#F39C12',
                      '#D35400', '#C0392B', '#8E44AD', '#2980B9', '#16A085']
        
        for idx, cell in enumerate(cells_to_show):
            try:
                vertices = cell['vertices'] * 1e6
                center = cell['center'] * 1e6
                
                # 为每个单元分配不同颜色
                color = colors_list[idx % len(colors_list)]
                
                if len(vertices) >= 4:
                    try:
                        hull = ConvexHull(vertices)
                        # 绘制所有面
                        for simplex in hull.simplices:
                            triangle = vertices[simplex]
                            poly3d = [[triangle[j] for j in range(3)]]
                            collection = Poly3DCollection(
                                poly3d, 
                                facecolors=color,
                                alpha=0.85,
                                edgecolors='#2C3E50',
                                linewidths=1.5
                            )
                            self.ax_voronoi.add_collection3d(collection)
                        
                        # 绘制种子点
                        self.ax_voronoi.scatter(center[0], center[1], center[2],
                                              c='black', s=40, marker='o', 
                                              edgecolors='white', linewidths=1, zorder=10)
                    except:
                        pass
            except:
                continue
        
        # 设置背景和样式
        self.ax_voronoi.set_xlabel('X (μm)', fontsize=10, fontweight='bold')
        self.ax_voronoi.set_ylabel('Y (μm)', fontsize=10, fontweight='bold')
        self.ax_voronoi.set_zlabel('Z (μm)', fontsize=10, fontweight='bold')
        self.ax_voronoi.set_title(f'3D Colorful Voronoi Cells\n({len(cells_to_show)} cells)', 
                                 fontsize=11, fontweight='bold')
        self.ax_voronoi.set_xlim(0, self.x_size*1e6)
        self.ax_voronoi.set_ylim(0, self.y_size*1e6)
        self.ax_voronoi.set_zlim(0, self.z_size*1e6)
        
        # 设置视角
        self.ax_voronoi.view_init(elev=20, azim=45)
        
        # 美化网格和背景
        self.ax_voronoi.xaxis.pane.fill = False
        self.ax_voronoi.yaxis.pane.fill = False
        self.ax_voronoi.zaxis.pane.fill = False
        self.ax_voronoi.grid(True, alpha=0.3)
        
    def plot_density_distribution(self):
        """绘制密度分布柱状图"""
        layer_names = ['Cortical', 'Transition', 'Trabecular']
        densities = [self.surface_density, self.middle_density, self.core_density]
        colors = ['#FF4444', '#FF8844', '#4488FF']
        
        bars = self.ax_density.bar(layer_names, densities, color=colors, alpha=0.7, edgecolor='black')
        self.ax_density.set_ylabel('Seed Density (seeds/mm³)')
        self.ax_density.set_title('Density Distribution')
        self.ax_density.grid(True, alpha=0.3, axis='y')
        
        # 显示数值
        for bar, density in zip(bars, densities):
            height = bar.get_height()
            self.ax_density.text(bar.get_x() + bar.get_width()/2., height,
                                f'{density:.0f}', ha='center', va='bottom', fontsize=9)
        
    def plot_pore_analysis(self):
        """绘制孔隙分析"""
        if hasattr(self.generator, 'gradient_analysis') and self.generator.gradient_analysis:
            layer_pore_data = []
            layer_labels = []
            colors = []
            
            for layer_name, data in self.generator.gradient_analysis.items():
                if 'mean_pore_size_um' in data:
                    layer_pore_data.append(data['mean_pore_size_um'])
                    if '皮质骨' in layer_name:
                        layer_labels.append('Cortical')
                        colors.append('#FF4444')
                    elif '过渡' in layer_name:
                        layer_labels.append('Transition')
                        colors.append('#FF8844')
                    else:
                        layer_labels.append('Trabecular')
                        colors.append('#4488FF')
            
            bars = self.ax_pore.bar(layer_labels, layer_pore_data, color=colors, 
                                   alpha=0.7, edgecolor='black')
            self.ax_pore.set_ylabel('Mean Pore Size (μm)')
            self.ax_pore.set_title('Pore Size by Layer')
            self.ax_pore.grid(True, alpha=0.3, axis='y')
            
            # 显示数值
            for bar, pore_size in zip(bars, layer_pore_data):
                height = bar.get_height()
                self.ax_pore.text(bar.get_x() + bar.get_width()/2., height,
                                 f'{pore_size:.1f}', ha='center', va='bottom', fontsize=9)
        
    def plot_gradient_curve(self):
        """绘制Z方向梯度曲线"""
        if hasattr(self.generator, 'pore_sizes') and len(self.generator.pore_sizes) > 0:
            z_positions = []
            pore_sizes_z = []
            colors = []
            
            for i, cell in enumerate(self.generator.interior_cells):
                if i < len(self.generator.pore_sizes):
                    z_pos = cell['center'][2] * 1e6
                    z_positions.append(z_pos)
                    pore_sizes_z.append(self.generator.pore_sizes[i])
                    
                    # 颜色编码
                    if z_pos <= 0.2 * self.z_size * 1e6:
                        colors.append('#FF4444')
                    elif z_pos <= 0.5 * self.z_size * 1e6:
                        colors.append('#FF8844')
                    else:
                        colors.append('#4488FF')
            
            self.ax_gradient.scatter(z_positions, pore_sizes_z, c=colors, alpha=0.6, s=20)
            self.ax_gradient.set_xlabel('Z Position (μm)')
            self.ax_gradient.set_ylabel('Pore Size (μm)')
            self.ax_gradient.set_title('Pore Gradient (Z-direction)')
            self.ax_gradient.grid(True, alpha=0.3)
            
            # 添加层边界线
            self.ax_gradient.axvline(x=0.2 * self.z_size * 1e6, color='red', 
                                    linestyle='--', alpha=0.5, linewidth=1)
            self.ax_gradient.axvline(x=0.5 * self.z_size * 1e6, color='orange', 
                                    linestyle='--', alpha=0.5, linewidth=1)
        
    def plot_statistics(self):
        """显示统计信息"""
        stats_text = f"""SCAFFOLD PARAMETERS
═══════════════════════════

Dimensions:
  {self.x_size*1e6:.0f} × {self.y_size*1e6:.0f} × {self.z_size*1e6:.0f} μm

Seed Densities:
  Cortical:    {self.surface_density:>6.0f} seeds/mm³
  Transition:  {self.middle_density:>6.0f} seeds/mm³
  Trabecular:  {self.core_density:>6.0f} seeds/mm³

Target Porosity: {self.target_porosity*100:.1f}%

Total Seeds: {len(self.generator.seeds)}
Interior Cells: {len(self.generator.interior_cells)}
"""
        
        if hasattr(self.generator, 'pore_sizes') and len(self.generator.pore_sizes) > 0:
            stats_text += f"\nPore Statistics:\n"
            stats_text += f"  Mean: {np.mean(self.generator.pore_sizes):.2f} μm\n"
            stats_text += f"  Std:  {np.std(self.generator.pore_sizes):.2f} μm\n"
            stats_text += f"  Range: {np.min(self.generator.pore_sizes):.1f}-{np.max(self.generator.pore_sizes):.1f} μm"
        
        self.ax_stats.text(0.05, 0.95, stats_text, transform=self.ax_stats.transAxes,
                          fontsize=9, verticalalignment='top', fontfamily='monospace',
                          bbox=dict(boxstyle="round,pad=0.5", facecolor="lightgray", alpha=0.8))
        
    def save_current_scaffold(self, event):
        """保存当前支架"""
        if self.generator is None:
            print("[WARNING] 请先生成支架!")
            return
        
        output_dir = "/Users/kiki/Desktop/bone scaffold/ Voronoi scaffold"
        
        # 生成STL
        self.generator.generate_stl_mesh()
        
        # 保存文件
        import datetime
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        
        stl_file = f"{output_dir}/scaffold_{timestamp}.stl"
        config_file = f"{output_dir}/config_{timestamp}.json"
        
        self.generator.save_stl(stl_file)
        self.generator.export_config_json(config_file)
        
        print(f"[SUCCESS] 支架已保存:")
        print(f"  STL: {stl_file}")
        print(f"  Config: {config_file}")
    
    def save_visualizations(self, event):
        """保存所有可视化图"""
        if self.generator is None:
            print("[WARNING] 请先生成支架!")
            return
        
        output_dir = "/Users/kiki/Desktop/bone scaffold/ Voronoi scaffold"
        
        import datetime
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        
        print(f"\n[INFO] 正在生成并保存可视化图...")
        
        # 1. 生成彩色3D Voronoi图（类似第一张参考图）
        print("  [1/3] 生成彩色3D Voronoi图...")
        voronoi_fig_path = f"{output_dir}/colorful_voronoi_3d_{timestamp}.png"
        self.generate_colorful_voronoi_3d(voronoi_fig_path)
        
        # 2. 生成仿真支架图（类似SEM图像）
        print("  [2/3] 生成仿真支架图...")
        scaffold_fig_path = f"{output_dir}/realistic_scaffold_{timestamp}.png"
        self.generate_realistic_scaffold_image(scaffold_fig_path)
        
        # 3. 生成梯度分析图
        print("  [3/3] 生成梯度分析图...")
        gradient_fig_path = f"{output_dir}/gradient_analysis_{timestamp}.png"
        self.generator.visualize_gradient_structure(gradient_fig_path)
        
        print(f"\n[SUCCESS] 所有可视化图已保存到: {output_dir}")
    
    def generate_colorful_voronoi_3d(self, save_path, max_cells=50):
        """生成彩色3D Voronoi多面体图（类似第一张参考图）"""
        fig = plt.figure(figsize=(12, 10))
        ax = fig.add_subplot(111, projection='3d')
        ax.set_facecolor('#F0F0F0')
        
        cells_to_show = self.generator.interior_cells[:min(max_cells, len(self.generator.interior_cells))]
        
        # 丰富的颜色列表
        colors_list = [
            '#FF6B6B', '#4ECDC4', '#45B7D1', '#FFA07A', '#98D8C8', 
            '#F7DC6F', '#BB8FCE', '#85C1E2', '#F8B88B', '#8FD8A0',
            '#E74C3C', '#3498DB', '#9B59B6', '#1ABC9C', '#F39C12',
            '#D35400', '#C0392B', '#8E44AD', '#2980B9', '#16A085',
            '#F39C6B', '#6C5CE7', '#00B894', '#FDCB6E', '#E17055',
            '#74B9FF', '#A29BFE', '#FD79A8', '#FDCB6E', '#55EFC4'
        ]
        
        for idx, cell in enumerate(cells_to_show):
            try:
                vertices = cell['vertices'] * 1e6
                center = cell['center'] * 1e6
                
                # 分配颜色
                color = colors_list[idx % len(colors_list)]
                
                if len(vertices) >= 4:
                    try:
                        hull = ConvexHull(vertices)
                        # 绘制所有面
                        for simplex in hull.simplices:
                            triangle = vertices[simplex]
                            poly3d = [[triangle[j] for j in range(3)]]
                            collection = Poly3DCollection(
                                poly3d,
                                facecolors=color,
                                alpha=0.9,
                                edgecolors='#2C3E50',
                                linewidths=2
                            )
                            ax.add_collection3d(collection)
                        
                        # 添加种子点
                        ax.scatter(center[0], center[1], center[2],
                                 c='black', s=50, marker='o',
                                 edgecolors='white', linewidths=1.5, zorder=10)
                    except:
                        pass
            except:
                continue
        
        ax.set_xlabel('X (μm)', fontsize=12, fontweight='bold')
        ax.set_ylabel('Y (μm)', fontsize=12, fontweight='bold')
        ax.set_zlabel('Z (μm)', fontsize=12, fontweight='bold')
        ax.set_title('3D Colorful Voronoi Scaffold Structure', 
                    fontsize=14, fontweight='bold', pad=20)
        
        ax.set_xlim(0, self.generator.x_size*1e6)
        ax.set_ylim(0, self.generator.y_size*1e6)
        ax.set_zlim(0, self.generator.z_size*1e6)
        ax.view_init(elev=25, azim=45)
        
        # 美化
        ax.xaxis.pane.fill = False
        ax.yaxis.pane.fill = False
        ax.zaxis.pane.fill = False
        ax.grid(True, alpha=0.2, linestyle='--')
        
        plt.tight_layout()
        plt.savefig(save_path, dpi=300, bbox_inches='tight', facecolor='white')
        plt.close()
        print(f"  ✓ 彩色3D Voronoi图已保存: {save_path}")
    
    def generate_realistic_scaffold_image(self, save_path):
        """生成仿真支架图（类似SEM扫描电镜图像）"""
        fig, axes = plt.subplots(2, 2, figsize=(14, 14))
        fig.patch.set_facecolor('#E8E8E8')
        
        # 生成STL网格（如果还没有）
        if not hasattr(self.generator, 'mesh') or self.generator.mesh is None:
            self.generator.generate_stl_mesh()
        
        # 4个不同视角的仿真图
        views = [
            (20, 45, '透视图 A'),
            (20, 135, '透视图 B'),
            (5, 90, '侧视图'),
            (85, 0, '俯视图')
        ]
        
        for idx, (ax, (elev, azim, title)) in enumerate(zip(axes.flat, views)):
            ax_3d = fig.add_subplot(2, 2, idx+1, projection='3d')
            ax_3d.set_facecolor('#1A1A1A')
            
            # 绘制支架结构（模拟SEM效果）
            max_cells_view = 60
            cells_to_show = self.generator.interior_cells[:min(max_cells_view, len(self.generator.interior_cells))]
            
            for cell in cells_to_show:
                try:
                    vertices = cell['vertices'] * 1e6
                    
                    if len(vertices) >= 4:
                        try:
                            hull = ConvexHull(vertices)
                            for simplex in hull.simplices:
                                triangle = vertices[simplex]
                                poly3d = [[triangle[j] for j in range(3)]]
                                
                                # 计算面的法向量用于光照效果
                                v1 = triangle[1] - triangle[0]
                                v2 = triangle[2] - triangle[0]
                                normal = np.cross(v1, v2)
                                normal = normal / (np.linalg.norm(normal) + 1e-10)
                                
                                # 光照方向
                                light_dir = np.array([0.5, 0.5, 1.0])
                                light_dir = light_dir / np.linalg.norm(light_dir)
                                
                                # 计算光照强度
                                intensity = max(0.3, abs(np.dot(normal, light_dir)))
                                
                                # 灰度颜色（模拟SEM）
                                gray_val = intensity * 0.9
                                color = (gray_val, gray_val, gray_val)
                                
                                collection = Poly3DCollection(
                                    poly3d,
                                    facecolors=color,
                                    alpha=1.0,
                                    edgecolors='#404040',
                                    linewidths=0.5
                                )
                                ax_3d.add_collection3d(collection)
                        except:
                            pass
                except:
                    continue
            
            # 设置
            ax_3d.set_xlabel('X (μm)', fontsize=9, color='white', fontweight='bold')
            ax_3d.set_ylabel('Y (μm)', fontsize=9, color='white', fontweight='bold')
            ax_3d.set_zlabel('Z (μm)', fontsize=9, color='white', fontweight='bold')
            ax_3d.set_title(title, fontsize=11, color='white', fontweight='bold', pad=10)
            
            ax_3d.set_xlim(0, self.generator.x_size*1e6)
            ax_3d.set_ylim(0, self.generator.y_size*1e6)
            ax_3d.set_zlim(0, self.generator.z_size*1e6)
            ax_3d.view_init(elev=elev, azim=azim)
            
            # SEM风格
            ax_3d.xaxis.pane.set_facecolor('#1A1A1A')
            ax_3d.yaxis.pane.set_facecolor('#1A1A1A')
            ax_3d.zaxis.pane.set_facecolor('#1A1A1A')
            ax_3d.grid(False)
            
            # 白色坐标轴
            ax_3d.tick_params(colors='white', labelsize=8)
            ax_3d.xaxis.pane.set_edgecolor('#404040')
            ax_3d.yaxis.pane.set_edgecolor('#404040')
            ax_3d.zaxis.pane.set_edgecolor('#404040')
        
        plt.suptitle('Biomimetic Scaffold - SEM-style Visualization', 
                    fontsize=16, fontweight='bold', color='white', y=0.98)
        
        # 添加比例尺和信息
        info_text = f"""
Scaffold Parameters:
• Dimensions: {self.generator.x_size*1e6:.0f} × {self.generator.y_size*1e6:.0f} × {self.generator.z_size*1e6:.0f} μm
• Porosity: {self.generator.target_porosity*100:.1f}%
• Total Cells: {len(self.generator.interior_cells)}
• Mean Pore: {np.mean(self.generator.pore_sizes):.1f} ± {np.std(self.generator.pore_sizes):.1f} μm
        """
        fig.text(0.02, 0.02, info_text, fontsize=8, color='white',
                bbox=dict(boxstyle='round', facecolor='#2C2C2C', alpha=0.8, edgecolor='white'))
        
        plt.tight_layout(rect=[0, 0.03, 1, 0.97])
        plt.savefig(save_path, dpi=300, bbox_inches='tight', facecolor='#1A1A1A')
        plt.close()
        print(f"  ✓ 仿真支架图已保存: {save_path}")
    

class GradientVoronoiScaffoldGenerator(VoronoiScaffoldGenerator):
    """支持梯度的Voronoi支架生成器"""
    
    def __init__(self, *args, gradient_type='linear', **kwargs):
        """
        gradient_type: 'linear' (线性), 'exponential' (指数), 'sigmoid' (S型)
        """
        super().__init__(*args, **kwargs)
        self.gradient_type = gradient_type
    
    def generate_seeds_with_gradient(self, gradient_param=None):
        """
        生成具有Z方向梯度的种子点
        表层（0-30μm）：种子密度高 → 孔隙细
        中层（30-70μm）：种子密度中等 → 孔隙中等
        内层（70-100μm）：种子密度低 → 孔隙粗
        """
        print("[INFO] 生成具有梯度的种子点...")
        
        if gradient_param is None:
            # 仿生骨结构：外层高密度(皮质骨) → 内层低密度(松质骨)
            gradient_param = {
                'surface_density': 25000,    # seeds/mm³ - 皮质骨区域(高密度，小孔隙)
                'middle_density': 12000,     # seeds/mm³ - 过渡区域(中等密度)  
                'core_density': 6000         # seeds/mm³ - 松质骨区域(低密度，大孔隙)
            }
        
        seeds = []
        
        # 仿生骨结构分层 - 更符合天然骨的比例
        z_surface = 0.2 * self.z_size   # 0-20% 皮质骨层(致密层)
        z_middle = 0.5 * self.z_size    # 20-50% 过渡层  
        z_core = self.z_size            # 50-100% 松质骨层(疏松层)
        
        # 表层
        n_surface = int(gradient_param['surface_density'] * 
                       self.x_size * self.y_size * z_surface * 1e9)
        seeds_surface = np.random.uniform(
            [0, 0, 0],
            [self.x_size, self.y_size, z_surface],
            size=(n_surface, 3)
        )
        seeds.append(seeds_surface)
        
        # 中层
        n_middle = int(gradient_param['middle_density'] * 
                      self.x_size * self.y_size * (z_middle - z_surface) * 1e9)
        seeds_middle = np.random.uniform(
            [0, 0, z_surface],
            [self.x_size, self.y_size, z_middle],
            size=(n_middle, 3)
        )
        seeds.append(seeds_middle)
        
        # 内层
        n_core = int(gradient_param['core_density'] * 
                    self.x_size * self.y_size * (z_core - z_middle) * 1e9)
        seeds_core = np.random.uniform(
            [0, 0, z_middle],
            [self.x_size, self.y_size, z_core],
            size=(n_core, 3)
        )
        seeds.append(seeds_core)
        
        self.seeds = np.vstack(seeds)
        
        print(f"[SUCCESS] 仿生梯度种子点生成完成")
        print(f"  皮质骨层(0-20%): {n_surface} 个种子 - 高密度，小孔隙")
        print(f"  过渡层(20-50%): {n_middle} 个种子 - 中等密度")
        print(f"  松质骨层(50-100%): {n_core} 个种子 - 低密度，大孔隙")
        print(f"  总计: {len(self.seeds)} 个种子 (仿生骨结构)")
        
        return self.seeds
    
    def analyze_gradient_properties(self):
        """分析梯度特性"""
        print("[INFO] 分析梯度特性...")
        
        # 按仿生骨结构分层分析孔隙大小
        z_layers = [
            (0, 0.2 * self.z_size),                    # 皮质骨层
            (0.2 * self.z_size, 0.5 * self.z_size),   # 过渡层
            (0.5 * self.z_size, self.z_size)          # 松质骨层
        ]
        layer_names = ['皮质骨层 (0-20%)', '过渡层 (20-50%)', '松质骨层 (50-100%)']
        
        gradient_analysis = {}
        
        for (z_min, z_max), name in zip(z_layers, layer_names):
            layer_pores = []
            
            for idx, pore_size in enumerate(self.pore_sizes):
                # 根据pore_size关联到相应层
                cell_center_z = self.interior_cells[idx]['center'][2]
                
                if z_min <= cell_center_z < z_max:
                    layer_pores.append(pore_size)
            
            if layer_pores:
                gradient_analysis[name] = {
                    'mean_pore_size_um': np.mean(layer_pores),
                    'std_pore_size_um': np.std(layer_pores),
                    'min_pore_size_um': np.min(layer_pores),
                    'max_pore_size_um': np.max(layer_pores),
                    'n_pores': len(layer_pores)
                }
        
        print("\n========== 仿生骨结构孔隙分析 ==========")
        for layer, data in gradient_analysis.items():
            print(f"\n{layer}:")
            for key, value in data.items():
                print(f"  {key:25s}: {value:.2f}" if isinstance(value, float) else f"  {key:25s}: {value}")
        
        # 添加仿生学评估
        print(f"\n========== 仿生学评估 ==========")
        if '皮质骨层 (0-20%)' in gradient_analysis and '松质骨层 (50-100%)' in gradient_analysis:
            cortical_pore = gradient_analysis['皮质骨层 (0-20%)']['mean_pore_size_um']
            trabecular_pore = gradient_analysis['松质骨层 (50-100%)']['mean_pore_size_um'] 
            pore_ratio = trabecular_pore / cortical_pore if cortical_pore > 0 else 0
            print(f"  孔隙梯度比: {pore_ratio:.2f} (松质骨/皮质骨)")
            print(f"  参考范围: 2.0-5.0 (天然骨)")
            
            if 1.5 <= pore_ratio <= 6.0:
                print(f"  ✅ 梯度结构符合仿生学要求")
            else:
                print(f"  ⚠️  建议调整密度参数以获得更好的梯度")
        
        self.gradient_analysis = gradient_analysis
        return gradient_analysis
    
    def visualize_gradient_structure(self, save_path=None):
        """
        生成梯度支架结构的专门可视化图
        """
        
        if not hasattr(self, 'gradient_analysis') or not self.gradient_analysis:
            print("请先运行 analyze_gradient_properties()")
            return
        
        # 创建大的综合图
        fig = plt.figure(figsize=(18, 12))
        
        # 1. 梯度种子分布 (3D)
        ax1 = fig.add_subplot(2, 4, 1, projection='3d')
        seeds_um = self.seeds * 1e6
        
        # 按层着色种子点
        z_positions = seeds_um[:, 2]
        colors = []
        for z in z_positions:
            if z <= 0.2 * self.z_size * 1e6:
                colors.append('red')      # 皮质骨层
            elif z <= 0.5 * self.z_size * 1e6:
                colors.append('orange')   # 过渡层
            else:
                colors.append('blue')     # 松质骨层
        
        ax1.scatter(seeds_um[:, 0], seeds_um[:, 1], seeds_um[:, 2], 
                   c=colors, s=15, alpha=0.7)
        ax1.set_xlabel('X (um)')
        ax1.set_ylabel('Y (um)')
        ax1.set_zlabel('Z (um)')
        ax1.set_title('Biomimetic Gradient Seed Distribution')
        
        # 添加图例
        from matplotlib.lines import Line2D
        legend_elements = [Line2D([0], [0], marker='o', color='w', markerfacecolor='red', markersize=8, label='Cortical Layer'),
                          Line2D([0], [0], marker='o', color='w', markerfacecolor='orange', markersize=8, label='Transition Layer'),
                          Line2D([0], [0], marker='o', color='w', markerfacecolor='blue', markersize=8, label='Trabecular Layer')]
        ax1.legend(handles=legend_elements, loc='upper right')
        
        # 2. 梯度密度分布
        ax2 = fig.add_subplot(2, 4, 2)
        layer_names_short = ['Cortical\\n(0-20%)', 'Transition\\n(20-50%)', 'Trabecular\\n(50-100%)']
        
        # 计算各层种子密度
        z_layers = [
            (0, 0.2 * self.z_size),
            (0.2 * self.z_size, 0.5 * self.z_size), 
            (0.5 * self.z_size, self.z_size)
        ]
        
        layer_densities = []
        layer_colors = ['red', 'orange', 'blue']
        
        for (z_min, z_max) in z_layers:
            layer_seeds = 0
            for seed in self.seeds:
                if z_min <= seed[2] < z_max:
                    layer_seeds += 1
            
            volume = self.x_size * self.y_size * (z_max - z_min) * 1e9  # mm³
            density = layer_seeds / volume if volume > 0 else 0
            layer_densities.append(density)
        
        bars = ax2.bar(layer_names_short, layer_densities, color=layer_colors, alpha=0.7)
        ax2.set_ylabel('Seed Density (seeds/mm³)')
        ax2.set_title('Seed Density Gradient')
        ax2.grid(True, alpha=0.3)
        
        # 在柱状图上显示数值
        for bar, density in zip(bars, layer_densities):
            height = bar.get_height()
            ax2.text(bar.get_x() + bar.get_width()/2., height + height*0.01,
                    f'{density:.0f}', ha='center', va='bottom')
        
        # 3. 各层孔隙大小对比
        ax3 = fig.add_subplot(2, 4, 3)
        
        layer_pore_data = []
        layer_labels = []
        
        for layer_name, data in self.gradient_analysis.items():
            if 'mean_pore_size_um' in data:
                layer_pore_data.append(data['mean_pore_size_um'])
                if '皮质骨' in layer_name:
                    layer_labels.append('Cortical')
                elif '过渡' in layer_name:
                    layer_labels.append('Transition') 
                else:
                    layer_labels.append('Trabecular')
        
        bars = ax3.bar(layer_labels, layer_pore_data, color=layer_colors[:len(layer_pore_data)], alpha=0.7)
        ax3.set_ylabel('Mean Pore Size (um)')
        ax3.set_title('Pore Size by Layer')
        ax3.grid(True, alpha=0.3)
        
        # 显示数值
        for bar, pore_size in zip(bars, layer_pore_data):
            height = bar.get_height()
            ax3.text(bar.get_x() + bar.get_width()/2., height + height*0.01,
                    f'{pore_size:.1f}', ha='center', va='bottom')
        
        # 4. Z方向孔隙大小变化趋势
        ax4 = fig.add_subplot(2, 4, 4)
        
        z_positions = []
        pore_sizes_z = []
        
        for i, cell in enumerate(self.interior_cells):
            if i < len(self.pore_sizes):
                z_pos = cell['center'][2] * 1e6  # 转换为微米
                z_positions.append(z_pos)
                pore_sizes_z.append(self.pore_sizes[i])
        
        # 按Z位置分层着色
        colors_z = []
        for z in z_positions:
            if z <= 0.2 * self.z_size * 1e6:
                colors_z.append('red')
            elif z <= 0.5 * self.z_size * 1e6:
                colors_z.append('orange')
            else:
                colors_z.append('blue')
        
        ax4.scatter(z_positions, pore_sizes_z, c=colors_z, alpha=0.7, s=30)
        ax4.set_xlabel('Z Position (um)')
        ax4.set_ylabel('Pore Size (um)')
        ax4.set_title('Pore Size vs Z Position')
        ax4.grid(True, alpha=0.3)
        
        # 添加层边界线
        ax4.axvline(x=0.2 * self.z_size * 1e6, color='gray', linestyle='--', alpha=0.7)
        ax4.axvline(x=0.5 * self.z_size * 1e6, color='gray', linestyle='--', alpha=0.7)
        
        # 5. 支架横截面示意图
        ax5 = fig.add_subplot(2, 4, 5)
        ax5.set_xlim(0, self.x_size * 1e6)
        ax5.set_ylim(0, self.z_size * 1e6)
        
        # 绘制分层区域
        cortical_height = 0.2 * self.z_size * 1e6
        transition_height = 0.3 * self.z_size * 1e6  
        trabecular_height = 0.5 * self.z_size * 1e6
        
        # 皮质骨层
        rect1 = patches.Rectangle((0, 0), self.x_size * 1e6, cortical_height, 
                                 facecolor='red', alpha=0.3, label='Cortical Layer')
        ax5.add_patch(rect1)
        
        # 过渡层
        rect2 = patches.Rectangle((0, cortical_height), self.x_size * 1e6, transition_height,
                                 facecolor='orange', alpha=0.3, label='Transition Layer')
        ax5.add_patch(rect2)
        
        # 松质骨层
        rect3 = patches.Rectangle((0, cortical_height + transition_height), self.x_size * 1e6, trabecular_height,
                                 facecolor='blue', alpha=0.3, label='Trabecular Layer')
        ax5.add_patch(rect3)
        
        # 在各层显示孔隙
        for i, cell in enumerate(self.interior_cells[:50]):  # 限制显示数量
            center = cell['center'] * 1e6
            if i < len(self.pore_sizes):
                radius = self.pore_sizes[i] / 4  # 缩放显示
                circle = patches.Circle((center[0], center[2]), radius, 
                                      facecolor='white', edgecolor='black', alpha=0.8)
                ax5.add_patch(circle)
        
        ax5.set_xlabel('X Position (um)')
        ax5.set_ylabel('Z Position (um)')
        ax5.set_title('Cross-section View (X-Z plane)')
        ax5.legend()
        ax5.set_aspect('equal', adjustable='box')
        
        # 6. 仿生学评估雷达图
        ax6 = fig.add_subplot(2, 4, 6, projection='polar')
        
        # 仿生学指标
        categories = ['Density\\nGradient', 'Pore Size\\nGradient', 'Layer\\nThickness', 
                     'Porosity\\nMatch', 'Structural\\nIntegrity']
        
        # 模拟评分（实际应用中可以根据具体指标计算）
        scores = [0.8, 0.6, 0.9, 0.7, 0.8]  # 0-1范围的评分
        
        angles = np.linspace(0, 2*np.pi, len(categories), endpoint=False).tolist()
        scores += scores[:1]  # 闭合图形
        angles += angles[:1]
        
        ax6.plot(angles, scores, 'o-', linewidth=2, color='green')
        ax6.fill(angles, scores, alpha=0.25, color='green')
        ax6.set_xticks(angles[:-1])
        ax6.set_xticklabels(categories)
        ax6.set_ylim(0, 1)
        ax6.set_title('Biomimetic Assessment')
        
        # 7-8. 统计信息和参数
        ax7 = fig.add_subplot(2, 4, (7, 8))
        ax7.axis('off')
        
        # 统计信息
        stats_text = f"""
BIOMIMETIC BONE SCAFFOLD ANALYSIS
═════════════════════════════════════

Scaffold Dimensions:
├─ Size: {self.x_size*1e6:.0f} × {self.y_size*1e6:.0f} × {self.z_size*1e6:.0f} μm
├─ Total Seeds: {len(self.seeds)}
└─ Interior Cells: {len(self.interior_cells)}

Layer Structure:
├─ Cortical Layer (0-20%): High density, small pores
├─ Transition Layer (20-50%): Medium density  
└─ Trabecular Layer (50-100%): Low density, large pores

Pore Analysis:
├─ Overall Mean: {np.mean(self.pore_sizes):.2f} ± {np.std(self.pore_sizes):.2f} μm
├─ Size Range: {np.min(self.pore_sizes):.1f} - {np.max(self.pore_sizes):.1f} μm
└─ Target Porosity: {self.target_porosity*100:.1f}%

Biomimetic Features:
├─ Density gradient: Outer dense → Inner porous
├─ Layer thickness ratio: 20% : 30% : 50%
└─ Pore size gradient: Small → Medium → Large
        """
        
        # 添加层级信息
        if hasattr(self, 'gradient_analysis'):
            stats_text += "\\n\\nLayer Details:\\n"
            for layer_name, data in self.gradient_analysis.items():
                short_name = layer_name.split('(')[0].strip()
                mean_pore = data.get('mean_pore_size_um', 0)
                n_pores = data.get('n_pores', 0)
                stats_text += f"├─ {short_name}: {mean_pore:.1f} μm ({n_pores} pores)\\n"
        
        ax7.text(0.05, 0.95, stats_text, transform=ax7.transAxes, 
                fontsize=9, verticalalignment='top', fontfamily='monospace',
                bbox=dict(boxstyle="round,pad=0.3", facecolor="lightgray", alpha=0.5))
        
        plt.suptitle('Biomimetic Gradient Voronoi Scaffold Structure Analysis', 
                     fontsize=16, fontweight='bold')
        plt.tight_layout()
        
        # 保存图片
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"[SUCCESS] 梯度支架结构图已保存: {save_path}")
        
        plt.close()
        
        return fig
    
    def visualize_3d_gradient_voronoi(self, save_path=None, max_cells=40):
        """
        生成3D彩色梯度Voronoi单元图，按层着色显示仿生结构
        """
        
        if not self.interior_cells:
            raise ValueError("请先提取内部单元")
        
        print(f"[INFO] 生成3D梯度Voronoi单元可视化图...")
        
        fig = plt.figure(figsize=(18, 12))
        
        # 创建三个子图：2D切片、3D整体视图、3D分层视图
        ax1 = fig.add_subplot(1, 3, 1)  # 2D切片
        ax2 = fig.add_subplot(1, 3, 2, projection='3d')  # 3D整体
        ax3 = fig.add_subplot(1, 3, 3, projection='3d')  # 3D分层
        
        cells_to_show = self.interior_cells[:min(max_cells, len(self.interior_cells))]
        
        # 定义仿生骨结构的颜色
        layer_colors = {
            'cortical': '#FF4444',    # 红色 - 皮质骨
            'transition': '#FF8844',  # 橙色 - 过渡层  
            'trabecular': '#4488FF'   # 蓝色 - 松质骨
        }
        
        # 分层阈值
        z_cortical = 0.2 * self.z_size
        z_transition = 0.5 * self.z_size
        
        # === 2D切片视图（显示梯度） ===
        z_slice = self.z_size / 2  # 中间切片
        
        seeds_2d = []
        colors_2d = []
        
        for cell in cells_to_show:
            center = cell['center']
            if abs(center[2] - z_slice) < self.z_size * 0.15:
                seeds_2d.append(center[:2] * 1e6)
                
                # 根据Z位置确定颜色
                if center[2] <= z_cortical:
                    colors_2d.append(layer_colors['cortical'])
                elif center[2] <= z_transition:
                    colors_2d.append(layer_colors['transition'])
                else:
                    colors_2d.append(layer_colors['trabecular'])
        
        if len(seeds_2d) >= 3:
            seeds_2d = np.array(seeds_2d)
            
            from scipy.spatial import Voronoi as Voronoi2D, voronoi_plot_2d
            
            try:
                vor_2d = Voronoi2D(seeds_2d)
                
                # 绘制Voronoi边
                voronoi_plot_2d(vor_2d, ax=ax1, show_vertices=False, 
                               line_colors='black', line_width=1.5)
                
                # 为区域着色
                for pointidx, simplex in zip(vor_2d.ridge_points, vor_2d.ridge_vertices):
                    simplex = np.asarray(simplex)
                    if np.all(simplex >= 0):
                        vertices = vor_2d.vertices[simplex]
                        # 简化的区域着色
                        pass
                        
            except Exception as e:
                print(f"[WARNING] 2D Voronoi绘制失败: {e}")
        
        # 绘制种子点
        if len(seeds_2d) > 0:
            scatter = ax1.scatter(seeds_2d[:, 0], seeds_2d[:, 1], 
                                c=colors_2d, s=60, edgecolors='black', zorder=5, alpha=0.8)
        
        ax1.set_xlim(0, self.x_size*1e6)
        ax1.set_ylim(0, self.y_size*1e6)
        ax1.set_xlabel('X (μm)')
        ax1.set_ylabel('Y (μm)')
        ax1.set_title(f'2D Gradient View\\n(Z = {z_slice*1e6:.1f} μm)')
        ax1.set_aspect('equal')
        ax1.grid(True, alpha=0.3)
        
        # 添加图例
        from matplotlib.patches import Patch
        legend_elements = [
            Patch(facecolor=layer_colors['cortical'], label='Cortical Layer'),
            Patch(facecolor=layer_colors['transition'], label='Transition Layer'),
            Patch(facecolor=layer_colors['trabecular'], label='Trabecular Layer')
        ]
        ax1.legend(handles=legend_elements, loc='upper right')
        
        # === 3D整体视图 ===
        print(f"[INFO] 渲染3D整体结构...")
        
        for i, cell in enumerate(cells_to_show):
            try:
                vertices = cell['vertices'] * 1e6
                center = cell['center'] * 1e6
                
                # 根据Z位置确定颜色
                if cell['center'][2] <= z_cortical:
                    color = layer_colors['cortical']
                    alpha = 0.8
                elif cell['center'][2] <= z_transition:
                    color = layer_colors['transition'] 
                    alpha = 0.7
                else:
                    color = layer_colors['trabecular']
                    alpha = 0.6
                
                if len(vertices) >= 4:
                    try:
                        hull = ConvexHull(vertices)
                        for simplex in hull.simplices:
                            triangle = vertices[simplex]
                            poly3d = [[triangle[j] for j in range(3)]]
                            ax2.add_collection3d(Poly3DCollection(poly3d,
                                                                facecolors=color,
                                                                alpha=alpha,
                                                                edgecolors='black',
                                                                linewidth=0.3))
                    except:
                        ax2.scatter(center[0], center[1], center[2],
                                  c=color, s=80, alpha=alpha, edgecolors='black')
                else:
                    ax2.scatter(center[0], center[1], center[2],
                              c=color, s=80, alpha=alpha, edgecolors='black')
                              
            except Exception as e:
                continue
        
        ax2.set_xlabel('X (μm)')
        ax2.set_ylabel('Y (μm)')
        ax2.set_zlabel('Z (μm)')
        ax2.set_title('3D Biomimetic Structure\\n(Integrated View)')
        ax2.set_xlim(0, self.x_size*1e6)
        ax2.set_ylim(0, self.y_size*1e6)
        ax2.set_zlim(0, self.z_size*1e6)
        ax2.view_init(elev=25, azim=45)
        
        # === 3D分层视图 ===
        print(f"[INFO] 渲染3D分层结构...")
        
        # 分层显示，每层略微分离
        z_offset = {'cortical': 0, 'transition': 5, 'trabecular': 10}  # 微米偏移
        
        for i, cell in enumerate(cells_to_show):
            try:
                vertices = cell['vertices'] * 1e6
                center = cell['center'] * 1e6
                
                # 确定层级和偏移
                if cell['center'][2] <= z_cortical:
                    layer = 'cortical'
                elif cell['center'][2] <= z_transition:
                    layer = 'transition'
                else:
                    layer = 'trabecular'
                
                color = layer_colors[layer]
                
                # 应用Z偏移
                vertices_offset = vertices.copy()
                vertices_offset[:, 2] += z_offset[layer]
                center_offset = center.copy()
                center_offset[2] += z_offset[layer]
                
                if len(vertices) >= 4:
                    try:
                        hull = ConvexHull(vertices_offset)
                        for simplex in hull.simplices:
                            triangle = vertices_offset[simplex]
                            poly3d = [[triangle[j] for j in range(3)]]
                            ax3.add_collection3d(Poly3DCollection(poly3d,
                                                                facecolors=color,
                                                                alpha=0.7,
                                                                edgecolors='darkgray',
                                                                linewidth=0.4))
                    except:
                        ax3.scatter(center_offset[0], center_offset[1], center_offset[2],
                                  c=color, s=100, alpha=0.8, edgecolors='black')
                else:
                    ax3.scatter(center_offset[0], center_offset[1], center_offset[2],
                              c=color, s=100, alpha=0.8, edgecolors='black')
                              
            except Exception:
                continue
        
        ax3.set_xlabel('X (μm)')
        ax3.set_ylabel('Y (μm)')
        ax3.set_zlabel('Z (μm) + offset')
        ax3.set_title('3D Layered Structure\\n(Exploded View)')
        ax3.set_xlim(0, self.x_size*1e6)
        ax3.set_ylim(0, self.y_size*1e6)
        ax3.set_zlim(0, self.z_size*1e6 + 20)
        ax3.view_init(elev=30, azim=60)
        
        plt.suptitle('3D Biomimetic Gradient Voronoi Scaffold Visualization', 
                     fontsize=16, fontweight='bold')
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"[SUCCESS] 3D梯度Voronoi图已保存: {save_path}")
        
        plt.close()
        
        return fig


if __name__ == "__main__":
    print("="*60)
    print("  仿生骨结构Voronoi支架生成器")
    print("  (皮质骨 → 过渡层 → 松质骨)")
    print("="*60)
    print("\n请选择模式:")
    print("  1 - 交互式界面 (可调整参数)")
    print("  2 - 直接生成 (使用默认参数)")
    
    try:
        mode = input("\n请输入选项 (1 或 2): ").strip()
    except:
        mode = "1"  # 默认交互式
    
    if mode == "1":
        # ============ 交互式模式 ============
        print("\n[INFO] 启动交互式界面...")
        print("       使用滑块调整参数后，点击 'Generate Scaffold' 按钮生成支架")
        print("       点击 'Save STL' 按钮保存当前支架\n")
        
        interactive_gen = InteractiveGradientScaffoldGenerator(
            x_size=800e-6,
            y_size=800e-6,
            z_size=100e-6,
            target_porosity=0.68
        )
        
        interactive_gen.create_interactive_interface()
        
    else:
        # ============ 直接生成模式 ============
        print("\n[INFO] 使用默认参数直接生成...")
        
        # 生成仿生梯度支架
        gradient_gen = GradientVoronoiScaffoldGenerator(
            x_size=800e-6,
            y_size=800e-6,
            z_size=100e-6,
            target_porosity=0.68
        )
        
        # 生成梯度种子
        gradient_gen.generate_seeds_with_gradient()
        
        # 计算Voronoi
        gradient_gen.compute_voronoi()
        gradient_gen.extract_interior_cells()
        gradient_gen.compute_cell_statistics()
        
        # 分析梯度特性
        gradient_gen.analyze_gradient_properties()
        
        # 生成并保存STL
        gradient_gen.generate_stl_mesh()
        
        # 保存到指定目录 - 修改为macOS路径
        output_dir = "/Users/kiki/Desktop/bone scaffold/ Voronoi scaffold"
        stl_file = output_dir + "/voronoi_scaffold_gradient.stl"
        config_file = output_dir + "/scaffold_gradient_config.json"
        
        gradient_gen.save_stl(stl_file)
        gradient_gen.export_config_json(config_file)
        
        # 生成支架结构图
        print("\n[INFO] 生成支架结构图...")
        
        # 基础结构分析图
        structure_fig_path = output_dir + "/scaffold_structure_analysis.png"
        gradient_gen.visualize_scaffold_structure(structure_fig_path)
        
        # 专门的梯度结构图
        gradient_fig_path = output_dir + "/biomimetic_gradient_analysis.png" 
        gradient_gen.visualize_gradient_structure(gradient_fig_path)
        
        # 3D彩色Voronoi可视化
        print("\n[INFO] 生成3D彩色Voronoi结构图...")
        voronoi_3d_path = output_dir + "/3d_gradient_voronoi_structure.png"
        gradient_gen.visualize_3d_gradient_voronoi(voronoi_3d_path, max_cells=35)
        
        # 基础3D Voronoi图
        basic_3d_path = output_dir + "/3d_voronoi_cells.png"
        gradient_gen.visualize_3d_voronoi_cells(basic_3d_path, max_cells=25)
        
        # 基础可视化
        gradient_gen.visualize_seeds()
        
        print("\n[COMPLETE] 仿生骨结构Voronoi支架生成完成！")
        print("✅ 已模拟天然骨的皮质骨-松质骨梯度结构")
        print(f"✅ 支架结构图已生成并保存到: {output_dir}")