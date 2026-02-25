# BCC visualizer program and its reciprocal lattice
import pygame
import numpy as np
from math import cos, sin
import sys
import os
import json

# --- Load Configuration ---
def load_config():
    # Open the JSON configuration file
    with open('config.json', 'r') as f:
        config = json.load(f)
    return config

# Load configuration when the program starts
config = load_config()

# Apply settings from the config file
WIDTH = config['window_width']
HEIGHT = config['window_height']
scale = config['initial_zoom']
angle_x = config['initial_rotation_x']
angle_y = config['initial_rotation_y']

# --- Colors and Screen Setup ---
BG = (200, 200, 225)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
GRAY = (150, 150, 150)

pygame.display.set_caption("BCC Reciprocal Lattice Visualization")
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# Set window icon
def resource_path(relative_path):
    try:
        # PyInstaller creates a temp directory and stores path there
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

icon_path = resource_path("BCC.png")  # Replace with the path to your icon file
icon = pygame.image.load(icon_path)
pygame.display.set_icon(icon)

# --- Initialize Pygame Font ---
pygame.font.init()  # Initialize the font system

# --- Initial Settings ---
scale = 100
circle_pos = [WIDTH / 2 - scale * 1, HEIGHT / 2 + scale * 1]  # Center the focal point at (1, -1, 1)
angle = 0

# --- Define 3D Points (BCC Atoms) ---
bcc_atom1 = np.array([
    [-1, -3, 1], [1, -3, 1], [1, -1, 1], [-1, -1, 1],
    [-1, -3, 3], [1, -3, 3], [1, -1, 3], [-1, -1, 3]
])
bcc_atom2 = np.array([
    [1, -3, -1], [3, -3, -1], [3, -1, -1], [1, -1, -1],
    [1, -3, 1], [3, -3, 1], [3, -1, 1], [1, -1, 1]
])
bcc_atom3 = np.array([
    [1, 1, 1], [3, 1, 1], [3, -1, 1], [1, -1, 1],
    [1, 1, 3], [3, 1, 3], [3, -1, 3], [1, -1, 3]
])

# Combine the points from all atoms
points = [np.matrix(coord) for cube in [bcc_atom1, bcc_atom2, bcc_atom3] for coord in cube]
intersection_point = np.array([1, -1, 1])

# Calculate centers of each cube
cube_centers = [
    np.mean(bcc_atom1, axis=0),
    np.mean(bcc_atom2, axis=0),
    np.mean(bcc_atom3, axis=0)
]

# --- Projection and Transformation ---
projection_matrix = np.matrix([
    [1, 0, 0],
    [0, 1, 0]
])

projected_points = [
    [0, 0] for _ in range(len(points))
]
projected_centers = [[0, 0] for _ in range(len(cube_centers))]

def connect_points(point1, point2):
    pygame.draw.line(screen, BLACK, (point1[0], point1[1]), (point2[0], point2[1]))

def connect_center(point1, point2):
    pygame.draw.line(screen, RED, (point1[0], point1[1]), (point2[0], point2[1]))

# Edges for a single cube
cube_edges = [
    [0, 1], [1, 2], [2, 3], [3, 0],  # Bottom face
    [4, 5], [5, 6], [6, 7], [7, 4],  # Top face
    [0, 4], [1, 5], [2, 6], [3, 7]   # Vertical edges
]

# --- Button Setup ---
button_width = 100
button_height = 40
play_button_rect = pygame.Rect(20, 20, button_width, button_height)
pause_button_rect = pygame.Rect(130, 20, button_width, button_height)
exit_button_rect = pygame.Rect(240, 20, button_width, button_height)

clock = pygame.time.Clock()
running = True
is_playing = True  # Animation starts in play mode

dragging = False  # Track dragging state
prev_mouse_pos = None  # Store the previous mouse position
angle_x = 0  # Rotation angle around X-axis
angle_y = 0  # Rotation angle around Y-axis

button_font = pygame.font.Font(None, 36)

# --- Button Drawing ---
def draw_button(screen, rect, text, font, color=GRAY, text_color=BLACK):
    pygame.draw.rect(screen, color, rect, border_radius=10)
    text_surface = font.render(text, True, text_color)
    text_rect = text_surface.get_rect(center=rect.center)
    screen.blit(text_surface, text_rect)

# --- Rotation Matrices ---
rotation_z, rotation_y, rotation_x = None, None, None

def update_rotation_matrices(angle_x, angle_y, angle_z):
    global rotation_z, rotation_y, rotation_x
    rotation_z = np.matrix([
        [cos(angle_z), -sin(angle_z), 0],
        [sin(angle_z), cos(angle_z), 0],
        [0, 0, 1]
    ])
    rotation_y = np.matrix([
        [cos(angle_y), 0, sin(angle_y)],
        [0, 1, 0],
        [-sin(angle_y), 0, cos(angle_y)]
    ])
    rotation_x = np.matrix([
        [1, 0, 0],
        [0, cos(angle_x), -sin(angle_x)],
        [0, sin(angle_x), cos(angle_x)]
    ])

