from kivy.app import App
from kivy.lang import Builder
from kivy.core.clipboard import Clipboard
from kivy.properties import StringProperty, BooleanProperty
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.utils import get_color_from_hex
import secrets
import string
from datetime import datetime
from pathlib import Path

KV = r"""
#:import dp kivy.metrics.dp

<ChoiceRow@BoxLayout>:
    text: ""
    active: False
    size_hint_y: None
    height: dp(44)
    spacing: dp(8)
    CheckBox:
        active: root.active
        on_active: root.active = self.active
        size_hint_x: None
        width: dp(42)
        color: 1, 1, 1, 1
    Label:
        text: root.text
        color: 0.88, 0.90, 0.95, 1
        halign: "left"
        valign: "middle"
        text_size: self.size

<MainScreen>:
    orientation: "vertical"
    padding: dp(20)
    spacing: dp(12)
    canvas.before:
        Color:
            rgba: 0.055, 0.067, 0.10, 1
        Rectangle:
            pos: self.pos
            size: self.size

    Label:
        text: "[b]SAD1ST[/b]  [color=#7C9CFF]PASSWORD GENERATOR[/color]"
        markup: True
        font_size: "20sp"
        size_hint_y: None
        height: dp(48)

    Label:
        text: "Створюй надійні випадкові паролі"
        color: 0.62, 0.67, 0.77, 1
        font_size: "13sp"
        size_hint_y: None
        height: dp(24)

    BoxLayout:
        orientation: "vertical"
        padding: dp(16)
        spacing: dp(10)
        size_hint_y: None
        height: self.minimum_height
        canvas.before:
            Color:
                rgba: 0.10, 0.12, 0.18, 1
            RoundedRectangle:
                pos: self.pos
                size: self.size
                radius: [dp(16)]

        Label:
            text: "ДОВЖИНА ПАРОЛЯ"
            color: 0.78, 0.82, 0.90, 1
            bold: True
            size_hint_y: None
            height: dp(24)
            halign: "left"
            text_size: self.size

        TextInput:
            id: length_input
            text: "16"
            input_filter: "int"
            multiline: False
            size_hint_y: None
            height: dp(48)
            font_size: "18sp"
            foreground_color: 1, 1, 1, 1
            background_color: 0.14, 0.17, 0.25, 1
            cursor_color: 0.49, 0.61, 1, 1
            hint_text: "Від 1 до 128"

        Label:
            text: "ТИПИ СИМВОЛІВ"
            color: 0.78, 0.82, 0.90, 1
            bold: True
            size_hint_y: None
            height: dp(24)
            halign: "left"
            text_size: self.size

        ChoiceRow:
            id: lower_choice
            text: "Малі літери (a-z)"
            active: True
        ChoiceRow:
            id: upper_choice
            text: "Великі літери (A-Z)"
            active: True
        ChoiceRow:
            id: digit_choice
            text: "Цифри (0-9)"
            active: True
        ChoiceRow:
            id: symbol_choice
            text: "Спеціальні символи (!@#...)"
            active: False

        Button:
            text: "ЗГЕНЕРУВАТИ ПАРОЛЬ"
            size_hint_y: None
            height: dp(52)
            background_normal: ""
            background_color: 0.25, 0.38, 0.82, 1
            bold: True
            on_release: root.generate_password()

        Label:
            text: "РЕЗУЛЬТАТ"
            color: 0.78, 0.82, 0.90, 1
            bold: True
            size_hint_y: None
            height: dp(24)
            halign: "left"
            text_size: self.size

        TextInput:
            id: result_input
            text: "Тут з'явиться пароль"
            readonly: True
            multiline: False
            size_hint_y: None
            height: dp(52)
            font_size: "16sp"
            foreground_color: 0.60, 0.73, 1, 1
            background_color: 0.14, 0.17, 0.25, 1
            halign: "center"

        BoxLayout:
            size_hint_y: None
            height: dp(46)
            spacing: dp(8)
            Button:
                text: "КОПІЮВАТИ"
                background_normal: ""
                background_color: 0.18, 0.22, 0.32, 1
                on_release: root.copy_password()
            Button:
                text: "ЗБЕРЕГТИ"
                background_normal: ""
                background_color: 0.18, 0.22, 0.32, 1
                on_release: root.save_password()

    Button:
        text: "ІСТОРІЯ ПАРОЛІВ"
        size_hint_y: None
        height: dp(46)
        background_normal: ""
        background_color: 0.14, 0.17, 0.25, 1
        on_release: root.show_history()

    Label:
        text: "SAD1ST • локальне збереження на пристрої"
        color: 0.42, 0.47, 0.57, 1
        font_size: "11sp"
        size_hint_y: None
        height: dp(22)
"""

