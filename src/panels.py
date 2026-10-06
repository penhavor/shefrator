import flet as ft
import secrets
from abc import ABC, abstractmethod


class Label(ft.Text):
    def __init__(self, txt, size):
        super().__init__(value=txt, size=size, weight=ft.FontWeight.BOLD)

class OptionCheckbox(ft.Checkbox):
    def __init__(self, txt, default, chars):
        super().__init__(label=txt, value=default)
        self.chars = chars

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


class Generate(ABC):
    @abstractmethod
    def work(self):
        pass

class Password(Generate):
    def __init__(self, allChars: tuple, passwordLen, passwordWindow, copyButton):
        self.allChars = allChars
        self.passwordLen = passwordLen
        self.passwordWindow = passwordWindow
        self.copyButton = copyButton

    def work(self):
        chars = ""
        for i in self.allChars:
            if i.value:
                chars += i.chars
        if not chars:
            self.passwordWindow.value = "Пароль нельзя сгенерировать!"
            self.copyButton.disabled = True
        else:
            self.copyButton.disabled = False
            self.passwordWindow.value = "".join([secrets.choice(chars) for _ in range(int(self.passwordLen.value))])
            self.copyButton.action = ft.CopyToClipboard(self.passwordWindow.value)


class PasswordPanel(ft.Column):
    def __init__(self):
        super().__init__(spacing=5)
        self.dig = OptionCheckbox(txt="цифры", default=True, chars="0123456789")
        self.spec = OptionCheckbox(txt="спец. символы", default=True, chars="`~!@\"'#№$;%^:&?*+-_(){}[]/\\,.|")
        self.lowers = OptionCheckbox(txt="маленькие буквы", default=True, chars="abcdefghijklmnopqrstuvwxyz")
        self.uppers = OptionCheckbox(txt="большие буквы", default=True, chars="ABCDEFGHIJKLMNOPQRSTUVWXYZ")
        self.passwordLen = PasswordLen()

        self.generatePassword = GeneratePassword("Сгенерировать пароль", click_event=self.generate)
        self.passwordWindow = PasswordWindow(text="")
        self.copyButton = CopyButton(copyText=self.passwordWindow.value)
        self.copyButton.disabled = True

        self.controls = [
            ft.Row(
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                controls=[
                    Label(txt="Настройки пароля", size=25),
                    Label(txt="Генерация пароля", size=25)
                ]
            ),
            self.dig,
            ft.Row(
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                controls=[self.spec, self.generatePassword]
            ),
            ft.Row(
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                controls=[
                    self.lowers,
                    ft.Row(controls=[self.passwordWindow, self.copyButton])
                ]
            ),
            self.uppers,
            ft.Row(
                controls=[self.passwordLen, Label(txt="Длина пароля", size=16)]
            )
        ]

    def generate(self):
        allChars = (self.dig, self.spec, self.lowers, self.uppers)
        password = Password(allChars, self.passwordLen, self.passwordWindow, self.copyButton)
        password.work()

class CryptoPanel(ft.Column):
    def __init__(self):
        super().__init__(spacing=10)
        self.controls = [
            Label(txt="Шифрование и Дешифрование", size=25),
            ft.Text(value="потом чего-нибудь добавлю...")
        ]