# --- Event Handling ---
def handle_events():
    global is_playing, dragging, prev_mouse_pos, scale, angle_x, angle_y
    for event in pygame.event.get():
        # Close the application
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # Mouse button pressed
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if play_button_rect.collidepoint(event.pos):  # Play button clicked
                is_playing = True
            elif pause_button_rect.collidepoint(event.pos):  # Pause button clicked
                is_playing = False
            elif exit_button_rect.collidepoint(event.pos):  # Exit button clicked
                pygame.quit()
                sys.exit()
            else:  # Dragging starts
                dragging = True
                prev_mouse_pos = event.pos

        # Mouse button released
        elif event.type == pygame.MOUSEBUTTONUP:
            dragging = False

        # Mouse motion (dragging)
        elif event.type == pygame.MOUSEMOTION and dragging:
            dx, dy = event.pos[0] - prev_mouse_pos[0], event.pos[1] - prev_mouse_pos[1]
            angle_y += dx * 0.005  # Horizontal dragging -> Y-axis rotation
            angle_x += dy * -0.005  # Vertical dragging -> X-axis rotation
            prev_mouse_pos = event.pos

        # Mouse scroll (zoom)
        elif event.type == pygame.MOUSEWHEEL:
            prev_scale = scale  # Save previous scale to adjust position
            scale *= 1.1 if event.y > 0 else 0.9  # Zoom in or out
            scale = max(20, min(scale, 300))  # Limit zoom range
            scale_ratio = scale / prev_scale
            circle_pos[0] = int(WIDTH / 2 + (circle_pos[0] - WIDTH / 2) * scale_ratio)
            circle_pos[1] = int(HEIGHT / 2 + (circle_pos[1] - HEIGHT / 2) * scale_ratio)

        # Keyboard keys (zoom with Ctrl + Up/Down)
        elif event.type == pygame.KEYDOWN:
            keys = pygame.key.get_pressed()  # Check all pressed keys
            if keys[pygame.K_LCTRL] or keys[pygame.K_RCTRL]:  # Check if Ctrl is pressed
                prev_scale = scale  # Save previous scale to adjust position
                if event.key == pygame.K_UP:  # Zoom in
                    scale *= 1.1
                elif event.key == pygame.K_DOWN:  # Zoom out
                    scale *= 0.9
                scale = max(20, min(scale, 300))  # Limit zoom range
                scale_ratio = scale / prev_scale
                circle_pos[0] = int(WIDTH / 2 + (circle_pos[0] - WIDTH / 2) * scale_ratio)
                circle_pos[1] = int(HEIGHT / 2 + (circle_pos[1] - HEIGHT / 2) * scale_ratio)

# --- Transform and Project Points ---
def transform_and_project(point, scale, rotation_matrices, center_pos, intersection_point, projection_matrix):
    point = point - intersection_point
    for rotation_matrix in rotation_matrices:
        point = np.dot(rotation_matrix, point.reshape((3, 1)))
    point += intersection_point.reshape((3, 1))
    projected = np.dot(projection_matrix, point)
    x = int(projected[0][0] * scale) + center_pos[0]
    y = int(projected[1][0] * scale) + center_pos[1]
    return [x, y]

# --- Main Loop ---
while running:
    clock.tick(60)

    # Clear the screen
    screen.fill(BG)

    # Handle all events (user inputs)
    handle_events()

    # Draw buttons (Play, Pause, Exit)
    draw_button(screen, play_button_rect, "Play", button_font, color=GREEN)
    draw_button(screen, pause_button_rect, "Pause", button_font)
    draw_button(screen, exit_button_rect, "Exit", button_font, color=RED, text_color=WHITE)
    
    update_rotation_matrices(angle_x, angle_y, angle)

    # Increment angles only if playing
    if is_playing:
        angle_x += 0.0075
        angle_y += 0.0075

    # Project and draw all cubes
    for cube_idx in range(3):
        for point_idx in range(8):
            projected_points[cube_idx * 8 + point_idx] = transform_and_project(
                points[cube_idx * 8 + point_idx], 
                scale, 
                [rotation_z, rotation_y, rotation_x], 
                circle_pos, 
                intersection_point, 
                projection_matrix
            )
            pygame.draw.circle(screen, BLUE, tuple(projected_points[cube_idx * 8 + point_idx]), 5)

        # Connect edges for the cube
        for edge in cube_edges:
            connect_points(projected_points[cube_idx * 8 + edge[0]], projected_points[cube_idx * 8 + edge[1]])

    # Draw and connect cube centers
    for i, center in enumerate(cube_centers):
        projected_centers[i] = transform_and_project(
            center, 
            scale, 
            [rotation_z, rotation_y, rotation_x], 
            circle_pos, 
            intersection_point, 
            projection_matrix
        )
        pygame.draw.circle(screen, GREEN, tuple(projected_centers[i]), 7)

        intersect_2d = np.dot(projection_matrix, intersection_point.reshape((3, 1)))
        ix = int(intersect_2d[0][0] * scale) + circle_pos[0]
        iy = int(intersect_2d[1][0] * scale) + circle_pos[1]

        connect_center(projected_centers[i], [ix, iy])

    # Display control instructions
    font = pygame.font.Font(None, 24)  # Small font for instructions
    instructions = [
        "Controls:",
        " - Drag the view: Hold Left Mouse Button + Move",
        " - Zoom in/out: Mouse Scroll Wheel",
        " - Zoom in/out Shortcut: Ctrl + Up/Down Arrow",
        " - Play/Pause: Buttons at Top Left",
        " - Exit: Press Exit Button or Close Window"
    ]

    # Render each line of text
    for i, line in enumerate(instructions):
        text_surface = font.render(line, True, BLACK)
        screen.blit(text_surface, (20, HEIGHT - 140 + i * 20))  # Position bottom-left
    
    pygame.display.update()
# Compiling command: pyinstaller --onedir --windowed --icon=icon.png --add-data "BCC.png;." BCC_Visualizer.py
