from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.filechooser import FileChooserListView
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.popup import Popup
from kivy.graphics import Rectangle, Color, Line, Ellipse
from kivy.core.window import Window
from kivy.core.clipboard import Clipboard
from kivy.clock import Clock
from openpyxl import load_workbook
from collections import defaultdict
from datetime import datetime
import os


class ClickableLabel(Label):
    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            if self.text.strip() != "":
                Clipboard.copy(self.text)
                App.get_running_app().show_notif("Hasil berhasil dicopy!")
            return True
        return super().on_touch_down(touch)


class RekapApp(App):

    def build(self):

        self.layout = BoxLayout(
            orientation='vertical',
            padding=15,
            spacing=15
        )

        with self.layout.canvas.before:

            # ===== Background Gelap =====
            Color(0.05, 0.05, 0.07, 1)
            self.bg = Rectangle(size=Window.size, pos=self.layout.pos)

            # ===== Garis Orange Atas =====
            Color(1, 0.25, 0, 1)
            self.top_bar = Rectangle(
                size=(Window.width, 25),
                pos=(0, Window.height - 25)
            )

            # ===== Bulatan Modern =====
            Color(1, 0.4, 0, 0.08)
            Ellipse(pos=(50, Window.height - 300), size=(250, 250))
            Ellipse(pos=(Window.width - 300, 80), size=(220, 220))

            # ===== Lingkaran Outline =====
            Color(1, 0.5, 0.3, 0.4)
            Line(circle=(Window.width * 0.8, Window.height * 0.7, 120), width=1.2)
            Line(circle=(Window.width * 0.2, Window.height * 0.3, 80), width=1)

            # ===== Segitiga Modern =====
            Color(1, 0.4, 0.2, 0.5)
            Line(points=[
                100, 150,
                200, 300,
                20, 300,
                100, 150
            ], width=1)

            Line(points=[
                Window.width - 150, Window.height - 200,
                Window.width - 50, Window.height - 100,
                Window.width - 250, Window.height - 100,
                Window.width - 150, Window.height - 200
            ], width=1)

            # ===== Kotak Modern =====
            Color(1, 0.3, 0.1, 0.3)
            Line(rectangle=(60, 60, 120, 120), width=1)
            Line(rectangle=(Window.width - 200, Window.height - 350, 150, 150), width=1)

        self.layout.bind(size=self.update_bg)

        # ===== HEADER =====
        self.label = Label(
            text="[b]REKAP DATA VOUCHER RUIJIE PRO[/b]",
            markup=True,
            font_size=20,
            size_hint=(1, 0.1),
            color=(1, 1, 1, 1)
        )
        self.layout.add_widget(self.label)

        # ===== HASIL =====
        self.result_label = ClickableLabel(
            text="Silakan pilih file Excel...",
            size_hint_y=None,
            markup=True,
            color=(1, 1, 1, 1)
        )
        self.result_label.bind(texture_size=self.result_label.setter('size'))

        scroll = ScrollView(size_hint=(1, 0.6))
        scroll.add_widget(self.result_label)
        self.layout.add_widget(scroll)

        # ===== Spacer =====
        self.layout.add_widget(Label(size_hint=(1, 0.03)))
        self.layout.add_widget(Label(size_hint=(1, 0.03)))
        self.layout.add_widget(Label(size_hint=(1, 0.03)))

        # ===== SHARE BUTTON =====
        self.btn_share = Button(
            text="Share Hasil Rekap",
            size_hint=(1, 0.1),
            background_color=(0.2, 0.6, 0.5, 1)
        )
        self.btn_share.bind(on_press=self.share_hasil)
        self.layout.add_widget(self.btn_share)

        # ===== PILIH FILE =====
        btn = Button(
            text="Pilih File Excel",
            size_hint=(1, 0.1),
            background_color=(0.2, 0.4, 0.9, 1)
        )
        btn.bind(on_press=self.buka_file)
        self.layout.add_widget(btn)

        # ===== NOTIF =====
        self.notif = Label(
            text="",
            size_hint=(1, 0.05),
            color=(1, 1, 0, 1)
        )
        self.layout.add_widget(self.notif)

        # ===== CREATOR =====
        self.creator_label = Label(
            text="creator by JUN.AI © 2026",
            size_hint=(1, 0.06),
            font_size=18,
            bold=True,
            color=(0.9, 0.9, 0.9, 1)
        )
        self.layout.add_widget(self.creator_label)

        return self.layout

    def update_bg(self, *args):
        self.bg.size = Window.size
        self.top_bar.size = (Window.width, 25)
        self.top_bar.pos = (0, Window.height - 25)

    def show_notif(self, text):
        self.notif.text = text
        Clock.schedule_once(self.clear_notif, 2)

    def clear_notif(self, dt):
        self.notif.text = ""

    def buka_file(self, instance):
        content = FileChooserListView()
        popup = Popup(
            title="Pilih File Excel",
            content=content,
            size_hint=(0.9, 0.9)
        )

        content.bind(
            on_submit=lambda x, selection, touch:
            self.proses_file(selection, popup)
        )
        popup.open()

    def proses_file(self, selection, popup):
        if not selection:
            return

        file_path = selection[0]
        popup.dismiss()

        try:
            wb = load_workbook(file_path)
            sheet = wb.active
        except:
            self.result_label.text = "[color=ff4444]Gagal membuka file![/color]"
            return

        rekap_detail = defaultdict(lambda: {"jumlah": 0, "total": 0})
        rekap_tanggal = defaultdict(int)

        header = [cell.value for cell in sheet[1]]

        try:
            kolom_grup = header.index("Grup pengguna")
            kolom_harga = header.index("Harga")
            kolom_tanggal = header.index("Diaktifkan di")
        except:
            self.result_label.text = "[color=ff4444]Header tidak sesuai![/color]"
            return

        for row in sheet.iter_rows(min_row=2, values_only=True):
            grup = row[kolom_grup]
            harga = row[kolom_harga]
            tanggal_full = row[kolom_tanggal]

            if grup and harga and tanggal_full:
                if isinstance(tanggal_full, datetime):
                    tanggal = tanggal_full.strftime("%Y/%m/%d")
                else:
                    tanggal = str(tanggal_full).split(" ")[0]

                try:
                    harga_int = int(harga)
                except:
                    continue

                key = (tanggal, grup)
                rekap_detail[key]["jumlah"] += 1
                rekap_detail[key]["total"] += harga_int
                rekap_tanggal[tanggal] += harga_int

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

    def share_hasil(self, instance):
        if not hasattr(self, "hasil_text"):
            self.show_notif("Belum ada hasil!")
            return

        file_path = os.path.join(os.getcwd(), "hasil_rekap.txt")
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(self.hasil_text)

        self.show_notif("File hasil_rekap.txt berhasil dibuat!")


if __name__ == "__main__":
    RekapApp().run()
