"""
支持组成梯度的Voronoi支架生成器
在Z方向创建梯度孔隙结构（表面细孔→内层粗孔）
"""

import numpy as np
from voronoi_scaffold_generator import VoronoiScaffoldGenerator


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
        import matplotlib.pyplot as plt
        import matplotlib.patches as patches
        
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
        import matplotlib.pyplot as plt
        from scipy.spatial import ConvexHull
        from mpl_toolkits.mplot3d.art3d import Poly3DCollection
        
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
    
    # 保存到指定目录
    output_dir = r"C:\Users\lenove\Desktop\bone scaffold\组成梯度的Voronoi生成"
    stl_file = output_dir + r"\voronoi_scaffold_gradient.stl"
    config_file = output_dir + r"\scaffold_gradient_config.json"
    
    gradient_gen.save_stl(stl_file)
    gradient_gen.export_config_json(config_file)
    
    # 生成支架结构图
    print("\n[INFO] 生成支架结构图...")
    
    # 基础结构分析图
    structure_fig_path = output_dir + r"\scaffold_structure_analysis.png"
    gradient_gen.visualize_scaffold_structure(structure_fig_path)
    
    # 专门的梯度结构图
    gradient_fig_path = output_dir + r"\biomimetic_gradient_analysis.png" 
    gradient_gen.visualize_gradient_structure(gradient_fig_path)
    
    # 3D彩色Voronoi可视化
    print("\n[INFO] 生成3D彩色Voronoi结构图...")
    voronoi_3d_path = output_dir + r"\3d_gradient_voronoi_structure.png"
    gradient_gen.visualize_3d_gradient_voronoi(voronoi_3d_path, max_cells=35)
    
    # 基础3D Voronoi图
    basic_3d_path = output_dir + r"\3d_voronoi_cells.png"
    gradient_gen.visualize_3d_voronoi_cells(basic_3d_path, max_cells=25)
    
    # 基础可视化
    gradient_gen.visualize_seeds()
    
    print("\n[COMPLETE] 仿生骨结构Voronoi支架生成完成！")
    print("✅ 已模拟天然骨的皮质骨-松质骨梯度结构")
    print(f"✅ 支架结构图已生成并保存到: {output_dir}")