#! /usr/bin/env python
from typing import Tuple, Union
import math
import pygame
COLORS = ((255, 0, 0), (255, 127, 0), (255, 255, 0), (0, 255, 0), (0, 0, 255), (75, 0, 130), (148, 0, 211))
DELAY = 0.8


class Timer:
    def __init__(self):
        self.prev_time = None

    def reset_timer(self) -> None:
        self.prev_time = self.get_epoch()

    def set_time(self, seconds: Union[int, float]) -> None:
        self.prev_time = self.get_epoch() - seconds

    def get_time(self) -> float:
        return 0.0 if self.prev_time is None else self.get_epoch() - self.prev_time

    @staticmethod
    def get_epoch() -> float:
        return pygame.time.get_ticks() / 1000


class ColorMgr:
    def __init__(self, color_list: Tuple[Tuple[int, int, int], ...], transition_time: Union[int, float]):
        self.color_list = color_list
        self.transition_time = transition_time
        self.color_index = -1
        self.distance = (0, 0, 0)
        self.timer = Timer()
        self.timer.reset_timer()
        self.next_color()

    def next_color(self, steps: int = 1) -> None:
        self.color_index = self.add_mod(self.color_index, steps, len(self.color_list))
        next_index = self.add_mod(self.color_index, 1, len(self.color_list))
        self.distance = tuple(self.color_list[next_index][i] - self.color_list[self.color_index][i] for i in range(3))

    def update(self) -> Tuple[int, ...]:
        elapsed_t = self.timer.get_time()
        if elapsed_t > self.transition_time:
            steps, elapsed_t = divmod(elapsed_t, self.transition_time)
            self.next_color(math.floor(steps))
            self.timer.set_time(elapsed_t)
        return tuple(round(self.color_list[self.color_index][i] + self.distance[i] * (elapsed_t / self.transition_time))
                     for i in range(3))

    @staticmethod
    def add_mod(var: int, add: int, mod: int) -> int:
        return (var + add) % mod


class MainProc:
    def __init__(self):
        pygame.init()
        self.display_info = pygame.display.Info()
        self.hardware_res = (self.display_info.current_w, self.display_info.current_h)
        self.min_res = (480, 360)
        self.window_res = self.min_res
        self.color_mgr = ColorMgr(COLORS, DELAY)
        pygame.display.set_caption("Rainbow :D")
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode(self.window_res, pygame.RESIZABLE)
        pygame.event.set_blocked(None)
        pygame.event.set_allowed((pygame.QUIT, pygame.VIDEORESIZE, pygame.KEYDOWN, pygame.KEYUP))
        fps = 60
        game_run = True
        full_screen = False
        while game_run:
            self.clock.tick(fps)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_run = False
                elif event.type == pygame.VIDEORESIZE and not full_screen:
                    self.window_res = tuple(new_res if new_res >= self.min_res[i] else self.min_res[i]
                                            for i, new_res in enumerate((event.w, event.h)))
                    self.screen = pygame.display.set_mode(self.window_res, pygame.RESIZABLE)
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_F11:
                    if full_screen := not full_screen:
                        self.screen = pygame.display.set_mode(self.hardware_res, pygame.FULLSCREEN)
                    else:
                        self.screen = pygame.display.set_mode(self.window_res, pygame.RESIZABLE)
            self.screen.fill(self.color_mgr.update())
            pygame.display.update()
        pygame.quit()


if __name__ == "__main__":
    MainProc()
