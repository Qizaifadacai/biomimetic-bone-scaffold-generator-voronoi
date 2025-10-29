# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [2.0.0] - 2025-10-26

### Added
- 🎮 **TextBox input interface** replacing sliders for precise numerical input
- 🎨 **Colorful 3D Voronoi visualization** with 30+ vibrant colors
- 📸 **SEM-style scaffold rendering** with grayscale and dynamic lighting
- 💾 **"Save Visuals" button** for one-click export of 3 visualization types
- 📊 **4-view angle display** in SEM-style visualization
- ⚡ **Real-time parameter validation** with automatic range limiting
- 📝 **Timestamp-based file naming** to prevent overwrites
- 🎯 **Seed point markers** in colorful Voronoi visualization

### Changed
- 🔄 **Interaction method**: Slider-based → TextBox-based
- 🎨 **Voronoi colors**: 3-color gradient → 30+ unique colors
- 📸 **Scaffold rendering**: Simple colored → Professional SEM-style
- 🖼️ **Visualization quality**: Enhanced to 300 DPI for publication

### Improved
- ⚡ **Performance**: Generate only when button clicked (not on every parameter change)
- 🎯 **Precision**: Direct numerical input for exact values
- 📊 **Visual clarity**: Thicker boundaries (2px) and better contrast
- 🔬 **Biomimetic accuracy**: Enhanced gradient analysis and reporting

### Fixed
- 🐛 Fixed issue with slider precision limitations
- 🐛 Fixed color mapping inconsistencies
- 🐛 Fixed file overwrite issues with timestamp implementation

## [1.0.0] - 2025-10-20

### Added
- ⚙️ **Basic Voronoi scaffold generation** with gradient structure
- 📊 **6-panel interactive visualization** (seeds, structure, analysis)
- 🎚️ **Slider-based parameter control** for 4 parameters
- 💾 **STL file export** for 3D printing
- 📈 **Gradient analysis** with layer-by-layer statistics
- 🔬 **Biomimetic structure** (cortical-transition-trabecular)
- 📝 **JSON configuration export**
- 🎨 **Basic 3D visualization** with gradient colors (red-orange-blue)

### Features
- Cortical, transition, and trabecular layer definition (20:30:50 ratio)
- Automatic pore size calculation and analysis
- Real-time seed distribution visualization
- Gradient property analysis and reporting

---

## Version Comparison

| Feature | v1.0.0 | v2.0.0 |
|---------|--------|--------|
| Input Method | Sliders | TextBoxes ✨ |
| Voronoi Colors | 3 colors | 30+ colors ✨ |
| Scaffold Rendering | Basic | SEM-style ✨ |
| Views | 1 angle | 4 angles ✨ |
| Save Options | 1 button | 2 buttons ✨ |
| Output Quality | Standard | 300 DPI ✨ |
| File Naming | Static | Timestamped ✨ |

---

## Roadmap

### Planned for v2.1.0
- [ ] Animation export (rotating Voronoi structure)
- [ ] Batch generation mode
- [ ] Custom color scheme selection
- [ ] Export to multiple STL file formats
- [ ] Interactive 3D rotation in real-time

### Under Consideration
- [ ] Machine learning-based parameter optimization
- [ ] Import/export of custom gradient profiles
- [ ] Integration with FEA software
- [ ] Web-based interface
- [ ] Multi-material scaffold support

---

## Contributors

- **Kiki** - Initial work and v2.0.0 major update

See also the list of [contributors](https://github.com/yourusername/biomimetic-scaffold-generator/contributors) who participated in this project.
