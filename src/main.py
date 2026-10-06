import flet as ft
import panels as pn
import os


class Switch(ft.FilledButton):
    def __init__(self, txt: str, click_event):
        super().__init__(
            content=ft.Text(value=txt, size=20, weight=ft.FontWeight.BOLD),
            on_click=click_event,
            width=420, height=70,
            bgcolor="grey"
        )


class Main:
    def __init__(self, page):
        self.page = page
        page.window.icon = "icon.ico"
        self.active = ""

        self.password = Switch(txt="Сгенерировать Пароль/Ключ", click_event=self.password_click)
        self.crypt = Switch(txt="Шифрование и Дешифрование", click_event=self.crypto_click)
        self.body = ft.Container(expand=True, padding=20)
        self.panel_password = pn.PasswordPanel()
        self.panel_crypto = pn.CryptoPanel()

        self.password_click()

    def color_set(self):
        if self.active == "key":
            self.password.bgcolor = "green"
            self.crypt.bgcolor = "grey"
        elif self.active == "crypto":
            self.password.bgcolor = "grey"
            self.crypt.bgcolor = "green"
    
    def password_click(self):
        self.active = "key"
        self.color_set()
        self.body.content = self.panel_password

    def crypto_click(self):
        self.active = "crypto"
        self.color_set()
        self.body.content = self.panel_crypto

    def create(self):
        self.page.title = "SheFraTor"
        self.page.add(
            ft.SafeArea(
                expand=True,
                content=ft.Column(
                    horizontal_alignment=ft.CrossAxisAlignment.STRETCH,  # !
                    spacing=10,
                    controls=[
                        ft.Row(
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                            spacing=20,
                            controls=[self.password, self.crypt],
                        ),
                        ft.Divider(thickness=2, color="black"),
                        self.body,
                    ],
                ),
            )
        )

    @staticmethod
    def main(page: ft.Page):
        Main(page).create()


if __name__ == "__main__":
    ft.run(Main.main)
