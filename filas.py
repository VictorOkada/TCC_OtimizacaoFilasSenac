from datetime import datetime, timedelta
import pandas as pd
import PySimpleGUI as sg
import csv
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import poisson

#caminho de arquivo insumo do programa
csv_file_path = "C:/Users/victo/source/Autentication/entrada.csv"
caminhoRaiz = "C:/Users/victo/source/Autentication/entrada.csv"

#variáveis globais
n_postos = None
n_medicos = None
modelo = []
dadosModelo = []
saida_triagem = None
saida_atendimento = None
dataTriagem = []
dataAtendimento = []

def triagem(paciente):
    #variáveis globais que são utilizadas no programa
    global csv_file_path
    global saida_triagem
    global saida_atendimento
    global dataTriagem
    global dataAtendimento
    col = "Horário de Entrada" # pega dados aleatórios da coluna Horário Entrada do arquivo "entrada.csv"
    df = pd.read_csv(csv_file_path, sep=";", usecols=[col]) # varíavel lê os dados separados por delimitação de ponto e vírgula
    h_entrada = df.iloc[paciente][col] # lê os dados da coluna por endereço do paciente X nome de coluna
    hora_entrada = datetime.strptime(h_entrada, '%H:%M:%S').time() # converte valor para formato string
    #print(f"Valor de hora_entrada: {hora_entrada}") # imprime valor de variável
    entrada_fila_triagem = hora_entrada # iguala valor de hora entrada a variável
    #print(f"Valor de entrada_fila_triagem: {entrada_fila_triagem}")  # imprime valor de variável
    if paciente > 0 : # verifica se paciente é o primeiro da fila ou não
        time_str1 = time_to_int(entrada_fila_triagem) # converte valor de variável entrada_fila_triagem para tipo inteiro
        time_str2 = time_to_int(saida_triagem) # converte valor de variável saida_triagem para tipo inteiro
        saida_fila_triagem = saida_fila_tgm(time_str1, time_str2, entrada_fila_triagem, saida_triagem) # chama função saida_fila_tgm para retornar maior valor entre entrada_fila_triagem e saida_triagem
        #print(f"Valor de saida_fila_triagem: {saida_fila_triagem}") # imprime valor de variável
    else:
        saida_fila_triagem = entrada_fila_triagem # iguala valor de entrada_fila_triagem a variável
        #print(f"Valor de saida_fila_triagem: {saida_fila_triagem}") # imprime valor de variável
    tempo_fila_triagem = time_difference(entrada_fila_triagem, saida_fila_triagem) # chama função time_difference que subtrai a diferença de horários das variáveis entrada_fila_triagem e saida_fila_triagem
    #print(f"Valor de tempo_fila_triagem: {tempo_fila_triagem}") # imprime valor de variável
    entrada_triagem = saida_fila_triagem # iguala valor de saida_fila_triagem a variável
    #print(f"Valor de entrada_triagem: {entrada_triagem}") # imprime valor de variável
    col = "Chegada na Triagem" # pega dados aleatórios da coluna Chegada na Triagem do arquivo "entrada.csv"
    df = pd.read_csv(csv_file_path, sep=";", usecols=[col]) # varíavel lê os dados separados por delimitação de ponto e vírgula
    chegada = df.iloc[paciente][col] # lê os dados da coluna por endereço do paciente X nome de coluna
    tempo_triagem = dist_probabilidade_triagem(chegada) # Retorna o tempo de fila de triagem de acordo com a distribuição de probabilidade de Triagem
    #print(f"tempo_triagem do Paciente {paciente} na Fila: {tempo_triagem}") # imprime valor de variável
    time_str1 = time_to_int(entrada_triagem) # converte valor de variável entrada_triagem para tipo inteiro
    time_str2 = time_to_int(tempo_triagem) # converte valor de variável tempo_triagem para tipo inteiro
    s_t = time_str1 + time_str2 # soma as variáveis
    saida_triagem = convert_to_time(s_t) # converte soma obtida em valor do tipo "hora"
    #print(f"Valor de Saída de Triagem: {saida_triagem}")  # imprime valor de variável 
    #print(f"Paciente {paciente + 1} triado") # imprime valor de paciente
    return hora_entrada,entrada_fila_triagem,saida_fila_triagem,tempo_fila_triagem,entrada_triagem,saida_triagem,tempo_triagem # retorna dados de função triagem
    
