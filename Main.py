import os
import threading
import requests
import pandas as pd
from datetime import datetime

from kivy.app import App
from kivy.clock import Clock
from kivy.metrics import dp
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import StringProperty
from kivymd.app import MDApp
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.filemanager import MDFileManager
from kivymd.toast import toast

# ================= CONFIG =================
REYEE_API_URL = "https://example.com/api"  # GANTI
REYEE_TOKEN = "YOUR_TOKEN"                 # GANTI

# ================= HELPER =================
def format_rupiah(value):
    try:
        return "Rp {:,.0f}".format(value).replace(",", ".")
    except:
        return "Rp 0"

# ================= UI =================
class GlassCard(MDCard):
    pass


class MainLayout(BoxLayout):
    total_text = StringProperty("Rp 0")
    tanggal_text = StringProperty("-")

    def __init__(self, **kwargs):
        super().__init__(orientation="vertical", spacing=dp(12), padding=dp(12), **kwargs)

        self.file_manager = MDFileManager(
            exit_manager=self.close_file_manager,
            select_path=self.select_path,
        )

        self.card = GlassCard(
            radius=[20],
            elevation=3,
            padding=dp(16),
            md_bg_color=(1, 1, 1, 0.15),
        )

        self.label_tanggal = MDLabel(
            text="Tanggal: -",
            halign="center",
            theme_text_color="Primary",
        )

        self.label_total = MDLabel(
            text="Total: Rp 0",
            halign="center",
            font_style="H5",
        )

        self.btn_pick = MDRaisedButton(
            text="PILIH FILE EXCEL",
            pos_hint={"center_x": 0.5},
            on_release=lambda x: self.open_file_manager(),
        )

        self.card.add_widget(self.label_tanggal)
        self.card.add_widget(self.label_total)

        self.add_widget(self.card)
        self.add_widget(self.btn_pick)

    # ================= FILE =================
    def open_file_manager(self):
        self.file_manager.show("/storage/emulated/0")

    def close_file_manager(self, *args):
        self.file_manager.close()

    def select_path(self, path):
        self.close_file_manager()
        threading.Thread(target=self.process_excel, args=(path,), daemon=True).start()

    # ================= PROCESS =================
    def process_excel(self, path):
        try:
            df = pd.read_excel(path)

            if "E" not in df.columns and len(df.columns) >= 5:
                harga_col = df.columns[4]
            else:
                harga_col = "E"

            if "L" not in df.columns and len(df.columns) >= 12:
                tanggal_col = df.columns[11]
            else:
                tanggal_col = "L"

            total = df[harga_col].fillna(0).sum()

            today = datetime.now().strftime("%d-%m-%Y")

            Clock.schedule_once(lambda dt: self.update_ui(total, today))
            threading.Thread(target=self.send_to_reyee, args=(total, today), daemon=True).start()

        except Exception as e:
            Clock.schedule_once(lambda dt: toast(f"Error: {e}"))

    def update_ui(self, total, tanggal):
        self.label_total.text = f"Total: {format_rupiah(total)}"
        self.label_tanggal.text = f"Tanggal: {tanggal}"

    # ================= REYEE =================
    def send_to_reyee(self, total, tanggal):
        try:
            headers = {"Authorization": f"Bearer {REYEE_TOKEN}"}
            data = {"tanggal": tanggal, "total": total}
            requests.post(REYEE_API_URL, json=data, headers=headers, timeout=10)
        except:
            pass


# ================= APP =================
class VoucherApp(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Blue"
        return MainLayout()


if __name__ == "__main__":
    VoucherApp().run()
