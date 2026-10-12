import flet as ft

from ui.widgets import (
    Label,
    OptionCheckbox,
    PasswordLen,
    GeneratePassword,
    PasswordWindow,
    CopyButton,
    TextWindow,
)
from models.generate import Password, Encrypt


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
        super().__init__(spacing=5)
        self.sourceWindow = TextWindow(text="", hint="текст")
        self.keyWindow = TextWindow(text="", hint="ключ")
        self.resultWindow = TextWindow(text="", hint="результат", read_only=True)
        self.copyButton = CopyButton(copyText=self.resultWindow.value)
        self.copyButton.disabled = True
        self.encryptButton = GeneratePassword("Зашифровать", click_event=self.encrypt)
        self.decryptButton = GeneratePassword("Расшифровать", click_event=self.decrypt)

        self.controls = [
            ft.Row(
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                controls=[
                    Label(txt="Исходный текст", size=25),
                    Label(txt="Результат", size=25)
                ]
            ),
            ft.Row(
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                controls=[
                    self.sourceWindow,
                    ft.Row(controls=[self.copyButton, self.resultWindow])
                ]
            ),
            ft.Row(
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                controls=[
                    self.keyWindow,
                    ft.Row(controls=[self.encryptButton, self.decryptButton])
                ]
            )
        ]

    def encrypt(self):
        Encrypt(self.sourceWindow, self.keyWindow, self.resultWindow, self.copyButton, cryptT="crypt").work()

    def decrypt(self):
        Encrypt(self.sourceWindow, self.keyWindow, self.resultWindow, self.copyButton, cryptT="uncrypt").work()
