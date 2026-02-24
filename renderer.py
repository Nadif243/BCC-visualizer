# renderer.py
import pygame
import numpy as np
from math import cos, sin
from config import BG, BLACK, BLUE, GREEN, RED, WHITE, GRAY
from lattice import CUBE_EDGES

# --- Projection Matrix ---
PROJECTION = np.array([
    [1, 0, 0],
    [0, 1, 0]
], dtype=float)

# --- Rotation Matrices ---
def get_rotation_matrices(angle_x, angle_y, angle_z):
    rx = np.array([
        [1,          0,           0],
        [0, cos(angle_x), -sin(angle_x)],
        [0, sin(angle_x),  cos(angle_x)]
    ], dtype=float)
    ry = np.array([
        [ cos(angle_y), 0, sin(angle_y)],
        [0,             1,           0],
        [-sin(angle_y), 0, cos(angle_y)]
    ], dtype=float)
    rz = np.array([
        [cos(angle_z), -sin(angle_z), 0],
        [sin(angle_z),  cos(angle_z), 0],
        [0,             0,            1]
    ], dtype=float)
    return rx, ry, rz

# --- Transform and Project a Single Point ---
def project_point(point, angle_x, angle_y, angle_z, scale, center_pos, origin):
    rx, ry, rz = get_rotation_matrices(angle_x, angle_y, angle_z)

    p = point - origin # origin = intersection
    p = rz @ p
    p = ry @ p
    p = rx @ p
    p = p + origin

    projected = PROJECTION @ p
    x = int(projected[0] * scale) + center_pos[0]
    y = int(projected[1] * scale) + center_pos[1]
    return [x, y]

# --- Drawing Functions ---
def draw_button(screen, rect, text, font, color=GRAY, text_color=BLACK):
    pygame.draw.rect(screen, color, rect, border_radius=10)
    text_surface = font.render(text, True, text_color)
    text_rect = text_surface.get_rect(center=rect.center)
    screen.blit(text_surface, text_rect)

def draw_lattice_edges(screen, projected_points, cube_idx):
    for edge in CUBE_EDGES:
        p1 = projected_points[cube_idx * 8 + edge[0]]
        p2 = projected_points[cube_idx * 8 + edge[1]]
        pygame.draw.line(screen, BLACK, p1, p2)

def draw_reciprocal_lines(screen, projected_centers, intersection_2d):
    for center in projected_centers:
        pygame.draw.line(screen, RED, center, intersection_2d)

def draw_instructions(screen, font, width, height):
    instructions = [
        "Controls:",
        " - Drag the view: Hold Left Mouse Button + Move",
        " - Zoom in/out: Mouse Scroll Wheel",
        " - Zoom in/out Shortcut: Ctrl + Up/Down Arrow",
        " - Play/Pause: Buttons at Top Left",
        " - Exit: Press Exit Button or Close Window"
    ]
    for i, line in enumerate(instructions):
        text_surface = font.render(line, True, BLACK)
        screen.blit(text_surface, (20, height - 140 + i * 20))
