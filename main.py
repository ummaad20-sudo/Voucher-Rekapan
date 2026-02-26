from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.filechooser import FileChooserListView
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.popup import Popup
from kivy.graphics import Rectangle, Color, Ellipse, Line
from kivy.graphics.texture import Texture
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.utils import platform
from collections import defaultdict
from datetime import datetime
from openpyxl import load_workbook
import os
import random


class ClickableLabel(Label):
    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            if self.text.strip() != "":
                from kivy.core.clipboard import Clipboard
                Clipboard.copy(self.text)
                App.get_running_app().show_notif("Hasil berhasil dicopy!")
            return True
        return super().on_touch_down(touch)


class RekapApp(App):

    # ===============================
    # BUAT TEXTURE GRADIENT ORANGE + BLUE
    # ===============================
    def create_gradient(self, width, height):
        texture = Texture.create(size=(1, height), colorfmt='rgba')
        buf = []

        for y in range(height):
            t = y / float(height)

            # Blend orange ke biru
            r = int((1 - t) * 255 + t * 0)
            g = int((1 - t) * 120 + t * 80)
            b = int((1 - t) * 0 + t * 255)
            a = 255

            buf.extend([r, g, b, a])

        buf = bytes(buf)
        texture.blit_buffer(buf, colorfmt='rgba', bufferfmt='ubyte')
        texture.wrap = 'repeat'
        texture.uvsize = (width, -1)

        return texture

    # ===============================
    def build(self):
        self.hasil_text = ""

        self.layout = BoxLayout(
            orientation='vertical',
            padding=15,
            spacing=15
        )

        with self.layout.canvas.before:

            # GRADIENT HALUS ORANGE-BLUE
            self.gradient_texture = self.create_gradient(
                Window.width,
                Window.height
            )

            self.bg = Rectangle(
                texture=self.gradient_texture,
                size=Window.size,
                pos=(0, 0)
            )

            # Overlay gelap tipis
            Color(0, 0, 0, 0.15)
            self.overlay = Rectangle(size=Window.size, pos=(0, 0))

            # Lingkaran transparan
            for _ in range(18):
                Color(1, 1, 1, 0.05)
                Ellipse(
                    pos=(random.randint(0, Window.width),
                         random.randint(0, Window.height)),
                    size=(random.randint(80, 250),
                          random.randint(80, 250))
                )

            # Segitiga outline
            for _ in range(12):
                Color(1, 1, 1, 0.25)
                x = random.randint(0, Window.width)
                y = random.randint(0, Window.height)
                size = random.randint(60, 160)

                Line(points=[
                    x, y,
                    x + size, y,
                    x + size/2, y + size,
                    x, y
                ], width=1.2)

            # Kotak outline
            for _ in range(12):
                Color(1, 1, 1, 0.2)
                Line(
                    rectangle=(
                        random.randint(0, Window.width),
                        random.randint(0, Window.height),
                        random.randint(60, 180),
                        random.randint(60, 180)
                    ),
                    width=1
                )

        self.layout.bind(size=self.update_bg)

        # HEADER
        self.header = Label(
            text="[b]REKAPAN VOUCHER PENJUALAN[/b]",
            markup=True,
            font_size=35,
            size_hint=(1, 0.1),
            color=(1, 1, 1, 1)
        )
        self.layout.add_widget(self.header)

        # HASIL
        self.result_label = ClickableLabel(
            text="MASUKAN FILE PENJUALAN",
            markup=True,
            size_hint_y=None,
            color=(1, 1, 1, 1)
        )
        self.result_label.bind(texture_size=self.result_label.setter('size'))

        scroll = ScrollView(size_hint=(1, 0.6))
        scroll.add_widget(self.result_label)
        self.layout.add_widget(scroll)

        # SHARE
        self.btn_share = Button(
            text="SHARE HASIL REKAPAN",
            size_hint=(1, 0.1),
            background_color=(0.1, 0.5, 0.8, 1)
        )
        self.btn_share.bind(on_press=self.share_hasil)
        self.layout.add_widget(self.btn_share)

        # PILIH FILE
        self.btn_file = Button(
            text="PILIH FILE EXCEL",
            size_hint=(1, 0.1),
            background_color=(0.2, 0.7, 0.4, 1)
        )
        self.btn_file.bind(on_press=self.buka_file)
        self.layout.add_widget(self.btn_file)

        # NOTIF
        self.notif = Label(
            text="",
            size_hint=(1, 0.05),
            color=(1, 1, 0, 1)
        )
        self.layout.add_widget(self.notif)

        # CREATOR
        self.creator = Label(
            text="creator by JUN.AI © 2026",
            size_hint=(1, 0.05),
            font_size=25,
            color=(0.9, 0.9, 0.9, 1)
        )
        self.layout.add_widget(self.creator)

        return self.layout

    # ===============================
    def update_bg(self, *args):
        self.bg.size = Window.size
        self.overlay.size = Window.size

    # ===============================
    def show_notif(self, text):
        self.notif.text = text
        Clock.schedule_once(self.clear_notif, 2)

    def clear_notif(self, dt):
        self.notif.text = ""

    # ===============================
    def buka_file(self, instance):
        content = FileChooserListView(
            path="/storage/emulated/0/",
            filters=["*.xlsx"]
        )

        popup = Popup(
            title="Pilih File Excel",
            content=content,
            size_hint=(0.95, 0.95)
        )

        content.bind(
            on_submit=lambda chooser, selection, touch:
            self.proses_file(selection, popup)
        )

        popup.open()

    # ===============================
    def proses_file(self, selection, popup):
        if not selection:
            return

        file_path = selection[0]
        popup.dismiss()

        try:
            wb = load_workbook(file_path, data_only=True)
            sheet = wb.active
        except:
            self.result_label.text = "[color=ff4444]Gagal membuka file![/color]"
            return

        rekap_detail = defaultdict(lambda: {"jumlah": 0, "total": 0})
        rekap_tanggal = defaultdict(int)

        header = [str(cell.value).strip() for cell in sheet[1]]

        try:
            kolom_grup = header.index("Grup pengguna")
            kolom_harga = header.index("Harga")
            kolom_tanggal = header.index("Diaktifkan di")
        except:
            self.result_label.text = "[color=ff4444]Header tidak sesuai![/color]"
            return

        for row in sheet.iter_rows(min_row=2, values_only=True):
            try:
                grup = row[kolom_grup]
                harga = row[kolom_harga]
                tanggal_full = row[kolom_tanggal]

                if not (grup and harga and tanggal_full):
                    continue

                if isinstance(tanggal_full, datetime):
                    tanggal = tanggal_full.strftime("%Y/%m/%d")
                else:
                    tanggal = str(tanggal_full).split(" ")[0]

                harga_int = int(float(harga))

                key = (tanggal, grup)
                rekap_detail[key]["jumlah"] += 1
                rekap_detail[key]["total"] += harga_int
                rekap_tanggal[tanggal] += harga_int

            except:
                continue

        hasil = "[b]===== HASIL REKAP =====[/b]\n\n"
        tanggal_terakhir = None

        for (tanggal, grup), data in sorted(rekap_detail.items()):
            if tanggal_terakhir and tanggal != tanggal_terakhir:
                hasil += f"[color=FFA500]>>> TOTAL {tanggal_terakhir} : Rp {rekap_tanggal[tanggal_terakhir]}[/color]\n"
                hasil += "-----------------------------\n"

            if tanggal != tanggal_terakhir:
                hasil += f"\n[b]Tanggal : {tanggal}[/b]\n"

            hasil += f"  Grup   : {grup}\n"
            hasil += f"  Jumlah : {data['jumlah']}\n"
            hasil += f"  Total  : Rp {data['total']}\n\n"

            tanggal_terakhir = tanggal

        if tanggal_terakhir:
            hasil += f"[color=FFA500]>>> TOTAL {tanggal_terakhir} : Rp {rekap_tanggal[tanggal_terakhir]}[/color]\n"

        self.hasil_text = hasil
        self.result_label.text = hasil

    # ===============================
    def share_hasil(self, instance):
        if not self.hasil_text:
            self.show_notif("Belum ada hasil!")
            return

        file_path = "/storage/emulated/0/hasil_rekap.txt"

        try:
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(self.hasil_text)

            if platform == "android":
                from plyer import share
                share.share(file_path)

            self.show_notif("File berhasil dibuat & dishare!")

        except:
            self.show_notif("Gagal membuat file!")


if __name__ == "__main__":
    RekapApp().run()
