# main.py
import pygame
import sys
import os
from config import load_config, BG, GREEN, RED, GRAY, WHITE, BLACK
from lattice import POINTS, CUBE_CENTERS, INTERSECTION
from renderer import project_point, draw_lattice_edges, draw_reciprocal_lines, draw_instructions, draw_button
from ui import handle_events, play_button, pause_button, exit_button

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

def main():
    pygame.init()
    config = load_config()

    WIDTH, HEIGHT = config.window_width, config.window_height
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("BCC Reciprocal Lattice Visualization")

    icon = pygame.image.load(resource_path("BCC.png"))
    pygame.display.set_icon(icon)

    button_font      = pygame.font.Font(None, 36)
    instruction_font = pygame.font.Font(None, 24)
    clock            = pygame.time.Clock()

    state = {
        'is_playing':  True,
        'dragging':    False,
        'prev_mouse':  None,
        'angle_x':     config.initial_rotation_x,
        'angle_y':     config.initial_rotation_y,
        'angle_z':     0.0,
        'scale':       config.initial_zoom,
        'center_pos':  [WIDTH / 2 - config.initial_zoom, HEIGHT / 2 + config.initial_zoom],
        'window_size': (WIDTH, HEIGHT)
    }

    while True:
        clock.tick(60)
        screen.fill(BG)

        state = handle_events(state)

        if state['is_playing']:
            state['angle_x'] += 0.0075
            state['angle_y'] += 0.0075

        # --- Project all points ---
        proj_args = (
            state['angle_x'],
            state['angle_y'],
            state['angle_z'],
            state['scale'],
            state['center_pos'],
            INTERSECTION
        )

        projected_points  = [project_point(p, *proj_args) for p in POINTS]
        projected_centers = [project_point(c, *proj_args) for c in CUBE_CENTERS]

        # --- Draw lattice ---
        for cube_idx in range(3):
            draw_lattice_edges(screen, projected_points, cube_idx)
            for i in range(8):
                pygame.draw.circle(screen, (0, 0, 255), projected_points[cube_idx * 8 + i], 5)

        # --- Draw reciprocal lines and center atoms ---
        intersect_2d = project_point(INTERSECTION, *proj_args)
        draw_reciprocal_lines(screen, projected_centers, intersect_2d)
        for center in projected_centers:
            pygame.draw.circle(screen, (0, 255, 0), center, 7)

        # --- Draw UI ---
        draw_button(screen, play_button,  "Play",  button_font, color=GREEN)
        draw_button(screen, pause_button, "Pause", button_font, color=GRAY)
        draw_button(screen, exit_button,  "Exit",  button_font, color=RED, text_color=WHITE)
        draw_instructions(screen, instruction_font, WIDTH, HEIGHT)

        pygame.display.update()

if __name__ == "__main__":
    main()