def atendimento_medico(paciente, hora_entrada, saida_triagem):
    #variáveis globais que são utilizadas no programa
    global csv_file_path
    global saida_atendimento
    entrada_fila_atendimento = saida_triagem[paciente] # iguala valor de saida_triagem a variável
    #print(f"Valor de Entrada Fila de Atendimento: {entrada_fila_atendimento}") # imprime valor de variável
    if paciente > 0: # verifica se paciente é o primeiro da fila ou não
        time_str1 = time_to_int(entrada_fila_atendimento) # converte valor de variável entrada_fila_atendimento para tipo inteiro
        time_str2 = time_to_int(saida_atendimento) # converte valor de variável saida_atendimento para tipo inteiro
        saida_fila_atendimento = saida_fila_tgm(time_str1, time_str2, entrada_fila_atendimento, saida_atendimento) # chama função saida_fila_tgm para retornar maior valor entre entrada_fila_atendimento e saida_atendimento
        #print(f"Valor de saida_fila_triagem: {saida_fila_atendimento}") # imprime valor de variável
    else: 
        saida_fila_atendimento = entrada_fila_atendimento # iguala valor de entrada_fila_atendimento a variável
    #print(f"Valor de Saída Fila de Atendimento: {saida_fila_atendimento}") # imprime valor de variável
    tempo_fila_atendimento = time_difference(saida_fila_atendimento, entrada_fila_atendimento) #chama função time_difference que subtrai a diferença de horários das variáveis saida_fila_atendimento e entrada_fila_atendimento
    #print(f"Valor de Tempo de Fila de Atendimento: {tempo_fila_atendimento}") # imprime valor de variável
    col = "Chegada de Atendimento" # pega dados aleatórios da coluna Chegada de Atendimento do arquivo "entrada.csv"
    df = pd.read_csv(csv_file_path, sep=";", usecols=[col]) # varíavel lê os dados separados por delimitação de ponto e vírgula
    chegada = df.iloc[paciente][col]  # lê os dados da coluna por endereço do paciente X nome de coluna
    tempo_atendimento = dist_probabilidade_atendimento(chegada) # retorna o tempo de fila de Atendimento Médico de acordo com a distribuição de probabilidade de Atendimento Médico
    #print(f"Valor de Tempo de Atendimento: {tempo_atendimento}") # imprime valor de variável
    entrada_atendimento = saida_fila_atendimento # iguala valor de saida_fila_atendimento a variável
    #print(f"Valor de Entrada de Atendimento: {entrada_atendimento}") # imprime valor de variável
    time_str1 = time_to_int(entrada_atendimento) # converte valor de variável entrada_atendimento para tipo inteiro
    time_str2 = time_to_int(tempo_atendimento) # converte valor de variável tempo_atendimento para tipo inteiro
    s_t = time_str1 + time_str2  # soma as variáveis
    saida_atendimento = convert_to_time(s_t)  # converte soma obtida em valor do tipo "hora"
    #print(f"Valor de hora_entrada: {hora_entrada[paciente]}") # imprime valor de variável
    #print(f"Valor de Saída de Atendimento: {saida_atendimento}") # imprime valor de variável
    tempo_sistema = time_difference(hora_entrada[paciente],saida_atendimento) #chama função time_difference que subtrai a diferença de horários das variáveis hora_entrada e saida_atendimento
    #print(f"Valor de Tempo de Sistema: {tempo_sistema}") # imprime valor de variável
    #print(f"Paciente {paciente + 1} Atendido") # imprime valor de variável
    return entrada_fila_atendimento, saida_fila_atendimento, tempo_fila_atendimento, entrada_atendimento, saida_atendimento, tempo_atendimento, tempo_sistema # retorna dados de função Atendimento Médico


