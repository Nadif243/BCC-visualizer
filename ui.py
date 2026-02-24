# ui.py
import pygame
import sys
from config import load_config

# --- Button Layout ---
BUTTON_WIDTH = 100
BUTTON_HEIGHT = 40

play_button   = pygame.Rect(20,  20, BUTTON_WIDTH, BUTTON_HEIGHT)
pause_button  = pygame.Rect(130, 20, BUTTON_WIDTH, BUTTON_HEIGHT)
exit_button   = pygame.Rect(240, 20, BUTTON_WIDTH, BUTTON_HEIGHT)

# --- Event Handler ---
def handle_events(state):
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if play_button.collidepoint(event.pos):
                state['is_playing'] = True
            elif pause_button.collidepoint(event.pos):
                state['is_playing'] = False
            elif exit_button.collidepoint(event.pos):
                pygame.quit()
                sys.exit()
            else:
                state['dragging'] = True
                state['prev_mouse'] = event.pos

        elif event.type == pygame.MOUSEBUTTONUP:
            state['dragging'] = False

        elif event.type == pygame.MOUSEMOTION and state['dragging']:
            dx = event.pos[0] - state['prev_mouse'][0]
            dy = event.pos[1] - state['prev_mouse'][1]
            state['angle_y'] += dx *  0.005
            state['angle_x'] += dy * -0.005
            state['prev_mouse'] = event.pos

        elif event.type == pygame.MOUSEWHEEL:
            state = _apply_zoom(state, event.y > 0)

        elif event.type == pygame.KEYDOWN:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LCTRL] or keys[pygame.K_RCTRL]:
                if event.key == pygame.K_UP:
                    state = _apply_zoom(state, zoom_in=True)
                elif event.key == pygame.K_DOWN:
                    state = _apply_zoom(state, zoom_in=False)

    return state

# --- Zoom Helper ---
def _apply_zoom(state, zoom_in):
    prev_scale = state['scale']
    state['scale'] *= 1.1 if zoom_in else 0.9
    state['scale'] = max(20, min(state['scale'], 300))

    ratio = state['scale'] / prev_scale
    cx, cy = state['center_pos']
    w, h   = state['window_size']
    state['center_pos'] = [
        int(w / 2 + (cx - w / 2) * ratio),
        int(h / 2 + (cy - h / 2) * ratio)
    ]
    return state