class MainScreen(BoxLayout):
    current_password = StringProperty("")

    def popup_message(self, title, message):
        content = BoxLayout(orientation="vertical", padding=dp(14), spacing=dp(12))
        content.add_widget(Label(text=message, halign="center", valign="middle"))
        close_btn = Button(text="Зрозуміло", size_hint_y=None, height=dp(44))
        content.add_widget(close_btn)
        popup = Popup(title=title, content=content, size_hint=(0.86, 0.36), auto_dismiss=False)
        close_btn.bind(on_release=popup.dismiss)
        popup.open()

    def generate_password(self):
        raw_length = self.ids.length_input.text.strip()
        try:
            length = int(raw_length)
            if not 1 <= length <= 128:
                raise ValueError
        except ValueError:
            self.popup_message("Помилка", "Введіть ціле число від 1 до 128.")
            return

        sets = []
        if self.ids.lower_choice.active:
            sets.append(string.ascii_lowercase)
        if self.ids.upper_choice.active:
            sets.append(string.ascii_uppercase)
        if self.ids.digit_choice.active:
            sets.append(string.digits)
        if self.ids.symbol_choice.active:
            sets.append("!@#$%^&*()-_=+[]{};:,.?")

        if not sets:
            self.popup_message("Помилка", "Оберіть хоча б один тип символів.")
            return
        if length < len(sets):
            self.popup_message("Помилка", "Довжина має бути не меншою за кількість вибраних типів символів.")
            return

        chars = [secrets.choice(char_set) for char_set in sets]
        all_chars = "".join(sets)
        while len(chars) < length:
            chars.append(secrets.choice(all_chars))
        secrets.SystemRandom().shuffle(chars)

        self.current_password = "".join(chars)
        self.ids.result_input.text = self.current_password

    def copy_password(self):
        if not self.current_password:
            self.popup_message("Увага", "Спочатку згенеруйте пароль.")
            return
        Clipboard.copy(self.current_password)
        self.popup_message("Готово", "Пароль скопійовано.")

    def history_path(self):
        return Path(App.get_running_app().user_data_dir) / "password_history.txt"

    def save_password(self):
        if not self.current_password:
            self.popup_message("Увага", "Спочатку згенеруйте пароль.")
            return
        try:
            path = self.history_path()
            with path.open("a", encoding="utf-8") as file:
                file.write(f"{datetime.now():%d.%m.%Y %H:%M:%S} | {self.current_password}\\n")
            self.popup_message("Збережено", "Пароль додано до локальної історії.")
        except OSError as error:
            self.popup_message("Помилка збереження", str(error))

    def show_history(self):
        path = self.history_path()
        try:
            history = path.read_text(encoding="utf-8") if path.exists() else "Історія поки порожня."
        except OSError:
            history = "Не вдалося прочитати файл історії."

        layout = BoxLayout(orientation="vertical", padding=dp(10), spacing=dp(8))
        scroll = ScrollView()
        label = Label(text=history, size_hint_y=None, halign="left", valign="top")
        label.bind(texture_size=lambda instance, value: setattr(instance, "height", value[1]))
        scroll.add_widget(label)
        layout.add_widget(scroll)
        close_btn = Button(text="Закрити", size_hint_y=None, height=dp(44))
        layout.add_widget(close_btn)
        popup = Popup(title="Історія паролів", content=layout, size_hint=(0.92, 0.75))
        close_btn.bind(on_release=popup.dismiss)
        popup.open()


class PasswordGeneratorApp(App):
    def build(self):
        Builder.load_string(KV)
        self.title = "SAD1ST Password Generator"
        return MainScreen()


if __name__ == "__main__":
    PasswordGeneratorApp().run()
