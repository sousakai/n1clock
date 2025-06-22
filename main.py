from kivy.app import App  # Importa a classe base para o app Kivy
from kivy.uix.boxlayout import BoxLayout  # Layout que organiza widgets em caixa (vertical/horizontal)
from kivy.uix.label import Label  # Widget para mostrar texto na tela
from kivy.uix.textinput import TextInput  # Widget para entrada de texto
from kivy.uix.button import Button  # Widget botão clicável
from kivy.graphics import Color, Rectangle  # Para desenhar o fundo colorido
from plyer import notification  # Biblioteca que permite notificação local no sistema

from logica import calcularSaida  # Função externa que calcula o horário de saída


class N1ClockLayout(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)  # Inicializa o BoxLayout pai

        # Define que os widgets serão organizados verticalmente
        self.orientation = 'vertical'
        self.padding = 20  # Espaço interno entre borda e widgets
        self.spacing = 20  # Espaço entre os widgets

        # --- COR DE FUNDO (para evitar tela preta) ---
        with self.canvas.before:
            Color(0, 0, 0, 0)  # Define a cor (RGBA)
            self.rect = Rectangle(size=self.size, pos=self.pos)  # Desenha um retângulo do tamanho do layout

        # Atualiza o retângulo caso o tamanho ou posição mudem (redimensionamento de janela)
        self.bind(size=self._update_rect, pos=self._update_rect)

        # --- CRIA OS WIDGETS ---

        # Label com instrução
        self.label = Label(text='Cálculo de saída')
        self.label = Label(text='Digite o horário de entrada (HH:MM):')
        self.add_widget(self.label)  # Adiciona a label no layout

        # Campo para digitar o horário de entrada
        self.input_hora = TextInput(multiline=False, hint_text='08:00')
        self.add_widget(self.input_hora)

        # Botão para disparar o cálculo
        self.btn_calcular = Button(text='Calcular horário de saída')
        self.btn_calcular.bind(on_press=self.calcular_saida)  # Liga o clique do botão à função calcular_saida
        self.add_widget(self.btn_calcular)

        # Label para mostrar o resultado do cálculo
        self.resultado = Label(text='')
        self.add_widget(self.resultado)

        # --- BOTÃO DE TESTE DE NOTIFICAÇÃO ---
        self.btn_notificacao = Button(text='Testar notificação')
        self.btn_notificacao.bind(on_press=self.enviar_notificacao)
        self.add_widget(self.btn_notificacao)

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
        Aqui, retorna a nossa tela principal N1ClockLayout.
        """
        return N1ClockLayout()


if __name__ == '__main__':
    N1ClockApp().run()  # Inicia o loop principal do app Kivy
