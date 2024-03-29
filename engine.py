from __future__ import annotations

from typing import TYPE_CHECKING, Optional
from entity import Actor

from tcod.console import Console
from tcod.map import compute_fov
from game_map import GameMap

from message_log import MessageLog
from render_functions import render_bar, render_names_at_mouse_location

import exceptions

if TYPE_CHECKING:
    from entity import Entity
    from engine import Engine

class Engine:
    game_map: GameMap
    
    def __init__(self, player: Actor):
        self.message_log = MessageLog()
        self.mouse_location = (0, 0)
        self.player = player

    def handle_enemy_turns(self) -> None:
        for entity in set(self.game_map.actors) - {self.player}:
            if entity.ai:
                try:
                    entity.ai.perform()
                except exceptions.Impossible:
                    pass #Ignore impossible action exception from AI


    def update_fov(self) -> None:
        self.game_map.visible[:] = compute_fov(
            self.game_map.tiles["transparent"],
            (self.player.x, self.player.y),
            radius=8,
        )

        self.game_map.explored |= self.game_map.visible

    def render(self, console: Console) -> None:
        self.game_map.render(console)

        self.message_log.render(console=console, x=21, y=45, width=40, height=5)

        render_bar(
            console=console,
            current_value=self.player.fighter.hp,
            maximum_value=self.player.fighter.max_hp,
            total_width=20,
        )

        render_names_at_mouse_location(console=console, x=21, y=44, engine=self)
        # Old HP stats display
        # console.print(
        #     x=1,
        #     y=47,
        #     string=f"HP: {self.player.fighter.hp}/{self.player.fighter.max_hp}",
        # )