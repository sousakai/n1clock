from kivy.app import App  # Importa a classe base para o app Kivy
from kivy.uix.boxlayout import BoxLayout  # Layout que organiza widgets em caixa (vertical/horizontal)
from kivy.uix.label import Label  # Widget para mostrar texto na tela
from kivy.uix.textinput import TextInput  # Widget para entrada de texto
from kivy.uix.button import Button  # Widget botão clicável
from kivy.graphics import Color, Rectangle  # Para desenhar o fundo colorido
from plyer import notification  # Biblioteca que permite notificação local no sistema

from kivy.uix.floatlayout import FloatLayout  # Layout que permite posicionamento absoluto e por porcentagem
from kivy.uix.widget import Widget  # Usado para inserir espaçadores invisíveis
from kivy.core.text import LabelBase  # Usado para registrar fontes personalizadas

from logica import calcularSaida  # Função externa que calcula o horário de saída

# exemplo de uso de labelbase, necessita fazer o download do arquivo e especificar o caminho fonte
# LabelBase.register(name='Roboto', fn_regular='fonts/Roboto-Regular.ttf')
# font_name='Roboto'

class N1ClockLayout(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)  # Inicializa o BoxLayout pai

        # Define que os widgets serão organizados verticalmente
        self.orientation = 'vertical'
        self.padding = 20  # Define margem interna ao redor de todo o layout
        self.spacing = 20  # Define o espaço vertical entre os widgets (PODE ALTERAR AQUI)
        self.size_hint = (0.9, None)  # Largura relativa à tela (90%), altura fixa
        self.height = self.minimum_height  # Ajusta altura com base no conteúdo
        self.pos_hint = {'center_x': 0.5, 'center_y': 0.5}  # Centraliza o layout na tela

        # --- COR DE FUNDO (para evitar tela preta) ---
        with self.canvas.before:
            Color(0, 0, 0, 0)  # Define a cor de fundo transparente
            self.rect = Rectangle(size=self.size, pos=self.pos)  # Desenha o fundo

        # Atualiza retângulo ao redimensionar
        self.bind(size=self._update_rect, pos=self._update_rect)

        # --- CRIA OS WIDGETS ---

        # Label com instrução
        self.label_titulo = Label(text="[b]N1Clock \n    0.15[/b]",
                                  markup=True,
                                  font_size=24)  # Fonte maior para o título
        self.add_widget(self.label_titulo)

        # --- Espaçamento adicional abaixo do título ---
        self.add_widget(Widget(size_hint_y=None, height=10))  # AUMENTE O "height" AQUI para mais espaçamento

        self.label = Label(text='Digite o horário de entrada (HH:MM):', font_size=18)
        self.add_widget(self.label)

        # Campo para digitar o horário de entrada
        self.input_hora = TextInput(
            multiline=False,
            hint_text='08:00',
            font_size=18,
            size_hint_y=None,  # altura fixa para melhor visual
            height=40,
            size_hint_x=None,
            width=500,  # Largura do campo de texto
            pos_hint={"center_x": 0.5}  # Centraliza horizontalmente
        )
        self.add_widget(self.input_hora)

        # Botão para disparar o cálculo
        self.btn_calcular = Button(
            text='Calcular horário de saída',
            size_hint_y=None,  # altura fixa para uniformidade
            height=70,
            size_hint_x=None,
            width=300,
            font_size=16,
            pos_hint={"center_x": 0.5}
        )
        self.btn_calcular.bind(on_press=self.calcular_saida)  # Liga o clique do botão à função calcular_saida
        self.add_widget(self.btn_calcular)

        # Label para mostrar o resultado do cálculo
        self.resultado = Label(text='', font_size=18)  # Fonte maior para resultado
        self.add_widget(self.resultado)

        # --- BOTÃO DE TESTE DE NOTIFICAÇÃO ---
        self.btn_notificacao = Button(
            text='Testar notificação',
            size_hint=(0.4, None),  # 40% da largura, altura fixa para deixar menor
            height=35,
            font_size=14,
            pos_hint={"center_x": 0.5}  # centralizado horizontalmente
        )
        self.btn_notificacao.bind(on_press=self.enviar_notificacao)
        self.add_widget(self.btn_notificacao)

        # rodapé
        self.rodape = Label(text='Kayke @ 2025', font_size=15)
        self.add_widget(self.rodape)

    def _update_rect(self, instance, value):
        """
        Atualiza a posição e tamanho do retângulo de fundo quando a janela muda.
        """
        self.rect.pos = instance.pos
        self.rect.size = instance.size

    def calcular_saida(self, instance):
        # Essa função é chamada quando o botão é pressionado (evento on_press)
        print("Botão clicado")  # Debug: confirma que a função foi disparada

        entrada_str = self.input_hora.text  # Pega o texto digitado no campo de entrada

        resultado = calcularSaida(entrada_str)
        # Chama a função da lógica que retorna uma tupla (entrada_formatada, saida_formatada)
        # ou None caso o formato seja inválido

        if resultado:
            # Se resultado não for None, desempacota a tupla
            entrada, saida = resultado

            # Atualiza o label com o horário de saída formatado
            self.resultado.text = f"Horário de saída: {saida}"
        else:
            # Se a função retornou None, mostra mensagem de erro para o usuário
            self.resultado.text = "Formato inválido! Use HH:MM."

    def enviar_notificacao(self, instance):
        """
        Essa função é chamada quando o botão de notificação é clicado.
        Usa a biblioteca plyer para disparar uma notificação local.
        """
        notification.notify(
            title='N1Clock',
            message='Notificação de teste funcionando!',
        )

class N1ClockApp(App):
    def build(self):
        """
        Método obrigatório da classe App.
        Deve retornar o widget raiz da interface, que será mostrado na tela.
        Aqui, retorna a nossa tela principal N1ClockLayout, centralizada.
        """
        root = FloatLayout()  # Cria o layout de fundo principal
        layout_central = N1ClockLayout()  # Instancia nosso layout customizado
        root.add_widget(layout_central)  # Adiciona ao centro da tela
        return root

if __name__ == '__main__':
    N1ClockApp().run()  # Inicia o loop principal do app Kivy
