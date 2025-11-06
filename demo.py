#!/usr/bin/env python3
"""
Interactive Biomimetic Bone Scaffold Generator - Demo Launcher
Author: Siqi (Qizaifadacai)
Email: fortyseven0629@gmail.com
"""

import sys
import os

def main():
    print("╔════════════════════════════════════════════════════════════╗")
    print("║   Interactive Biomimetic Scaffold Generator v2.0          ║")
    print("║   交互式仿生骨支架生成器                                   ║")
    print("╚════════════════════════════════════════════════════════════╝")
    print()
    print("Features:")
    print("  ✨ TextBox Input - Direct numerical input, no sliders")
    print("  🎨 Colorful 3D Voronoi - 30+ vibrant colors")
    print("  📸 SEM-Style Rendering - Realistic grayscale visualization")
    print("  💾 One-Click Save - Auto-generate 3 high-quality images")
    print()
    print("How to Use:")
    print("  1️⃣  Enter values in textboxes")
    print("  2️⃣  Press Enter to confirm")
    print("  3️⃣  Click 'Generate Scaffold'")
    print("  4️⃣  Click 'Save Visuals' to export")
    print()
    print("Parameter Ranges:")
    print("  • Cortical Density: 5,000 - 40,000 seeds/mm³")
    print("  • Transition Density: 3,000 - 25,000 seeds/mm³")
    print("  • Trabecular Density: 1,000 - 15,000 seeds/mm³")
    print("  • Target Porosity: 40 - 85 %")
    print()
    print("Recommended (Standard Biomimetic Bone):")
    print("  Cortical: 25000, Transition: 12000, Trabecular: 6000, Porosity: 68%")
    print()
    
    input("Press Enter to launch interactive interface...")
    
    try:
        from scaffold_generator import InteractiveGradientScaffoldGenerator
        
        generator = InteractiveGradientScaffoldGenerator(
            x_size=800e-6,
            y_size=800e-6,
            z_size=100e-6,
            target_porosity=0.68
        )
        
        print("\n[INFO] Launching interactive interface...")
        print("       • Interface contains 6 real-time plots")
        print("       • Enter values and press Enter to confirm")
        print("       • Click buttons to generate or save\n")
        
        generator.create_interactive_interface()
        
    except Exception as e:
        print(f"\n❌ Launch failed: {e}")
        print("\nPossible causes:")
        print("  1. Missing dependencies: pip install numpy scipy matplotlib numpy-stl")
        print("  2. Cannot import main module: check file path")
        print("  3. Display environment: ensure GUI is available")
        
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
