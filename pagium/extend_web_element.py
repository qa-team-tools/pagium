from selenium.webdriver.remote.command import Command
from selenium.webdriver.remote.webelement import WebElement


def extend_web_element():
    def move_to(web_element: WebElement):
        web_element._execute(Command.MOVE_TO, {'element': web_element._id})

    if not getattr(WebElement, 'move_to', None):
        WebElement.move_to = move_to
    if not getattr(WebElement, 'focus', None):
        WebElement.focus = move_to
