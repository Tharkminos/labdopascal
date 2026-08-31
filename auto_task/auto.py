from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time
from functions import nota as notas
import os
cwd = os.getcwd()
service = Service(str(cwd)+"/"+"chromedriver")
driver = webdriver.Chrome(service=service)

# Abre o Google
driver.get("https://auth-cs.identidadedigital.pr.gov.br/centralautenticacao/login.html?response_type=token&client_id=f340f1b1f65b6df5b5e3f94d95b11daf&redirect_uri=https%3A%2F%2Frco.paas.pr.gov.br&scope=emgpr.mobile%20emgpr.v1.ocorrencia.post&state=null&urlCert=https://certauth-cs.identidadedigital.pr.gov.br&dnsCidadao=https://cidadao-cs.identidadedigital.pr.gov.br/centralcidadao&loginPadrao=btnCentral&labelCentral=CPF,Login%20Sentinela&modulosDeAutenticacao=btnSentinela,btnCpf,btnCentral&urlLogo=https%3A%2F%2Fwww.registrodeclasse.seed.pr.gov.br%2Frcdig%2Fimages%2Flogo_sistema.png&acesso=2071&tokenFormat=jwt&exibirLinkAutoCadastro=true&exibirLinkRecuperarSenha=true&exibirLinkAutoCadastroCertificado=false&exibirAviso=true&captcha=false")
def login(user,senha):
    login = driver.find_element(By.ID, "attribute_central")
    login.send_keys(user)
    pwd = driver.find_element(By.ID, "password")
    pwd.send_keys(senha)

def selecionar_recuperacao(ID,value):
    botao =  wait.until(EC.element_to_be_clickable((By.XPATH, f"//label[normalize-space(.)='Recuperação']")))
    botao.click()
    botao2 = wait.until(EC.element_to_be_clickable((By.XPATH, f"//label[normalize-space(.)='{ID} ({value})']")))
    botao2.click()


def find_turmas():
    cards = wait.until(
        EC.presence_of_all_elements_located(
            (By.CSS_SELECTOR, ".card-body")
        )
    )
    for card in cards:
        infos = card.find_elements(By.CSS_SELECTOR, ".d-flex")

        print("Escola:", infos[0].text.strip())
        print("Turma:", infos[1].text.strip())
        print("Disciplina:", infos[2].text.strip())
        print("-" * 50)
    return cards
def selecionar_avaliacao(ID):
    botao = wait.until(EC.element_to_be_clickable(
            (By.XPATH, f"//label[normalize-space(.)='{ID}']")))
    botao.click()
def selecionar_data(data):
    # Abre o calendário
    campo = wait.until(
        EC.element_to_be_clickable(
            (By.ID, "dataAvaliacaoParcial")
        )
    )
    campo.click()

    # Espera o calendário aparecer
    calendario = wait.until(
        EC.visibility_of_element_located(
            (By.ID, "dataAvaliacaoParcial__dialog_")
        )
    )

    # Procura a data pelo atributo data-date
    dia = wait.until(
        EC.element_to_be_clickable(
            (
                By.CSS_SELECTOR,
                f'#dataAvaliacaoParcial__dialog_ [data-date="{data}"]:not([aria-disabled="true"])'
            )
        )
    )

    dia.click()

    # Espera o calendário fechar
    wait.until(
        EC.invisibility_of_element_located(
            (By.ID, "dataAvaliacaoParcial__dialog_")
        )
    )
def input_pesoDecimal(value):
    av_input= wait.until(EC.element_to_be_clickable((By.ID, "pesoDecimal")))
    av_input.click()
    av_input.send_keys(str(value))
def clicar_elemento(texto): 
    xpath = (f"//button[normalize-space()='{texto}']"
        f" | //a[normalize-space()='{texto}']"
        f" | //label[normalize-space()='{texto}']"
        f" | //*[@role='button' and normalize-space()='{texto}']")

    botao = wait.until(
        EC.element_to_be_clickable((By.XPATH, xpath))
    )
    #rede = driver.find_element(By.XPATH,f)
    botao.click()

