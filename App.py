import speech_recognition as sr
import playsound
from gtts import gTTS, tts
import random
import webbrowser
import pyttsx3
import os
import datetime
from binance.client import Client
import re
import numpy as np

class Virtual_assit():
    def __init__(self, assist_name, person):
        self.person = person
        self.assit_name = assist_name

        self.engine = pyttsx3.init()
        self.r = sr.Recognizer()
        
        self.voice_data = ''

    def engine_speak(self, text):
        """
        Fala da assitente virtual
        """
        text = str(text)
        self.engine.say(text)
        self.engine.runAndWait()

    def record_audio(self, ask=""):

        with sr.Microphone() as source:
            if ask:
                print('Ouvindo...')
                #self.engine_speak(ask)
            
            audio = self.r.listen(source, 5, 5)# pega dados de auido
            print('Salvando, informações no banco de dados')
            try:
                self.voice_data = self.r.recognize_google(audio, language="pt-BR") #converte audio para texto

            except sr.UnknownValueError:
                self.engine_speak('Desculpa, não entendi o que você disse. Por favor, pode repetir?')

            except sr.RequestError:
                self.engine_speak('Desculpe, meu servidor está inativo') # recognizer is not connected

            print(">>",self.voice_data.lower()) #imprime o que vc disse
            self.voice_data = self.voice_data.lower()

            return self.voice_data.lower()

    def engine_speak(self, audio_strig):
        audio_strig = str(audio_strig)
        tts = gTTS(text=audio_strig, lang='pt-br')
        r = random.randint(1,20000)
        audio_file = 'audio' + str(r) + '.mp3'
        tts.save(audio_file)
        playsound.playsound(audio_file)
        print(self.assit_name + ':', audio_strig)
        os.remove(audio_file)

    def there_exist(self, terms):
        """
        Função para identificar se o termo existe
        """
        for term in terms:
            if term in self.voice_data:
                return True

    def bitCoin_price(self):
        api_key = 'ftwcigvia9i20th9O0brkn15R6k7DXGvsrkDRboBsl4VEoVh5BXn6gsbXKdtmPmv'
        api_secret = 'Qc9gmDovckYI0gkrpo1ZcLa5ggn80Wy16bGC5CRUZX0vwbT7OwEq0hZYuF4Jvv7p'
        client = Client(api_key = api_key, api_secret= api_secret)
        price = round(float(client.get_ticker(symbol = 'BTCBRL')['lastPrice']), 2)
        return price
    
    def converte_aritimetica(self, conta):
        numeros = []
        regex = re.compile(r'[0-9]+')
        check = regex.findall(conta)
        for item in check:
            numeros.append(float(item))
        numeros = np.array(numeros)
        return numeros

    def respond(self, voice_data):
        #Variavel de "Curiosidade" + "Piada"
        curiosidades = [
        "Existem mais formas de vida vivendo na sua pele do que humanos habitando a Terra. Esta, certamente, é uma das curiosidades do mundo mais impactantes.",
        "Em média, cada pessoa perde 4kg de pele morta em um ano",
        "Charles Osborne teve uma crise de soluços que durou, nada mais nada menos que, 69 anos. Começou em 1922, quando pesava um cerdo para sacrificá-lo e só parou quando ele já tinha 97 anos.",
        "Todas as pessoas que têm olhos azuis têm um mesmo ancestral em comum.",
        "O cérebro é um órgão extraordinário. Isso porque comanda todo o organismo humano. Além disso, é o único que não pode sentir dor.",
        "Geralmente, 30% do sangue bombeado pelo coração vai direto para o cérebro.",
        "A decomposição do corpo humano começa apenas 4 minutos depois da morte.",
        "Respirar pela boca o tempo todo pode causar cáries e modificar o formato da mandíbula.Uma das curiosidades do mundo mais chocantes, hein?",
        "Quando você fala para si mesmo, por exemplo, enquanto lê, essa ‘voz’ interior é acompanhada de movimentos muito sutis da laringe.",
        "Beijar um bebê na orelha pode deixá-lo surdo."]

        piadas = [
        "Por que os fantasmas são péssimos para contar mentiras?....... Porque são transparentes.",
        "Por que a plantinha não foi atendida no hospital?....... Porque só tinha médico de plantão.",
        "O que a Lua disse ao Sol?....... – Nossa, você é tão grande e ainda não te deixam sair à noite!",
        "Eu perdi peso no mês passado....... Mas este mês ele já me encontrou de novo.",
        "Sabe qual é a melhor forma de consumir o tempo?....... Comer relógios.",
        "Você sabe por que a água foi presa?....... - Porque ela matou a sede.",
        "Qual a cidade brasileira que não tem táxi?....... Uberlândia.",
        "Qual a fórmula da água benta?....... H Deus O.",
        "Qual o contrário de papelada?....... Pá vestida.",
        "Contei uma piada química....... não teve reação.",]

        # Comprimento Inicial
        if self.there_exist(['hey', 'hi', 'hello', 'oi', 'holla', 'aila', 'oi aila']):
            greetigns = [f'Hi {self.person}, O que deseja fazer hoje?',
                        'Oi chefe, como posso te ajudar?',
                        'Olá chefe, o que precisa?']

            greet = greetigns[random.randint(0,len(greetigns)-1)]
            self.engine_speak(greet)

        #Situação da assistente
        if self.there_exist(['como você está', 'como voce esta', 'tudo bem']):
            greetigns = [f'Hi {self.person}, Estou ótima, obrigado por perguntar',
                        'Estou entediada, por favor me tire do tedio',
                        'Estou triste, você me esqueceu']

            greet = greetigns[random.randint(0,len(greetigns)-1)]
            self.engine_speak(greet)

        #Pesquisa no Google
        if self.there_exist(['pesquise']) and 'youtube' not in voice_data:
            search_term = voice_data.split("procure")[-1]
            url =  "http://google.com/search?q=" + search_term
            webbrowser.get().open(url)
            self.engine_speak("Aqui está o que eu encontrei para " + search_term + 'on google')

        #Pesquisa no Youtube
        if self.there_exist(["procurar no youtube"]):
            search_term  = voice_data.split("procurar no")[-1]
            url = "http://www.youtube.com/results?search_query=" + search_term
            webbrowser.get().open(url)
            self.engine_speak("Aqui está o que eu encontrei para" + search_term + 'on youtube')
            
        #Falar as Horas
        if self.there_exist(['que horas são']):
            hora = datetime.datetime.now().strftime('%H:%M')
            self.engine.runAndWait()
            self.engine_speak("Agora são" + hora)
            
        #Contar uma Curiosidade
        if self.there_exist(['conte uma curiosidade']):
            self.engine.runAndWait()
            self.engine_speak(random.choice(curiosidades))
        
        #Contar uma Piada
        if self.there_exist(['conte uma piada']):
            self.engine.runAndWait()
            self.engine_speak(random.choice(piadas))
            
        #Bitcoin
        if self.there_exist(['preço do bitcoin']):
            self.engine.runAndWait()
            self.engine_speak(f'o preço do bitcoin é de {self.bitCoin_price()} reais')
            
        #Calculos de matematica
        if self.there_exist(['faça uma conta de adição']):
            self.engine.runAndWait()
            self.engine_speak('O que voce quer somar')
            self.engine.runAndWait()
            voice_data = assistent.record_audio()
            voice_data = voice_data.replace('um', '1')
            soma = self.converte_aritimetica(voice_data)
            self.engine_speak(f'O resultado é {soma.sum()}')
            
        if self.there_exist(['faça uma conta de subtração']):
            self.engine.runAndWait()
            self.engine_speak('O que voce quer subtrair')
            self.engine.runAndWait()
            voice_data = assistent.record_audio()
            voice_data = voice_data.replace('um', '1')
            subtracao = self.converte_aritimetica(voice_data)
            self.engine_speak(f'O resultado é {subtracao[0] - subtracao[1]}')
        
        if self.there_exist(['faça uma conta de multiplicação']):
            self.engine.runAndWait()
            self.engine_speak('O que voce quer multiplicar')
            self.engine.runAndWait()
            voice_data = assistent.record_audio()
            voice_data = voice_data.replace('um', '1')
            multiplicacao = self.converte_aritimetica(voice_data)
            self.engine_speak(f'O resultado é {multiplicacao[0] * multiplicacao[1]}')
            
        if self.there_exist(['faça uma conta de divisão']):
            self.engine.runAndWait()
            self.engine_speak('O que voce quer dividir')
            self.engine.runAndWait()
            voice_data = assistent.record_audio()
            voice_data = voice_data.replace('um', '1')
            divisao = self.converte_aritimetica(voice_data)
            self.engine_speak(f'O resultado é {divisao[0] / divisao[1]}')
        
assistent = Virtual_assit('Ayla', 'Mestre')

while True:

    voice_data = assistent.record_audio('Escutando...')
    assistent.respond(voice_data)

    if assistent.there_exist(['bye', 'obrigado', 'tchal', 'até logo', 'até logo', 'tchau', 'thanks']):
        assistent.engine_speak("Até logo")
        
        break