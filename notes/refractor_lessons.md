# Refractor Notes

## Introduction
My motivation in revising this project is to learn better ways of structuring code. Looking back at the original assignment version, everything was packed into a single file — which worked, but felt messy and hard to navigate. I assumed there had to be a more effective approach, and this revision was my way of finding out what that looks like in practice. Hence, these notes are what i went through and learnt in the process of revising this project.

What I wanted to get out of this:
- Recall and re-understand what this project actually does physically and geometrically
- Practice more structured programming workflow
- Learn how a reasonably well-organized Python app is laid out, especially one with rendering and interactivity

---

## Architecture

The core problem with the original was that a single file was doing everything at once — configuration, geometry data, rendering, event handling, and the main loop all lived together. For 200 lines it was still readable, but it doesn't scale, and more importantly it doesn't communicate intent. A reader has to parse the entire file to understand what any one part is doing.

The fix is separating by responsibility. Each file handles one concern:

- `config.py` — loads settings from `config.json` and exposes color constants
- `lattice.py` — defines the BCC geometry: points, edges, centers, intersection
- `renderer.py` — handles projection, rotation math, and all drawing functions
- `ui.py` — owns event handling and button layout
- `main.py` — wires everything together and runs the main loop

`main.py` is the only file that knows about all the others. Every other file is focused and could be read, tested, or reused independently.

---

## config.py: dataclasses and type hints

Moving configuration into a Python file (rather than reading JSON directly in main) meant I could use a `@dataclass` to give the config a proper structure:

```python
@dataclass
class AppConfig:
    window_width: int
    window_height: int
    initial_zoom: float
    initial_rotation_x: float
    initial_rotation_y: float
```

A few things I learned here:

`@dataclass` automatically generates `__init__` from the field declarations, so you don't write a constructor manually. The type hints (`int`, `float`) aren't enforced at runtime — Python won't crash if the JSON gives the wrong type — but they document intent clearly for anyone reading the code.

`AppConfig(**data)` unpacks the JSON dictionary directly into the dataclass constructor. This works cleanly because the JSON keys match the field names exactly. One clear contract between the JSON and the Python.

`-> AppConfig` on the function is a return type hint — same idea, not enforced but communicates what comes out.

Color constants also live in `config.py` because they're app-wide values with no logic attached. Any module that needs a color just imports it from one place.

---

## lattice.py: data separated from rendering

The BCC geometry — point coordinates, edge connectivity, cube centers, intersection point — all moved into `lattice.py`. Nothing in this file touches pygame or knows anything about the screen.

Two small but meaningful improvements over the original:

`np.matrix` removed in favor of `np.array` everywhere. `np.matrix` is deprecated and was inconsistent — most of the code already used `np.array` and `np.dot()`. The modern convention is `np.array` with `@` for matrix multiplication.

`CUBE_CENTERS` is now computed directly from the point data using `.mean(axis=0)` rather than being hardcoded separately. If the atom positions ever change, the centers follow automatically. One source of truth.

---

## renderer.py: no more globals for rotation state

The original code stored rotation matrices as globals that got overwritten every frame via a function with `global rotation_z, rotation_y, rotation_x`. This made it hard to trace where state lived and what was modifying it.

The fix: `get_rotation_matrices()` now simply returns the three matrices as local values. They're computed fresh each frame and passed where needed. No side effects, no hidden state.

Also fixed: `pygame.font.Font(None, 24)` was being called every single frame inside the main loop in the original. Font objects are expensive to initialize. In the revised version fonts are created once at startup and passed in.

---

## ui.py: state dict instead of scattered globals

Event handling in the original modified several globals directly — `is_playing`, `angle_x`, `angle_y`, `scale`, `dragging`, `prev_mouse_pos` — all scattered across the file with no clear ownership.

The revised approach collects all mutable runtime state into a single dictionary that gets passed into `handle_events()` and returned:

```python
state = {
    'is_playing': True,
    'angle_x': 0.0,
    'scale': 100,
    ...
}
state = handle_events(state)
```

This makes the contract explicit — we can see exactly what the function touches, and `main.py` owns the state rather than it being implicit everywhere. The natural next step beyond this pattern would be a proper class with attributes, which would make sense if the state grew significantly larger.

The zoom logic was also duplicated between mouse scroll and keyboard shortcuts in the original. Extracting it into `_apply_zoom()` means it lives in one place. The underscore prefix is a Python convention signaling it's internal to the module.

---

## Known issue carried over

The intersection point drifts slightly after repeated zooming. This is a floating point rounding accumulation in the zoom calculation — each zoom step introduces a small error that compounds over time. It's minor enough not to affect usability, but worth noting as something to investigate and fix properly later.