def avaliar(alunos,conf,rng):
    wait = WebDriverWait(driver, 10 )
    botao = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[normalize-space()='Avaliação']")))
    botao.click()
    wait = WebDriverWait(driver, 2 )
    cnt = rng   
    while True:
        try:
            print(conf[f"AV{cnt}"])
            selecionar_avaliacao(f"AV{cnt}")
            selecionar_data("2026-08-18")
            input_pesoDecimal(conf[f"AV{cnt}"])
            break
        except Exception as error:
            print(error)
    wait = WebDriverWait(driver, 10 )
    b1 =  wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Avançar')]")))
    b1.click()
    for aluno in alunos:
        name = aluno["Nome"]    
        print(name)
        try:
            line = wait.until(EC.element_to_be_clickable((By.XPATH,f"//tr[.//td[contains(., '{name}')]]")))
            input_nota = line.find_element(By.CSS_SELECTOR,"input")
            input_nota.send_keys(aluno[f"AV{cnt}"])
        except Exception as error:
            print(error)
    print("Marcando Conteúdo...")
    checkbox = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH,"(//fieldset[.//legend//label[contains(normalize-space(), 'Conteúdos')]]//input[@type='checkbox'])[1]")))
    driver.execute_script("arguments[0].click();", checkbox)
    #input("Clique para Salvar:")
    print("Salvando...")
    botao_salvar = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH,"//div[contains(@class, 'card-footer')]//button[contains(normalize-space(), 'Salvar')]")))

    botao_salvar.click()
    print("Salvo com sucesso")


def recuperar(alunos,conf,rng):
    wait = WebDriverWait(driver, 2 )
    cnt = rng    
    while True:
        try:
            print(f"AV{cnt}",conf[f"RAV{cnt}"])
            selecionar_recuperacao(f"AV{cnt}",conf[f"RAV{cnt}"].replace(",","."))
            selecionar_data("2026-08-18")
            break
        except Exception as error:
            print(error)
    wait = WebDriverWait(driver, 10 )
    b1 =  wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Avançar')]")))
    b1.click()
    for aluno in alunos:
        name = aluno["Nome"]    
        print(name)
        try:
            line = wait.until(EC.element_to_be_clickable((By.XPATH,f"//tr[.//td[contains(., '{name}')]]")))
            input_nota = line.find_element(By.CSS_SELECTOR,"input")
            input_nota.send_keys(aluno[f"RAV{cnt}"])
        except Exception as error:
            print(error)
    #input("Clique para Salvar:")
    print("Salvando...")
    botao_salvar = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH,"//div[contains(@class, 'card-footer')]//button[contains(normalize-space(), 'Salvar')]")))

    botao_salvar.click()
    print("Salvo com sucesso")





login('11067177914','potencia1')
wait = WebDriverWait(driver, 10 )
clicar_elemento("Entrar")
elemento = wait.until(EC.element_to_be_clickable((By.XPATH,f"//label[contains(normalize-space(.), 'REDE ESTADUAL')]")))
elemento.click()
driver.get("https://rco.paas.pr.gov.br/livro")
turmas= find_turmas()

###///
classes = ["1 -8º Ano - Tarde - A",
           "2 -8º Ano - Tarde - B",
           "3 -8º Ano - Tarde - C",
           "4 -9º Ano - Manhã - A",
           "5 -9º Ano - Manhã - B",
           "6 -9º Ano - Manhã - C",
           "7 -1ª série - Manhã - B",
           "8 -ª série - Manhã - A - FE",
           "9 -1ª série - Manhã - A - RH",
           "10 -ª série - Manhã - A - FE",
           "11-ª série - Manhã - A - LG",
           "12-1ª série - Manhã - A - RH"
            ]
