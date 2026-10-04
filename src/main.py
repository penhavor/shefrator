import flet as ft


class Switch(ft.FilledButton):
    def __init__(self, txt: str, click_event):
        super().__init__(
            content=ft.Text(txt, size=20, weight=ft.FontWeight.BOLD),
            on_click=click_event,
            width=420,
            height=70,
            bgcolor="grey"
        )


class App:
    def __init__(self, page):
        self.page = page
        self.active = ""
        self.password = Switch(txt="Сгенерировать Пароль/Ключ", click_event=self.key_click)
        self.crypt = Switch(txt="Шифрование и Дешифрование", click_event=self.crypto_click)

    def color_set(self):
        if self.active == "key":
            self.password.bgcolor = "green"
            self.crypt.bgcolor = "grey"
        elif self.active == "crypto":
            self.password.bgcolor = "grey"
            self.crypt.bgcolor = "green"
    
    def key_click(self):
        self.active = "key"
        self.color_set()

    def crypto_click(self):
        self.active = "crypto"
        self.color_set()

    def create(self):
        self.page.title = "SheFraTor"
        self.page.add(
            ft.SafeArea(
                expand=True,
                content=ft.Column(
                    horizontal_alignment=ft.CrossAxisAlignment.STRETCH,  # !
                    spacing=20,
                    controls=[
                        ft.Row(
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                            spacing=20,
                            controls=[self.password, self.crypt],
                        ),
                        ft.Divider(thickness=2, color="black")
                    ],
                ),
            )
        )

    @staticmethod
    def main(page: ft.Page):
        App(page).create()


if __name__ == "__main__":
    ft.run(App.main)