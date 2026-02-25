# BCC Reciprocal Lattice Visualization
This program visualizes the reciprocal lattice of a Body-Centered Cubic (BCC) structure, with interactive controls for rotation, zoom, and manipulation. The visualization allows you to explore the BCC structure in 3D, with the ability to rotate the lattice and zoom in or out using mouse scroll or keyboard shortcuts. Keep in mind that this visualization is not based on actual calculation of lattice structure governed by the physical principles underlying atomic lattice concepts of the BCC structure(s). Instead, it is a manually constructed model of the BCC lattice structure, designed to approximate the real lattice structure. This model is intended primarily for educational and illustrative purposes.

## Features:
- **Interactive Controls:**
  - Drag the mouse to rotate the BCC structure.
  - Zoom in and out with the mouse scroll wheel.
  - Zoom in and out using the **Ctrl + Up/Down** arrow keys.
  - Play and pause the animation using the **Play** and **Pause** buttons.
  - Exit the program using the **Exit** button.

## How to Use:
1. Ensure the program files are properly set up in the same folder. The following files and folders must be in the same directory as the executable (`.exe`):
   - **`config.json`**: This file contains the program's configuration settings (e.g., window size, zoom level, rotation angles).
   - **`_internal` folder**: This folder contains necessary resources and assets required by the program.
2. Double-click the executable (`.exe`) file to launch the program.
3. (Optional) To customize the program's behavior, edit the `config.json` file before launching the executable.
   (Look into **## Configuration** part below for details on the available settings.)

## Known Issues:
- **Stationary Center Point Issue:**
  - There is a minor issue with the behavior of the stationary center point during zooming. After zooming in or out multiple times, the center point (which is supposed to remain fixed) may shift slightly.
  - This issue is caused by the way zooming adjustments are made, and while the movement is minimal, it might be noticeable when zooming repeatedly. This is a known limitation in the current implementation.
  
  **Workaround:** There isn't a direct fix for this issue at the moment, but the behavior is relatively subtle and does not significantly affect the overall functionality of the program.

## Configuration:
- You can adjust the initial settings (such as window size, zoom level, and rotation angles) by modifying the `config.json` file in the same directory as the executable.

### Example `config.json`:
```json
{
  "window_width": 800,
  "window_height": 600,
  "initial_zoom": 80,
  "initial_rotation_x": 2,
  "initial_rotation_y": 2
}