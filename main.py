"""
Mini Web IDE - Flet ile tamamen Python'la yazılmış mobil HTML/CSS/JS editörü
Kod yazma alanı ÜSTTE, canlı önizleme ALTTA.
APK'ye derlemek için: flet build apk   (aşağıdaki talimatlara bak)
"""

import flet as ft
import flet_webview as fwv

DEFAULT_HTML = """<h1>Merhaba Dünya 👋</h1>
<p>Yukarıdan HTML, CSS, JS sekmelerini düzenle.</p>
<button onclick="tikla()">Bana Tıkla</button>
<p id="cikti"></p>"""

DEFAULT_CSS = """body{
  font-family: sans-serif;
  text-align: center;
  padding: 30px;
  background: #f5f5f5;
}
h1{ color:#6c5ce7; }
button{
  padding:10px 20px;
  border:none;
  border-radius:8px;
  background:#6c5ce7;
  color:#fff;
  font-size:14px;
}"""

DEFAULT_JS = """function tikla(){
  document.getElementById('cikti').innerText = 'JS calisiyor! ' + new Date().toLocaleTimeString();
}"""


def main(page: ft.Page):
    page.title = "Mini Web IDE"
    page.padding = 0
    page.spacing = 0
    page.theme_mode = ft.ThemeMode.DARK
    page.bgcolor = "#1e1e2e"

    mono = ft.TextStyle(font_family="Consolas, monospace", size=13)

    html_field = ft.TextField(
        value=DEFAULT_HTML, multiline=True, expand=True, min_lines=1000,
        text_style=mono, border=ft.InputBorder.NONE,
        bgcolor="#181825", color="#f38ba8", cursor_color="#89b4fa",
    )
    css_field = ft.TextField(
        value=DEFAULT_CSS, multiline=True, expand=True, min_lines=1000,
        text_style=mono, border=ft.InputBorder.NONE,
        bgcolor="#181825", color="#89b4fa", cursor_color="#89b4fa",
    )
    js_field = ft.TextField(
        value=DEFAULT_JS, multiline=True, expand=True, min_lines=1000,
        text_style=mono, border=ft.InputBorder.NONE,
        bgcolor="#181825", color="#f9e2af", cursor_color="#89b4fa",
    )

    status_text = ft.Text("hazir", size=11, color="#888")

    webview = fwv.WebView(expand=True, bgcolor="#ffffff")

    def build_doc() -> str:
        return f"""<!DOCTYPE html>
<html><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<style>{css_field.value}</style>
</head><body>
{html_field.value}
<script>{js_field.value}</script>
</body></html>"""

    def run_code(e=None):
        webview.load_html(build_doc())
        status_text.value = "calistirildi ✓"
        page.update()

    def reset_code(e):
        html_field.value = DEFAULT_HTML
        css_field.value = DEFAULT_CSS
        js_field.value = DEFAULT_JS
        page.update()
        run_code()

    tabs = ft.Tabs(
        selected_index=0,
        animation_duration=150,
        tabs=[
            ft.Tab(text="HTML", content=ft.Container(html_field, expand=True, padding=5)),
            ft.Tab(text="CSS", content=ft.Container(css_field, expand=True, padding=5)),
            ft.Tab(text="JS", content=ft.Container(js_field, expand=True, padding=5)),
        ],
        expand=True,
    )

    top_bar = ft.Container(
        padding=ft.padding.symmetric(horizontal=12, vertical=8),
        bgcolor="#181825",
        content=ft.Row(
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            controls=[
                ft.Text("⚡ Mini Web IDE", size=16, weight=ft.FontWeight.BOLD, color="#89b4fa"),
                ft.Row(spacing=4, controls=[
                    ft.IconButton(icon=ft.Icons.PLAY_ARROW_ROUNDED, tooltip="Calistir",
                                  icon_color="#a6e3a1", on_click=run_code),
                    ft.IconButton(icon=ft.Icons.REFRESH_ROUNDED, tooltip="Sifirla",
                                  icon_color="#f38ba8", on_click=reset_code),
                ]),
            ],
        ),
    )

    preview_bar = ft.Container(
        padding=ft.padding.only(left=12, right=12, top=4, bottom=4),
        bgcolor="#181825",
        content=ft.Row(
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            controls=[
                ft.Text("Canli Onizleme", size=11, color="#888"),
                status_text,
            ],
        ),
    )

    page.add(
        ft.Column(
            expand=True,
            spacing=0,
            controls=[
                top_bar,
                ft.Container(content=tabs, expand=1),  # ÜST: kod yazma alani
                ft.Container(height=1, bgcolor="#313244"),
                preview_bar,
                ft.Container(content=webview, expand=1),  # ALT: canli onizleme
            ],
        )
    )

    run_code()


ft.run(main)
