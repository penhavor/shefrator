import flet as ft
import secrets
import os
import base64

from abc import ABC, abstractmethod
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.ciphers.aead import AESGCM


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

class Encrypt(Generate):
    def __init__(self, sourceWindow, keyWindow, resultWindow, copyButton, cryptT):
        self.sourceWindow = sourceWindow
        self.keyWindow = keyWindow
        self.resultWindow = resultWindow
        self.copyButton = copyButton
        self.cryptT = cryptT

    def work(self):
        text = self.sourceWindow.value
        password = self.keyWindow.value
        if not text or not password:
            self.resultWindow.value = "Заполните все поля!"
            self.copyButton.disabled = True
            return
        key = hashes.Hash(hashes.SHA256())
        key.update(password.encode())
        aes = AESGCM(key.finalize())
        try:
            if self.cryptT == "uncrypt":
                data = base64.b64decode(text)
                result = aes.decrypt(data[:12], data[12:], None).decode()
            elif self.cryptT == "crypt":
                iv = os.urandom(12)
                result = base64.b64encode(iv + aes.encrypt(iv, text.encode(), None)).decode()
            self.resultWindow.value = result
            self.copyButton.disabled = False
            self.copyButton.action = ft.CopyToClipboard(result)
        except Exception:
            self.resultWindow.value = "Ошибка обработки данных!"
            self.copyButton.disabled = True


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