def convert_to_time(seconds):
    hours, remainder = divmod(seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    return '{:02}:{:02}:{:02}'.format(int(hours), int(minutes), int(seconds))

def time_to_int(dateobj):
    try:
        time_format = '%H:%M:%S'
        string = str(dateobj)
        current_time = datetime.strptime(string, time_format)
        total = int(current_time.strftime("%S"))
        total += int(current_time.strftime('%M')) * 60
        total += int(current_time.strftime('%H')) * 60 * 60
    except:
        total = 0
    return total

def time_difference(time_str1, time_str2):
    #em caso de erro ao calcular a diferenca(ocorre quando variaveis estão em formatos diferentes. Ex: datetime e string)
    try:
        # converte string em datetime
        datetime1 = datetime.combine(datetime.today(), time_str1)
        datetime2 = datetime.combine(datetime.today(), time_str2)

        # Calcula a diferença de variáveis datetime
        difference = datetime2 - datetime1
    except:
        #converte datetime em inteiro
        var1 = time_to_int(time_str1)
        var2 = time_to_int(time_str2)
        if var2 > var1:
            s_t = var2 - var1
        else:
            s_t = var1 - var2
        saida_triagem = convert_to_time(s_t)
         # Calculate the time difference
        difference = saida_triagem
    # Retorna variavel difference
    return difference

def retornaMediaTempoFila(tempo_fila):
    #calcula média de tempo_fila, caso divisao por 0 retorna 0
    try: 
        media = sum(tempo_fila) / len(tempo_fila)
    except ZeroDivisionError:
        media = 0
    return media

def calcularDisponibilidade(postoAtendimento, clientes):
    match postoAtendimento:
        case 1: clientes = 1 ; return clientes
        case 2: clientes = 2 ; return clientes
        case 3: clientes = 3 ; return clientes
        case 4: clientes = 4 ; return clientes
        case 5: clientes = 5 ; return clientes
        case 6: clientes = 6 ; return clientes
        case 7: clientes = 7 ; return clientes
        case 8: clientes = 8 ; return clientes
        case 9: clientes = 9 ; return clientes
        case 10: clientes = 10 ; return clientes
        case _:
            print("O número máximo de postos de atendimento é 10. Digite um número menor")
    
def dist_probabilidade_triagem(chegada): # distribuição de probabilidade na chegada dos pacientes no serviço de Triagem
    if chegada <= 20: tempo_espera = timedelta(hours=0, minutes=4, seconds=0) # retorna "00:04:00" se valor de variável chegada for menor ou igual a 20
    elif chegada >= 21 and chegada <= 30: tempo_espera = timedelta(hours=0, minutes=5, seconds=0) # retorna "00:05:00" se valor de variável chegada estiver entre 21 e 30
    elif chegada >= 31 and chegada <= 50: tempo_espera = timedelta(hours=0, minutes=8, seconds=0) # retorna "00:08:00" se valor de variável chegada estiver entre 31 e 50
    elif chegada >= 51 and chegada <= 80: tempo_espera = timedelta(hours=0, minutes=12, seconds=0) # retorna "00:12:00" se valor de variável chegada estiver entre 51 e 80
    else : tempo_espera = timedelta(hours=0, minutes=15, seconds=0) # retorna "00:15:00" se valor de variável chegada for maior que 80
    return tempo_espera


def dist_probabilidade_atendimento(chegada): # distribuição de probabilidade na chegada dos pacientes no serviço de Atendimento Médico
    if chegada <= 10: tempo_espera = timedelta(hours=0, minutes=10, seconds=0) # retorna "00:10:00" se valor de variável chegada for menor ou igual a 10
    elif chegada >= 11 and chegada <= 30: tempo_espera = timedelta(hours=0, minutes=15, seconds=0) # retorna "00:15:00" se valor de variável chegada estiver entre 11 e 30
    elif chegada >= 31 and chegada <= 70: tempo_espera = timedelta(hours=0, minutes=18, seconds=0) # retorna "00:18:00" se valor de variável chegada estiver entre 31 e 70
    else : tempo_espera = timedelta(hours=0, minutes=20, seconds=0)  # retorna "00:20:00" se valor de variável chegada for maior que 70
    return tempo_espera

def saida_fila_tgm(v1, v2, hora_entrada, saida_triagem):
    if v1 < v2: return saida_triagem
    else: return hora_entrada

def imprimir_dados_modelo(txChegada_filaTriagem, media_tempo_fila_triagem, media_tempo_fila_atend, media_tempo_atend): #recebe como parÂmetros o tempo médio: fila de Triagem, Triagem, fila de Atendimento Médico, Atendimento Médico
    sg.theme('DarkTeal3') # tema da janela de interface
    layout = [
        [sg.Text("Modelo de Dados", font="Arial 20 bold", pad=(10, 10), justification="Left")],
        [sg.Text("Tempo Médio de Fila Triagem em minutos"), sg.InputText(txChegada_filaTriagem, font=("Arial 10 bold"), disabled=True)],
        [sg.Text("Tempo Médio de Atendimento Triagem em minutos"), sg.InputText(media_tempo_fila_triagem, font=("Arial 10 bold"), disabled=True)],
        [sg.Text("Tempo Médio de Fila Atendimento Médico em minutos"), sg.InputText(media_tempo_fila_atend, font=("Arial 10 bold"), disabled=True)],
        [sg.Text("Tempo Médio de Atendimento Médico em minutos"),  sg.InputText(media_tempo_atend, font=("Arial 10 bold"), disabled=True)]
    ] #caixas de texto com informação exibidas na tela somente para a exibição
    janela = sg.Window("Modelo de Dados", layout) # janela do modelo com título "Modelo de Dados"
    botao, valores = janela.read() # variáveis eventos e valores responsáveis pelo armazenamento de informações de objetos da interface para execução do programa
    janela.close() # fecha janela ativa
    if botao == 'voltar': # botão voltar para o menu
        janela.close() # fecha janela ativa


def imprimir_dados_iniciais(dados):
    sg.theme('DarkTeal3') # tema da janela de interface
    layout = [
        [sg.Text("Dados Aleatórios", font=("Arial 16 bold"), pad=(20, 30))],
        [sg.Table(values=dados, headings=['Chegada dos pacientes','Horário de Entrada','Chegada na Triagem',
                                          'Chegada de Atendimento'],
                                           auto_size_columns=True, num_rows=20)],
        [sg.Button("Voltar", key="voltar", size=(24, 2))]
    ] #caixas de texto e tabelas com informação exibidas na tela somente para a exibição
    janela = sg.Window("Dados Aleatórios", layout) # janela do modelo com título "Dados Aleatórios"
    botao, valores = janela.read() # variáveis eventos e valores responsáveis pelo armazenamento de informações de objetos da interface para execução do programa
    janela.close() # fecha janela ativa
    if botao == 'voltar': # botão voltar para o menu
        janela.close() # fecha janela ativa

def imprimir_dados(dados, dados2):
    sg.theme('DarkTeal3') # tema da janela de interface
    layout = [
        [sg.Text("Triagem", font=("Arial 16 bold"), pad=(20, 30))],
        [sg.Table(values=dados, headings=['hora_entrada','entrada_fila_triagem', 'saida_fila_triagem','tempo_fila_triagem', 'entrada_triagem','saida_triagem','tempo_triagem'],
                                           auto_size_columns=True, num_rows=20)],
        [sg.Text("Atendimento Médico", font=("Arial 16 bold"), pad=(20, 30))],
        [sg.Table(values=dados2, headings=['entrada_fila_atendimento','saida_fila_atendimento','tempo_fila_atendimento', 'entrada_atendimento','saida_atendimento','tempo_atendimento','tempo_sistema'],
                                           auto_size_columns=True, num_rows=20)],
        [sg.Button("Voltar", key="voltar", size=(24, 2))]
    ] #caixas de texto e tabelas com informação exibidas na tela somente para a exibição
    janela = sg.Window("Dados Centro Hospitalar", layout) # janela do modelo com título "Dados Centro Hospitalar"
    botao, valores = janela.read() # variáveis eventos e valores responsáveis pelo armazenamento de informações de objetos da interface para execução do programa
    janela.close() # fecha janela ativa
    if botao == 'voltar': # botão voltar para o menu
        janela.close() # fecha janela ativa
  
def import_csv_file():
    filepath = sg.popup_get_file('Selecione o arquivo CSV') #abre popup pra seleção de arquivo de extensão .csv
    if filepath: #verifica se diretório existe
        with open(filepath, 'r', newline='') as file: # lê os registros contidos no arquivo .csv 
            reader = csv.reader(file) # determina a extensão do arquivo padrão como .csv
            data = list(reader) #adiciona arquivo na variável data
        return data # retorna arquivo
    return None #retorna vazio se não encontrar diretório

def export_csv_file(data):
    if data: #verifica se dados existem
        filepath = sg.popup_get_file('Salvar como', save_as=True, file_types=(("Arquivos CSV", "*.csv"),)) #abre popup pra salvar arquivo em extensão .csv
        if filepath: #verifica se diretório existe
            with open(filepath, 'w', newline='') as file: # escreve os registros contidos em data no arquivo .csv de saída
                writer = csv.writer(file) # determina a extensão do arquivo padrão como .csv
                writer.writerows(data) #escreve linhas de registro no arquivo na variável data
            sg.popup('Arquivo exportado com sucesso!') # exibe mensagem de sucesso de importação na tela

def main(postosAtendimento, num_medicos):
    global csv_file_path
    global saida_triagem
    global saida_atendimento
    contador = 0
    paciente = 0
    entrada_fila_triagem = 0
    saida_fila_triagem = 0
    entrada_triagem = 0
    tempo_fila_triagem = 0
    tempo_triagem = 0
    tx_sistema = 0
    tx_chegada = 0
    saida_atendimento = 0
    h_s = []
    lista_entrada = []
    h_s3 = []
    media_tx_fila_triagem = []
    tempo_fila = []
    tx_fila_triagem = []
    tx_chegada_triagem = []
    tx_atend_triagem = []
    tx_chegada_atend = []
    tx_atend_fila = []
    tx_atend = []

    data1 = []
    data2 = []
    global dataTriagem
    global dataAtendimento

    col = "Horário de Entrada"
    df = pd.read_csv(csv_file_path, sep=";", usecols=[col])
    linhasTotal = df.shape[0]

    #verifica quantos postos de atendimento estao disponiveis 
    disponibilidade = calcularDisponibilidade(postosAtendimento, linhasTotal)
    print(f"Caixas disponíveis para atendimento: {disponibilidade}")

    linhasTotal = int(linhasTotal / disponibilidade)
    print(linhasTotal)

    #laço de execucao total
    while paciente < linhasTotal:
        # executa a trigaem e atendimento dos pacientes a partir do retorno de postos(onde é atendido apenas quando disponiveo o numero de postos)
        while contador < disponibilidade:
            chegada, entrada_fila_triagem, saida_fila_triagem, tempo_fila_triagem, entrada_triagem, saida_triagem, tempo_triagem = triagem(paciente)
            data1 = [chegada, entrada_fila_triagem, saida_fila_triagem, tempo_fila_triagem, entrada_triagem, saida_triagem, tempo_triagem]
            dataTriagem.append(data1)
            contador+=1
            paciente+=1
            tx_sistema = time_to_int(tempo_triagem)
            tx_chegada = time_to_int(chegada)
            tx_chegada_triagem.append(tx_chegada)
            tx_atend_triagem.append(tx_sistema)

            media_tx_fila_triagem.append(tempo_fila_triagem)
            h_s.append(tempo_triagem)
            lista_entrada.append(chegada)
            h_s3.append(saida_triagem)
            t_fila = time_to_int(tempo_triagem)
            t_fila_tgm = time_to_int(tempo_fila_triagem)
            tempo_fila.append(t_fila) 
            tx_fila_triagem.append(t_fila_tgm)

        #paciente = paciente + 1
        contador = 0

    txChegada_filaTriagem = retornaMediaTempoFila(tx_fila_triagem)
    #print("Tempo Médio de Fila de Triagem em minutos:", round(txChegada_filaTriagem * 60, 4)) 
    print("Tempo Médio de Fila de Triagem em minutos:", convert_to_time(txChegada_filaTriagem))
    media_tempo_fila_triagem = retornaMediaTempoFila(tempo_fila)
    print("Tempo Médio de Triagem em minutos:", convert_to_time(media_tempo_fila_triagem))
    #print("Tempo Médio de Triagem em minutos:", round(media_tempo_fila_triagem * 60, 4)) 

    paciente = 0
    contador = 0
    disponibilidade = calcularDisponibilidade(num_medicos, linhasTotal)
    print(f"Número de Médicos disponíveis para Atendimento: {disponibilidade}")

    linhasTotal = int(linhasTotal / disponibilidade)
    print(linhasTotal)

    #laço de execucao total
    while paciente < linhasTotal :
        while contador < disponibilidade:
            entrada_fila_atendimento, saida_fila_atendimento, tempo_fila_atendimento, entrada_atendimento, saida_atendimento, tempo_atendimento, tempo_sistema = atendimento_medico(paciente, lista_entrada, h_s3)
            data2 = [entrada_fila_atendimento, saida_fila_atendimento, tempo_fila_atendimento, entrada_atendimento, saida_atendimento, tempo_atendimento, tempo_sistema]
            dataAtendimento.append(data2)
            contador+=1
            paciente+=1
            tx_sistema_atend = time_to_int(tempo_atendimento)
            tx_chegada_atend = time_to_int(tempo_fila_atendimento)
            tx_atend_fila.append(tx_chegada_atend)
            tx_atend.append(tx_sistema_atend)

        #paciente = paciente + 1
        contador = 0

    media_tempo_fila_atend = retornaMediaTempoFila(tx_atend_fila)
    print("Tempo médio de Fila de Atendimento em minutos:", convert_to_time(media_tempo_fila_atend))
    #print("Tempo médio de Fila de Atendimento em minutos:", round(media_tempo_fila_atend * 60, 4)) 
    media_tempo_atend = retornaMediaTempoFila(tx_atend)
    print("Tempo médio de Atendimento em minutos:", convert_to_time(media_tempo_atend))
    #print("Tempo médio de Atendimento em minutos:", round(media_tempo_atend * 60, 4)) 

    imprimir_dados_modelo(convert_to_time(txChegada_filaTriagem), convert_to_time(media_tempo_fila_triagem), convert_to_time(media_tempo_fila_atend), convert_to_time(media_tempo_atend)) #imprime dados do modelo na tela

    imprimir_dados(dataTriagem, dataAtendimento) #imprime processamento de dados na tela

    #imprimir gráficos de Poisson na tela

    sample1 = poisson.rvs(mu=txChegada_filaTriagem/60, size=100)
    sample2 = poisson.rvs(mu=media_tempo_fila_atend/60, size=100)

    #Plotting Poisson Distribution using Seaborn
    plt.figure(figsize=(10, 5))
    plt.title("Tempo Médio de Fila Atendimento Triagem vs Tempo Médio de Fila Atendimento Médico")
    sns.kdeplot(x=sample1, fill=True, label='Tempo Médio de Fila Triagem')
    sns.kdeplot(x=sample2, fill=True, label='Tempo Médio de Fila Atendimento Triagem')
    plt.xlabel('Tempo Médio em minutos')
    plt.ylabel('Probabilidade')
    plt.legend()
plt.show()




if __name__ == "__main__":
    paciente = 0 # incialização da variável paciente
    dataAleat = [] #lista de dados aleatórios temporária
    dataAleatFinal = [] # lista de dados aleatórios exibidas no botão "Exibir dados de entrada"
    sg.theme('DarkTeal3')

    layout = [
        [sg.Text("Centro Hospitalar", font="Arial 25 bold", pad=(100, 20), justification="Center")], # texto de exibição central do nome do programa
        [sg.Text("Número de Postos de Atendimento", font=("Arial 18"), pad=(0, 10)), sg.Spin([1,2,3,4,5,6,7,8,9,10], size=(6,2), key="postosAtendimento")], #caixa de adição ou subtração de valores de postos de atendimento
        [sg.Text("Número de Médicos", font=("Arial 18"), pad=(0, 10)), sg.Spin([1,2,3,4,5,6,7,8,9,10], size=(6,2), key="numMedicos")], #caixa de adição ou subtração de valores de némeros de médicos
        [sg.Button('Exibir dados de entrada', key='-DISPLAY-', size=(20,3), pad=(150, 10))], # botão responsável por exibir dados aleatórios do arquivo "entrada.csv"
        [sg.Button('Importar arquivo CSV', key='-IMPORT-', size=(20,3), pad=(150, 10))], # botão responsável pela importação do arquivo "entrada.csv" para execução do programa
        [sg.Button('Exibir dados do modelo', key='-DISPLAY2-', size=(20,3), pad=(150, 10))], # botão responsável pela execução e geração do modelo de fila e gráficos Poisson
        [sg.Button('Exportar arquivo CSV', key='-EXPORT-', size=(20,3), pad=(150, 10))] # botão responsável pela exportação de arquivo "saida.csv" no final de execução do programa
    ]

    window = sg.Window('Menu', layout, size=(500, 500))  # janela de execução do menu do programa com tamanho 500 x 500

    while True:
        event, values = window.read()  # variáveis eventos e valores responsáveis pelo armazenamento de informações de objetos da interface para execução do programa
        if event == sg.WINDOW_CLOSED: #evento de fechamento de janela ativa
            break
        elif event == '-IMPORT-': # evento de botão de importação de arquivo de entrada
            data = import_csv_file()
        elif event == '-DISPLAY-': # evento de botão de exibir dados de entrada
            while paciente < 100: # executa a amostra de 100 pacientes contida no arquivo "entrada.csv"
                col = "Chegada dos pacientes" #dado aleatorio
                df = pd.read_csv(caminhoRaiz, sep=";", usecols=[col])
                chegada_pacientes = df.iloc[paciente][col] # pega numero de chegada do .csv
                col = "Horário de Entrada" #dado aleatorio
                df = pd.read_csv(caminhoRaiz, sep=";", usecols=[col])
                hora_entrada = df.iloc[paciente][col] # pega numero de chegada do .csv
                col = "Chegada na Triagem" #dado aleatorio
                df = pd.read_csv(caminhoRaiz, sep=";", usecols=[col])
                chegada_triagem = df.iloc[paciente][col] # pega numero de chegada do .csv
                col = "Chegada de Atendimento" #dado aleatorio
                df = pd.read_csv(caminhoRaiz, sep=";", usecols=[col])
                chegada_atendimento = df.iloc[paciente][col] # pega numero de chegada do .csv
                dataAleat = [chegada_pacientes, hora_entrada, chegada_triagem, chegada_atendimento] # armazena lista de dados do laço do paciente tratado
                dataAleatFinal.append(dataAleat) # armazena dados de lista dataAleat para exibição completa de dados aleatórios
                paciente = paciente + 1 # incrementa a variável paciente para execução do programa
            imprimir_dados_iniciais(dataAleatFinal) # imprime dados aleatórios em uma nova janela
        elif event == '-DISPLAY2-': # evento de botão de Exibir dados do modelo
            postosAtendimento = values['postosAtendimento'] # guarda o valor de Spin "Postos de Atendimento"
            num_medicos = values['numMedicos'] # guarda o valor de Spin "Número de Médicos"
            main(postosAtendimento, num_medicos) # roda a execução do modelo de fila
        elif event == '-EXPORT-': # evento de botão de exportação de arquivo "saida.csv"
            export_csv_file(dataTriagem, dataAtendimento) #exporta dados de Triageme Atendimento médico

    window.close() # fecha janela do Menu