tri = '2º Tri'
turmas[11].find_element(By.XPATH,f".//a[normalize-space()='{tri}']").click()
est = '''
Nº	Média	Nome	AV1	1,0	AV2	2,0	AV3	3,0	AV4	4,0
1	8,1	ÁGATHA APARECIDA BARBOSA FARIA	1,0	0,8	2,0	2,0	1,5	1,0	3,6	0,0
2	6,5	ANDRIELLY DE OLIVEIRA CAMPOS	1,0	0,8	2,0	2,0	1,5	1,2	0,0	2,0
3	10,0	ASHLEY SCHMOLLER WERNER	1,0	0,8	2,0	2,0	3,0	1,8	4,0	0,0
4	8,1	BERNARDO HENRIQUE INACHESKI DE LORENA	1,0	0,8	1,6	1,6	2,5	1,6	3,0	0,0
5	8,1	BRUNO PHELYPE SANTOS MILANI	1,0	0,8	0,8	0,8	2,7	0,6	3,6	0,0
6	7,0	BRYAN LUCCAS DA SILVA AMBROSIO	1,0	0,8	2,0	2,0	2,3	2,0	0,0	1,7
7	7,6	CAUAN FELIPE POLERÁ	1,0	0,8	0,8	0,8	2,6	0,4	3,2	0,0
8	6,0	DAIANA ARCELES SAMPAIO	1,0	0,8	1,6	1,6	2,2	2,0	0,0	1,2
9	8,1	DIOGO ARON ALMEIDA DIAS	1,0	0,8	1,2	1,2	2,5	0,1	3,4	0,0
10	9,6	EDUARDO RAMOS CORDEIRO	1,0	0,8	2,0	2,0	3,0	1,6	3,6	0,0
11	9,1	ENZO MIGUEL DE OLIVEIRA STOCKER	1,0	0,8	1,6	1,6	2,7	1,0	3,8	0,0
12	8,1	ESTHEFANY LARISSA ALCANTARA DE ANDRADE	1,0	0,8	1,6	1,6	2,5	1,7	3,0	0,0
13	5,5	EWELYN RAYANE FERREIRA ALVES	1,0	0,8	0,8	0,8	2,2	0,1	0,0	1,5
14		FATIMA MORAIS RIZZATO		0,0						
15	6,0	FLAVIA ALESSANDRA LIMA NASCIMENTO	1,0	0,8	1,2	1,2	2,2	2,0	0,0	1,6
16		GABRIEL FERREIRA DA SILVA		0,0						
17	7,7	GIOVANA ANABELE MACHADO	1,0	0,8	1,2	1,2	1,5	1,5	4,0	0,0
18	9,2	GIOVANNA YASMIM MARTIMIANO DA SILVA	1,0	0,8	1,2	1,2	3,0	1,7	4,0	0,0
19	7,3	GUILHERME JULIAN RODRIGUES DE OLIVEIRA	1,0	0,8	0,8	0,8	2,7	0,5	2,8	0,0
20	9,2	HELENA LOPES CARCAIOLI	1,0	0,8	1,6	1,6	3,0	1,8	3,6	0,0
21	6,0	INGRID VITÓRIA CARDOSO DE PAULA	1,0	0,8	0,8	0,8	1,5	1,1	0,0	2,7
22	9,0	IOLANDA CRISTINA DOS SANTOS MARCOLINO	1,0	0,8	1,6	1,6	2,7	1,8	3,7	0,0
23		JOAO MUNIZ DOS SANTOS								
24	8,8	LAIS CAMILI TEIXEIRA DIAS	1,0	0,8	1,2	1,2	3,0	1,6	3,6	0,0
25		LETHYCIA GABRIELLY GOMES ANDRADE								
26		LIVIA LUIZA DE LARA SEQUINEL DE PAULA								
27	5,0	LUIZ GUSTAVO FOGUES OLIVEIRA	1,0	0,8	0,8	0,8	1,5	0,4	0,0	1,7
28	8,7	MARIA CECILIA SILVA POPOVISK	1,0	0,8	1,6	1,6	2,5	0,6	3,6	0,0
29	6,5	MARIA EDUARDA CAMARGO	1,0	0,8	1,2	1,2	1,5	0,1	2,8	0,0
30	5,5	MATHEUS GABRIEL LOURENCO ALBANO DA SILVA	1,0	0,8	0,8	0,8	2,4	1,0	1,3	0,0
31	5,5	MATHEUS KIERDEL TSCHURTSCHENTHALER	1,0	0,8	0,0	0,0	1,5	1,4	3,0	0,0
32	8,3	MAYSA EDUARDA BORIN	1,0	0,8	1,2	1,2	2,5	1,7	3,6	0,0
33	7,8	MURILLO ENRICO DA SILVA	1,0	0,8	1,2	1,2	2,0	1,1	3,6	0,0
34	6,3	MYLLENA ROCHA SOARES	1,0	0,8	0,8	0,8	1,5	0,4	3,0	0,0
35	9,3	NÍCOLAS ARAUJO DE AZEVEDO	1,0	0,8	1,6	1,6	2,7	0,1	4,0	0,0
36	7,1	PETERSON MATHEUS SOARES ROSA	1,0	0,8	1,6	1,6	2,5	2,0	0,0	2,0
37	10,0	SARAH EDUARDA CAVALCANTE DE OLIVEIRA	1,0	0,8	2,0	2,0	3,0	1,1	4,0	0,0
38	8,6	SIDNEI SANCHES	1,0	0,8	1,6	1,6	2,0	0,5	4,0	0,0
39		YASMIM GABRIELI DE LARA SEQUINEL DE PAULA								
40	9,5	YASMIN MELO SIECZKO DA SILVA	1,0	0,0	2,0	2,0	2,7	1,8	3,8	0,0
'''
alunos,conf  = notas(est)
salvando_notas = True
rng = 1
while salvando_notas:
    avaliar(alunos,conf,rng)
    recuperar(alunos,conf,rng)
    rng += 1
###///
#driver.get("https://rco.paas.pr.gov.br/avaliacao")

# Clica no primeiro resultado
#if resultados:
#    resultados[0].click()

input("Pressione ENTER para fechar...")

driver.quit()
