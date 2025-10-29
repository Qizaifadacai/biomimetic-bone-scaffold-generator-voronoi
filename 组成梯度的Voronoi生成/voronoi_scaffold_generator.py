"""
Voronoi支架生成器基类
用于生成3D Voronoi多孔支架结构
"""

import numpy as np
from scipy.spatial import Voronoi
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import json


class VoronoiScaffoldGenerator:
    """Voronoi支架生成器基类"""
    
    def __init__(self, x_size=1e-3, y_size=1e-3, z_size=1e-3, 
                 target_porosity=0.7, seed_density=None):
        """
        初始化Voronoi支架生成器
        
        参数:
            x_size, y_size, z_size: 支架尺寸 (米)
            target_porosity: 目标孔隙率 (0-1)
            seed_density: 种子点密度 (seeds/mm³)，如果为None则自动计算
        """
        self.x_size = x_size
        self.y_size = y_size
        self.z_size = z_size
        self.target_porosity = target_porosity
        self.seed_density = seed_density
        
        self.seeds = None
        self.vor = None
        self.interior_cells = []
        self.pore_sizes = []
        self.mesh_vertices = None
        self.mesh_faces = None
        
        print(f"[INFO] 初始化Voronoi支架生成器")
        print(f"  尺寸: {x_size*1e6:.1f} × {y_size*1e6:.1f} × {z_size*1e6:.1f} μm")
        print(f"  目标孔隙率: {target_porosity*100:.1f}%")
    
    def generate_seeds(self, n_seeds=None):
        """
        生成随机种子点
        
        参数:
            n_seeds: 种子点数量，如果为None则根据seed_density计算
        """
        print("[INFO] 生成种子点...")
        
        if n_seeds is None:
            if self.seed_density is None:
                # 默认种子密度：10 seeds/mm³
                self.seed_density = 10
            
            volume_mm3 = self.x_size * self.y_size * self.z_size * 1e9
            n_seeds = int(self.seed_density * volume_mm3)
        
        # 生成随机种子点
        self.seeds = np.random.uniform(
            [0, 0, 0],
            [self.x_size, self.y_size, self.z_size],
            size=(n_seeds, 3)
        )
        
        print(f"[SUCCESS] 生成了 {len(self.seeds)} 个种子点")
        print(f"  种子密度: {len(self.seeds)/(self.x_size*self.y_size*self.z_size*1e9):.2f} seeds/mm3")
        
        return self.seeds
    
    def compute_voronoi(self):
        """计算Voronoi图"""
        if self.seeds is None:
            raise ValueError("请先生成种子点")
        
        print("[INFO] 计算Voronoi图...")
        self.vor = Voronoi(self.seeds)
        print(f"[SUCCESS] Voronoi计算完成")
        print(f"  顶点数: {len(self.vor.vertices)}")
        print(f"  区域数: {len(self.vor.regions)}")
        
        return self.vor
    
    def extract_interior_cells(self):
        """提取内部完整的Voronoi单元"""
        if self.vor is None:
            raise ValueError("请先计算Voronoi图")
        
        print("[INFO] 提取内部Voronoi单元...")
        self.interior_cells = []
        
        for point_idx, region_idx in enumerate(self.vor.point_region):
            region = self.vor.regions[region_idx]
            
            # 跳过无限区域（包含-1的区域）
            if -1 in region or len(region) == 0:
                continue
            
            # 获取该单元的所有顶点
            vertices = self.vor.vertices[region]
            
            # 检查所有顶点是否在边界内
            in_bounds = np.all(
                (vertices[:, 0] >= 0) & (vertices[:, 0] <= self.x_size) &
                (vertices[:, 1] >= 0) & (vertices[:, 1] <= self.y_size) &
                (vertices[:, 2] >= 0) & (vertices[:, 2] <= self.z_size)
            )
            
            if in_bounds:
                cell_center = self.seeds[point_idx]
                self.interior_cells.append({
                    'point_idx': point_idx,
                    'region_idx': region_idx,
                    'vertices': vertices,
                    'center': cell_center
                })
        
        print(f"[SUCCESS] 提取了 {len(self.interior_cells)} 个内部单元")
        return self.interior_cells
    
    def compute_cell_statistics(self):
        """计算单元统计信息（体积、孔隙大小等）"""
        if not self.interior_cells:
            raise ValueError("请先提取内部单元")
        
        print("[INFO] 计算单元统计...")
        self.pore_sizes = []
        total_volume = 0
        
        for cell in self.interior_cells:
            vertices = cell['vertices']
            
            # 简化估计：使用凸包体积
            # 更精确的方法需要实现凸包体积计算
            # 这里使用近似方法：计算到中心的平均距离
            center = cell['center']
            distances = np.linalg.norm(vertices - center, axis=1)
            avg_distance = np.mean(distances)
            
            # 估计等效球体积
            cell_volume = (4/3) * np.pi * (avg_distance ** 3)
            total_volume += cell_volume
            
            # 孔隙大小（等效直径，单位：微米）
            pore_size = 2 * avg_distance * 1e6
            self.pore_sizes.append(pore_size)
            cell['volume'] = cell_volume
            cell['pore_size'] = pore_size
        
        self.pore_sizes = np.array(self.pore_sizes)
        
        # 计算实际孔隙率
        scaffold_volume = self.x_size * self.y_size * self.z_size
        actual_porosity = total_volume / scaffold_volume
        
        print(f"[SUCCESS] 统计完成")
        print(f"  平均孔隙大小: {np.mean(self.pore_sizes):.2f} ± {np.std(self.pore_sizes):.2f} μm")
        print(f"  孔隙大小范围: {np.min(self.pore_sizes):.2f} - {np.max(self.pore_sizes):.2f} μm")
        print(f"  实际孔隙率: {actual_porosity*100:.2f}%")
        
        return {
            'mean_pore_size': np.mean(self.pore_sizes),
            'std_pore_size': np.std(self.pore_sizes),
            'min_pore_size': np.min(self.pore_sizes),
            'max_pore_size': np.max(self.pore_sizes),
            'porosity': actual_porosity
        }
    
    def generate_stl_mesh(self, wall_thickness=20e-6):
        """
        生成STL网格
        
        参数:
            wall_thickness: 墙壁厚度 (米)
        """
        print(f"[INFO] 生成STL网格 (墙厚: {wall_thickness*1e6:.1f} μm)...")
        
        vertices = []
        faces = []
        vertex_count = 0
        
        # 为每个Voronoi单元生成网格
        for cell in self.interior_cells:
            cell_vertices = cell['vertices']
            center = cell['center']
            
            # 为每个面生成三角形
            # 简化版本：创建从中心到每个顶点的四面体
            n_verts = len(cell_vertices)
            
            for i in range(n_verts):
                for j in range(i+1, n_verts):
                    for k in range(j+1, n_verts):
                        # 创建三角形面
                        v1 = cell_vertices[i]
                        v2 = cell_vertices[j]
                        v3 = cell_vertices[k]
                        
                        # 添加顶点
                        vertices.extend([v1, v2, v3])
                        
                        # 添加面（使用顶点索引）
                        faces.append([vertex_count, vertex_count+1, vertex_count+2])
                        vertex_count += 3
        
        self.mesh_vertices = np.array(vertices)
        self.mesh_faces = np.array(faces)
        
        print(f"[SUCCESS] 网格生成完成")
        print(f"  顶点数: {len(self.mesh_vertices)}")
        print(f"  面数: {len(self.mesh_faces)}")
        
        return self.mesh_vertices, self.mesh_faces
    
    def save_stl(self, filename='voronoi_scaffold.stl'):
        """保存为STL文件"""
        if self.mesh_vertices is None or self.mesh_faces is None:
            raise ValueError("请先生成网格")
        
        print(f"[INFO] 保存STL文件: {filename}")
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write('solid voronoi_scaffold\n')
            
            for face in self.mesh_faces:
                v1 = self.mesh_vertices[face[0]]
                v2 = self.mesh_vertices[face[1]]
                v3 = self.mesh_vertices[face[2]]
                
                # 计算法向量
                edge1 = v2 - v1
                edge2 = v3 - v1
                normal = np.cross(edge1, edge2)
                normal = normal / np.linalg.norm(normal)
                
                f.write(f'  facet normal {normal[0]:.6e} {normal[1]:.6e} {normal[2]:.6e}\n')
                f.write('    outer loop\n')
                f.write(f'      vertex {v1[0]:.6e} {v1[1]:.6e} {v1[2]:.6e}\n')
                f.write(f'      vertex {v2[0]:.6e} {v2[1]:.6e} {v2[2]:.6e}\n')
                f.write(f'      vertex {v3[0]:.6e} {v3[1]:.6e} {v3[2]:.6e}\n')
                f.write('    endloop\n')
                f.write('  endfacet\n')
            
            f.write('endsolid voronoi_scaffold\n')
        
        print(f"[SUCCESS] STL文件已保存: {filename}")
    
    def export_config_json(self, filename='scaffold_config.json'):
        """导出配置为JSON文件"""
        config = {
            'dimensions': {
                'x_size_um': self.x_size * 1e6,
                'y_size_um': self.y_size * 1e6,
                'z_size_um': self.z_size * 1e6
            },
            'target_porosity': self.target_porosity,
            'seed_density': self.seed_density,
            'n_seeds': len(self.seeds) if self.seeds is not None else None,
            'statistics': {
                'mean_pore_size_um': float(np.mean(self.pore_sizes)) if len(self.pore_sizes) > 0 else None,
                'std_pore_size_um': float(np.std(self.pore_sizes)) if len(self.pore_sizes) > 0 else None,
                'n_interior_cells': len(self.interior_cells)
            }
        }
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=2, ensure_ascii=False)
        
        print(f"[SUCCESS] 配置已保存: {filename}")
    
    def visualize_seeds(self):
        """可视化种子点"""
        if self.seeds is None:
            raise ValueError("请先生成种子点")
        
        fig = plt.figure(figsize=(10, 8))
        ax = fig.add_subplot(111, projection='3d')
        
        ax.scatter(self.seeds[:, 0]*1e6, self.seeds[:, 1]*1e6, self.seeds[:, 2]*1e6, 
                  c='blue', marker='o', s=20, alpha=0.6)
        
        ax.set_xlabel('X (μm)')
        ax.set_ylabel('Y (μm)')
        ax.set_zlabel('Z (μm)')
        ax.set_title(f'Voronoi种子点分布 (n={len(self.seeds)})')
        
        plt.tight_layout()
        plt.close()
    
    def visualize_voronoi_3d(self, max_cells=50):
        """
        3D可视化Voronoi结构
        
        参数:
            max_cells: 最大显示单元数（避免过于复杂）
        """
        if not self.interior_cells:
            raise ValueError("请先提取内部单元")
        
        fig = plt.figure(figsize=(12, 10))
        ax = fig.add_subplot(111, projection='3d')
        
        # 随机选择一些单元显示
        cells_to_show = self.interior_cells[:min(max_cells, len(self.interior_cells))]
        
        for cell in cells_to_show:
            vertices = cell['vertices'] * 1e6  # 转换为微米
            
            # 创建凸包的简化版本：连接所有顶点对
            # 注意：这只是可视化，不是真正的凸包
            poly = Poly3DCollection([vertices], alpha=0.1, facecolor='cyan', edgecolor='blue')
            ax.add_collection3d(poly)
        
        ax.set_xlabel('X (um)')
        ax.set_ylabel('Y (um)')
        ax.set_zlabel('Z (um)')
        ax.set_title(f'Voronoi Scaffold Structure (showing {len(cells_to_show)} cells)')
        
        # 设置坐标轴范围
        ax.set_xlim(0, self.x_size*1e6)
        ax.set_ylim(0, self.y_size*1e6)
        ax.set_zlim(0, self.z_size*1e6)
        
        plt.tight_layout()
        plt.close()
    
    def visualize_3d_voronoi_cells(self, save_path=None, max_cells=30):
        """
        生成3D彩色Voronoi单元图，类似你提供的参考图
        """
        from scipy.spatial import ConvexHull
        import matplotlib.colors as mcolors
        
        if not self.interior_cells:
            raise ValueError("请先提取内部单元")
        
        print(f"[INFO] 生成3D Voronoi单元可视化图...")
        
        fig = plt.figure(figsize=(15, 12))
        
        # 创建两个子图：2D切片和3D视图
        ax1 = fig.add_subplot(1, 2, 1)  # 2D切片视图
        ax2 = fig.add_subplot(1, 2, 2, projection='3d')  # 3D视图
        
        # 限制显示的单元数量以避免过于复杂
        cells_to_show = self.interior_cells[:min(max_cells, len(self.interior_cells))]
        
        # 生成颜色映射
        colors = plt.cm.Set3(np.linspace(0, 1, len(cells_to_show)))
        
        # === 2D切片视图 (Z=中间层) ===
        z_slice = self.z_size / 2  # 取中间层
        
        # 显示种子点
        seeds_2d = []
        colors_2d = []
        
        for i, cell in enumerate(cells_to_show):
            center = cell['center']
            if abs(center[2] - z_slice) < self.z_size * 0.1:  # 在切片附近的点
                seeds_2d.append(center[:2] * 1e6)  # 转换为微米，只取X,Y
                colors_2d.append(colors[i])
        
        if len(seeds_2d) > 0:
            seeds_2d = np.array(seeds_2d)
            
            # 计算2D Voronoi图
            from scipy.spatial import Voronoi as Voronoi2D, voronoi_plot_2d
            
            if len(seeds_2d) >= 3:  # 需要至少3个点
                vor_2d = Voronoi2D(seeds_2d)
                
                # 绘制2D Voronoi图
                voronoi_plot_2d(vor_2d, ax=ax1, show_vertices=False, line_colors='black', line_width=2)
                
                # 为每个区域着色
                for i, region in enumerate(vor_2d.regions):
                    if len(region) > 0 and -1 not in region:
                        vertices = vor_2d.vertices[region]
                        # 检查区域是否在边界内
                        if np.all(vertices >= 0) and np.all(vertices[:, 0] <= self.x_size*1e6) and np.all(vertices[:, 1] <= self.y_size*1e6):
                            color = colors[i % len(colors)]
                            ax1.fill(vertices[:, 0], vertices[:, 1], color=color, alpha=0.6, edgecolor='black')
        
        # 绘制种子点
        if len(seeds_2d) > 0:
            ax1.scatter(seeds_2d[:, 0], seeds_2d[:, 1], c=colors_2d, s=50, edgecolors='black', zorder=5)
        
        ax1.set_xlim(0, self.x_size*1e6)
        ax1.set_ylim(0, self.y_size*1e6)
        ax1.set_xlabel('X (μm)')
        ax1.set_ylabel('Y (μm)')
        ax1.set_title(f'2D Voronoi Diagram (Z = {z_slice*1e6:.1f} μm slice)')
        ax1.set_aspect('equal')
        ax1.grid(True, alpha=0.3)
        
        # === 3D视图 ===
        print(f"[INFO] 渲染3D Voronoi单元...")
        
        for i, cell in enumerate(cells_to_show):
            try:
                vertices = cell['vertices'] * 1e6  # 转换为微米
                center = cell['center'] * 1e6
                
                # 尝试构建凸包
                if len(vertices) >= 4:  # 3D凸包至少需要4个点
                    try:
                        hull = ConvexHull(vertices)
                        
                        # 绘制凸包的面
                        for simplex in hull.simplices:
                            triangle = vertices[simplex]
                            poly3d = [[triangle[j] for j in range(3)]]
                            ax2.add_collection3d(Poly3DCollection(poly3d, 
                                                                facecolors=colors[i], 
                                                                alpha=0.7,
                                                                edgecolors='black',
                                                                linewidth=0.5))
                    
                    except Exception:
                        # 如果凸包失败，使用简化显示
                        ax2.scatter(center[0], center[1], center[2], 
                                  c=[colors[i]], s=100, alpha=0.8, edgecolors='black')
                
                else:
                    # 顶点太少，只显示中心点
                    ax2.scatter(center[0], center[1], center[2], 
                              c=[colors[i]], s=100, alpha=0.8, edgecolors='black')
            
            except Exception as e:
                print(f"[WARNING] 跳过单元 {i}: {e}")
                continue
        
        # 显示种子点
        seeds_3d = np.array([cell['center'] for cell in cells_to_show]) * 1e6
        ax2.scatter(seeds_3d[:, 0], seeds_3d[:, 1], seeds_3d[:, 2], 
                   c='red', s=30, alpha=1.0, edgecolors='darkred', zorder=10, label='Seed Points')
        
        ax2.set_xlabel('X (μm)')
        ax2.set_ylabel('Y (μm)')
        ax2.set_zlabel('Z (μm)')
        ax2.set_title(f'3D Voronoi Cells (showing {len(cells_to_show)} cells)')
        ax2.legend()
        
        # 设置坐标轴范围
        ax2.set_xlim(0, self.x_size*1e6)
        ax2.set_ylim(0, self.y_size*1e6)
        ax2.set_zlim(0, self.z_size*1e6)
        
        # 设置视角
        ax2.view_init(elev=20, azim=45)
        
        plt.suptitle('3D Voronoi Scaffold Structure Visualization', fontsize=16, fontweight='bold')
        plt.tight_layout()
        
        # 保存图片
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"[SUCCESS] 3D Voronoi图已保存: {save_path}")
        
        plt.close()
        
        return fig
    
    def visualize_scaffold_structure(self, save_path=None):
        """
        生成完整的支架结构图，包括多个视角和分析
        """
        if not self.interior_cells or len(self.pore_sizes) == 0:
            raise ValueError("请先完成支架生成和统计分析")
        
        # 创建大图包含多个子图
        fig = plt.figure(figsize=(16, 12))
        
        # 1. 种子点分布图
        ax1 = fig.add_subplot(2, 3, 1, projection='3d')
        seeds_um = self.seeds * 1e6
        ax1.scatter(seeds_um[:, 0], seeds_um[:, 1], seeds_um[:, 2], 
                   c='red', marker='o', s=10, alpha=0.6)
        ax1.set_xlabel('X (um)')
        ax1.set_ylabel('Y (um)')
        ax1.set_zlabel('Z (um)')
        ax1.set_title('Seed Points Distribution')
        
        # 2. 孔隙大小分布直方图
        ax2 = fig.add_subplot(2, 3, 2)
        ax2.hist(self.pore_sizes, bins=20, alpha=0.7, color='skyblue', edgecolor='black')
        ax2.axvline(np.mean(self.pore_sizes), color='red', linestyle='--', 
                   label=f'Mean: {np.mean(self.pore_sizes):.1f} um')
        ax2.set_xlabel('Pore Size (um)')
        ax2.set_ylabel('Frequency')
        ax2.set_title('Pore Size Distribution')
        ax2.legend()
        ax2.grid(True, alpha=0.3)
        
        # 3. Voronoi结构3D视图（简化）
        ax3 = fig.add_subplot(2, 3, 3, projection='3d')
        # 显示少量单元以避免过于复杂
        max_show = min(20, len(self.interior_cells))
        for i, cell in enumerate(self.interior_cells[:max_show]):
            vertices = cell['vertices'] * 1e6
            # 简化显示：只显示中心点和边界
            center = cell['center'] * 1e6
            ax3.scatter(center[0], center[1], center[2], 
                       c='blue', s=50, alpha=0.8)
        
        ax3.set_xlabel('X (um)')
        ax3.set_ylabel('Y (um)')
        ax3.set_zlabel('Z (um)')
        ax3.set_title(f'Voronoi Cells (showing {max_show} cells)')
        
        # 4. Z方向孔隙大小变化
        ax4 = fig.add_subplot(2, 3, 4)
        z_positions = []
        pore_sizes_z = []
        
        for i, cell in enumerate(self.interior_cells):
            if i < len(self.pore_sizes):
                z_pos = cell['center'][2] * 1e6  # 转换为微米
                z_positions.append(z_pos)
                pore_sizes_z.append(self.pore_sizes[i])
        
        ax4.scatter(z_positions, pore_sizes_z, alpha=0.6, c='green')
        ax4.set_xlabel('Z Position (um)')
        ax4.set_ylabel('Pore Size (um)')
        ax4.set_title('Pore Size vs Z Position')
        ax4.grid(True, alpha=0.3)
        
        # 5. 支架统计信息
        ax5 = fig.add_subplot(2, 3, 5)
        ax5.axis('off')
        
        stats_text = f"""
Scaffold Statistics:
─────────────────────
Dimensions: {self.x_size*1e6:.0f} × {self.y_size*1e6:.0f} × {self.z_size*1e6:.0f} μm
Total Seeds: {len(self.seeds)}
Interior Cells: {len(self.interior_cells)}

Pore Analysis:
─────────────────────
Mean Pore Size: {np.mean(self.pore_sizes):.2f} ± {np.std(self.pore_sizes):.2f} μm
Min Pore Size: {np.min(self.pore_sizes):.2f} μm
Max Pore Size: {np.max(self.pore_sizes):.2f} μm

Target Porosity: {self.target_porosity*100:.1f}%
Seed Density: {self.seed_density if self.seed_density else 'Auto'} seeds/mm³
        """
        
        ax5.text(0.1, 0.9, stats_text, transform=ax5.transAxes, 
                fontsize=10, verticalalignment='top', fontfamily='monospace')
        
        # 6. 孔隙大小箱线图
        ax6 = fig.add_subplot(2, 3, 6)
        ax6.boxplot(self.pore_sizes, labels=['Pore Size'])
        ax6.set_ylabel('Pore Size (um)')
        ax6.set_title('Pore Size Distribution (Box Plot)')
        ax6.grid(True, alpha=0.3)
        
        plt.suptitle('Voronoi Scaffold Structure Analysis', fontsize=16, fontweight='bold')
        plt.tight_layout()
        
        # 保存图片
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"[SUCCESS] 支架结构图已保存: {save_path}")
        
        plt.close()
        
        return fig
    
    def plot_pore_size_distribution(self):
        """绘制孔隙大小分布直方图"""
        if len(self.pore_sizes) == 0:
            raise ValueError("请先计算统计信息")
        
        plt.figure(figsize=(10, 6))
        plt.hist(self.pore_sizes, bins=30, alpha=0.7, color='skyblue', edgecolor='black')
        plt.axvline(np.mean(self.pore_sizes), color='red', linestyle='--', 
                   label=f'Mean: {np.mean(self.pore_sizes):.2f} μm')
        plt.xlabel('孔隙大小 (μm)')
        plt.ylabel('频数')
        plt.title('孔隙大小分布')
        plt.legend()
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        plt.close()


if __name__ == "__main__":
    # 测试示例
    print("="*60)
    print("  Voronoi生物支架生成器测试")
    print("="*60)
    
    # 创建生成器
    gen = VoronoiScaffoldGenerator(
        x_size=1e-3,      # 1 mm
        y_size=1e-3,      # 1 mm
        z_size=0.5e-3,    # 0.5 mm
        target_porosity=0.7,
        seed_density=10   # 10 seeds/mm³
    )
    
    # 生成和处理
    gen.generate_seeds()
    gen.compute_voronoi()
    gen.extract_interior_cells()
    gen.compute_cell_statistics()
    
    # 可视化
    gen.visualize_seeds()
    gen.plot_pore_size_distribution()
    
    print("\n[COMPLETE] 测试完成！")
