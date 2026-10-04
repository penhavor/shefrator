import flet as ft


class Label(ft.Text):
    def __init__(self, txt, size):
        super().__init__(value=txt, size=size, weight=ft.FontWeight.BOLD)

class OptionCheckbox(ft.Checkbox):
    def __init__(self, txt, default, chars):
        super().__init__(label=txt, value=default)
        self.chars = chars


class PasswordPanel(ft.Column):
    def __init__(self):
        super().__init__(spacing=10)
        self.dig = OptionCheckbox(txt="цифры", default=True, chars="0123456789")
        self.spec = OptionCheckbox(txt="спец. символы", default=True, chars="`~!@\"'#№$;%^:&?*+-_(){}[]/\\,.|")
        self.lowers = OptionCheckbox(txt="маленькие буквы", default=True, chars="abcdefghijklmnopqrstuvwxyz")
        self.uppers = OptionCheckbox(txt="большие буквы", default=True, chars="ABCDEFGHIJKLMNOPQRSTUVWXYZ")
        self.repeat = OptionCheckbox(txt="повторения", default=True, chars="")
        self.controls = [
            Label(txt="Настройки пароля", size=25),
            self.dig,
            self.spec,
            self.lowers,
            self.uppers,
            self.repeat,
        ]

    def get_chars(self):
        chars = ""
        for box in (self.dig, self.spec, self.lowers, self.uppers):
            if box.value:
                chars += box.chars
        return chars

class CryptoPanel(ft.Column):
    def __init__(self):
        super().__init__(spacing=10)
        self.controls = [
            Label(txt="Шифрование и Дешифрование", size=25),
            ft.Text(value="потом чего-нибудь добавлю"),
        ]
