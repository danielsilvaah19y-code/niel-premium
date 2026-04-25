import ssl
from kivy.config import Config

# Configura o app para ser redimensionável
Config.set('graphics', 'resizable', '1')

import webbrowser
from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.toolbar import MDTopAppBar
from kivymd.uix.textfield import MDTextField
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDRaisedButton, MDIconButton
from kivymd.uix.dialog import MDDialog
from kivy.metrics import dp
from kivy.utils import platform

# Ignora erros de SSL para garantir que os links carreguem sempre
ssl._create_default_https_context = ssl._create_unverified_context

class NielIPTVApp(MDApp):
    dialogo = None
    
    # BANCO DE DADOS - Canais e Novela (Links Reais)
    CONTEUDO = [
        {"nome": "TRÊS GRAÇAS (INÍCIO)", "icon": "numeric-1-box-outline", "link": "https://globo.com"},
        {"nome": "TRÊS GRAÇAS (HOJE)", "icon": "update", "link": "https://globo.com"},
        {"nome": "GLOBO AO VIVO", "icon": "television-classic", "link": "https://globo.com"},
        {"nome": "SBT AO VIVO", "icon": "television-guide", "link": "https://sbt.com.br"},
        {"nome": "RECORD TV", "icon": "television-play", "link": "https://r7.com"},
        {"nome": "PLUTO TV FILMES", "icon": "movie-open", "link": "http://pluto.tv"},
        {"nome": "PLUTO TV SÉRIES", "icon": "youtube-tv", "link": "http://pluto.tv"},
        {"nome": "PLUTO TV RETRÔ", "icon": "history", "link": "http://pluto.tv"},
    ]

    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Red"
        self.tela_principal = MDScreen()
        self.exibir_lista()
        return self.tela_principal

    def exibir_lista(self, texto=""):
        self.tela_principal.clear_widgets()
        layout_fundo = MDBoxLayout(orientation='vertical')
        
        barra = MDTopAppBar(title="Niel IPTV GRATIS", elevation=10)
        layout_fundo.add_widget(barra)
        
        layout_busca = MDBoxLayout(size_hint_y=None, height=dp(80), padding=dp(15))
        self.busca = MDTextField(
            hint_text="Buscar novela ou canais...",
            mode="round",
            size_hint_x=0.85,
            pos_hint={"center_x": 0.5}
        )
        self.busca.bind(text=lambda instance, value: self.filtrar_busca(value))
        layout_busca.add_widget(self.busca)
        layout_fundo.add_widget(layout_busca)
        
        scroll = MDScrollView()
        self.grade = MDGridLayout(cols=2, adaptive_height=True, padding=dp(20), spacing=dp(20))
        self.atualizar_grid(texto)

        scroll.add_widget(self.grade)
        layout_fundo.add_widget(scroll)
        self.tela_principal.add_widget(layout_fundo)

    def atualizar_grid(self, filtro=""):
        self.grade.clear_widgets()
        for item in self.CONTEUDO:
            if filtro.lower() in item['nome'].lower():
                card = MDCard(
                    orientation='vertical', size_hint=(None, None), size=(dp(150), dp(180)),
                    radius=[20,], elevation=4, ripple_behavior=True,
                    on_release=lambda x, i=item: self.confirmar_play(i)
                )
                icone = MDIconButton(
                    icon=item['icon'], icon_size="70dp", pos_hint={"center_x": .5},
                    theme_text_color="Custom", text_color=self.theme_cls.primary_color
                )
                label = MDLabel(text=item['nome'], halign="center", bold=True, theme_text_color="Primary")
                card.add_widget(icone)
                card.add_widget(label)
                self.grade.add_widget(card)

    def filtrar_busca(self, texto):
        self.atualizar_grid(texto)

    def confirmar_play(self, item):
        self.dialogo = MDDialog(
            title=f"Abrir {item['nome']}?",
            text="Deseja assistir agora?",
            buttons=[
                MDRaisedButton(text="VOLTAR", on_release=lambda x: self.dialogo.dismiss()),
                MDRaisedButton(text="ASSISTIR", on_release=lambda x, u=item['link']: self.abrir_no_player(u)),
            ],
        )
        self.dialogo.open()

    def abrir_no_player(self, url):
        if self.dialogo: self.dialogo.dismiss()
        if platform == 'android':
            try:
                from jnius import autoclass, cast
                PythonActivity = autoclass('org.kivy.android.PythonActivity')
                Intent = autoclass('android.content.Intent')
                Uri = autoclass('android.net.Uri')
                intent = Intent(Intent.ACTION_VIEW)
                intent.setDataAndType(Uri.parse(url), "video/*")
                intent.addFlags(Intent.FLAG_ACTIVITY_NEW_TASK)
                current_activity = cast('android.app.Activity', PythonActivity.mActivity)
                current_activity.startActivity(intent)
            except: webbrowser.open(url)
        else: webbrowser.open(url)

if __name__ == "__main__":
    NielIPTVApp().run()
