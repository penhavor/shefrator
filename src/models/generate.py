import flet as ft
import secrets
import os
import base64

from abc import ABC, abstractmethod
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.ciphers.aead import AESGCM


class Generate(ABC):
    @abstractmethod
    def work(self):
        pass


class Password(Generate):
    def __init__(self, allChars: tuple, passwordLen, passwordWindow, copyButton):
        self._allChars = allChars
        self._passwordLen = passwordLen
        self._passwordWindow = passwordWindow
        self._copyButton = copyButton

    @property
    def allChars(self):
        return self._allChars

    @allChars.setter
    def allChars(self, value):
        self._allChars = value

    @property
    def passwordLen(self):
        return self._passwordLen

    @passwordLen.setter
    def passwordLen(self, value):
        self._passwordLen = value

    @property
    def passwordWindow(self):
        return self._passwordWindow

    @passwordWindow.setter
    def passwordWindow(self, value):
        self._passwordWindow = value

    @property
    def copyButton(self):
        return self._copyButton

    @copyButton.setter
    def copyButton(self, value):
        self._copyButton = value

    def work(self):
        chars = ""
        for i in self._allChars:
            if i.value:
                chars += i.chars
        if not chars:
            self._passwordWindow.value = "Пароль нельзя сгенерировать!"
            self._copyButton.disabled = True
        else:
            self._copyButton.disabled = False
            self._passwordWindow.value = "".join([secrets.choice(chars) for _ in range(int(self._passwordLen.value))])
            self._copyButton.action = ft.CopyToClipboard(self._passwordWindow.value)

    def __eq__(self, other):
        if not isinstance(other, Password):
            return False
        if self._passwordLen.value != other._passwordLen.value:
            return False
        return [i.chars for i in self._allChars] == [i.chars for i in other._allChars]

    def __lt__(self, other):
        return self._passwordLen.value < other._passwordLen.value

    def __hash__(self):
        return hash((self._passwordLen.value, tuple(i.chars for i in self._allChars)))

    def __repr__(self):
        return f"Password(len={int(self._passwordLen.value)})"

    def __str__(self):
        return f"Генерация пароля длиной {int(self._passwordLen.value)}"


class Encrypt(Generate):
    def __init__(self, sourceWindow, keyWindow, resultWindow, copyButton, cryptT):
        self._sourceWindow = sourceWindow
        self._keyWindow = keyWindow
        self._resultWindow = resultWindow
        self._copyButton = copyButton
        self._cryptT = cryptT

    @property
    def sourceWindow(self):
        return self._sourceWindow

    @sourceWindow.setter
    def sourceWindow(self, value):
        self._sourceWindow = value

    @property
    def keyWindow(self):
        return self._keyWindow

    @keyWindow.setter
    def keyWindow(self, value):
        self._keyWindow = value

    @property
    def resultWindow(self):
        return self._resultWindow

    @resultWindow.setter
    def resultWindow(self, value):
        self._resultWindow = value

    @property
    def copyButton(self):
        return self._copyButton

    @copyButton.setter
    def copyButton(self, value):
        self._copyButton = value

    @property
    def cryptT(self):
        return self._cryptT

    @cryptT.setter
    def cryptT(self, value):
        self._cryptT = value

    def work(self):
        text = self._sourceWindow.value
        password = self._keyWindow.value
        if not text or not password:
            self._resultWindow.value = "Заполните все поля!"
            self._copyButton.disabled = True
            return
        key = hashes.Hash(hashes.SHA256())
        key.update(password.encode())
        aes = AESGCM(key.finalize())
        try:
            if self._cryptT == "uncrypt":
                data = base64.b64decode(text)
                result = aes.decrypt(data[:12], data[12:], None).decode()
            elif self._cryptT == "crypt":
                iv = os.urandom(12)
                result = base64.b64encode(iv + aes.encrypt(iv, text.encode(), None)).decode()
            self._resultWindow.value = result
            self._copyButton.disabled = False
            self._copyButton.action = ft.CopyToClipboard(result)
        except Exception:
            self._resultWindow.value = "Ошибка обработки данных!"
            self._copyButton.disabled = True

    def __eq__(self, other):
        if not isinstance(other, Encrypt):
            return False
        if self._sourceWindow.value != other._sourceWindow.value:
            return False
        if self._keyWindow.value != other._keyWindow.value:
            return False
        return self._cryptT == other._cryptT

    def __lt__(self, other):
        return self._cryptT < other._cryptT

    def __hash__(self):
        return hash((self._sourceWindow.value, self._keyWindow.value, self._cryptT))

    def __repr__(self):
        return f"Encrypt(cryptT={self._cryptT})"

    def __str__(self):
        if self._cryptT == "crypt":
            return "Шифрование текста"
        return "Расшифровка текста"
