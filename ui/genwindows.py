from . import windows, menus

class MainMenuWindow(Window):
    def __init__(self, interf):
        super().__init__(interf)

        mn = menus.Menu()
        mn.menuItems = [menus.MenuItem("abcdef", "a")]

        self.children = []