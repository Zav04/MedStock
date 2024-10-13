def maximize_window(page):
    if not page.window.maximized:
        page.window.maximized = True
        page.update()
    else:
        page.window.maximized = False
        page.update()

def minimize_window(page):
    page.window.minimized = True
    page.update()
