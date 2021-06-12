from entity import Entity

player = Entity(char="@", color=(255,255,255), name="Player", blocks_movement=True)

goblin = Entity(char="g", color=(63,127,63), name="Goblin", blocks_movement=True)
hobgoblin = Entity(char="H", color=(0,127,0), name="Hobgoblin", blocks_movement=True)