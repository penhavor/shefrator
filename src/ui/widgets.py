import flet as ft


class Switch(ft.FilledButton):
    def __init__(self, txt: str, click_event):
        super().__init__(
            content=ft.Text(value=txt, size=20, weight=ft.FontWeight.BOLD),
            on_click=click_event,
            width=420, height=70,
            bgcolor="grey"
        )


class Label(ft.Text):
    def __init__(self, txt, size):
        super().__init__(value=txt, size=size, weight=ft.FontWeight.BOLD)


class OptionCheckbox(ft.Checkbox):
    def __init__(self, txt, default, chars):
        super().__init__(label=txt, value=default)
        self._chars = chars

    @property
    def chars(self):
        return self._chars

    @chars.setter
    def chars(self, value):
        self._chars = value


class PasswordLen(ft.Slider):
    def __init__(self):
        super().__init__(value=16, min=8, max=64, divisions=56, width=300, label="{value} символов")


class GeneratePassword(ft.FilledButton):
    def __init__(self, txt, click_event):
        super().__init__(content=txt, on_click=click_event, width=300, height=50)


class PasswordWindow(ft.TextField):
    def __init__(self, text):
        super().__init__(value=text, read_only=True)


class CopyButton(ft.Button):
    def __init__(self, copyText):
        super().__init__(icon=ft.Icons.COPY, action=ft.CopyToClipboard(copyText))


class TextWindow(ft.TextField):
    def __init__(self, text, hint, read_only=False):
        super().__init__(
            value=text,
            hint_text=hint,
            read_only=read_only,
            multiline=True,
            min_lines=4,
            max_lines=8,
            width=300
        )
