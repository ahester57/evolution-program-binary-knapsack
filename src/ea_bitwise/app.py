# ahester57

import asyncio

from ea_bitwise.menu import GAMenu


class App:
    """Simple class to be used as an entrypoint."""
    def __init__(self) -> None:
        pass

    async def start(self) -> None:
        ga = await GAMenu().configure_ga()
        await ga.simulate()


if __name__ == '__main__':
    app = App()
    try:
        asyncio.run(app.start())
    except EOFError:
        print('^D')
    except KeyboardInterrupt:
        print('^C')
