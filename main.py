import tcod
import traceback

import color
import exceptions
import input_handlers
import setup_game

def main() -> None:
    screen_width = 80
    screen_height = 50

    debug_mode = True


    tileset = tcod.tileset.load_tilesheet("dejavu10x10_gs_tc.png", 32, 8, tcod.tileset.CHARMAP_TCOD)

    handler: input_handlers.BaseEventHandler = setup_game.MainMenu()

    with tcod.context.new_terminal(
        screen_width,
        screen_height,
        tileset=tileset,
        title="Yet Another Roguelike",
        vsync=True,
    ) as context:
        root_console = tcod.Console(screen_width, screen_height, order="F")
        try:
            while True:
                root_console.clear()
                handler.on_render(console=root_console)
                context.present(root_console)

                try:
                    for event in tcod.event.wait():
                        context.convert_event(event)
                        handler = handler.handle_events(event)
                except Exception: # Handle exceptions in game.
                    traceback.print_exc() # Print error to stderr
                    # Then print the error to the message log.
                    if isinstance(handler, input_handlers.EventHandler):
                        handler.engine.message_log.add_message(
                            traceback.format_exc(), color.error
                        )
        except exceptions.QuitWithoutSaving:
            raise
        except SystemExit: # Save and quit.
            # TODO: Add the save function here
            raise
        except BaseException: # Save on any other unexpected exceptions
            # TODO  Add the save function here
            raise

if __name__ == "__main__":
    main()