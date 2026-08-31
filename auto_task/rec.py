def selecionar_recuperacao(ID,value):
    botao =  wait.until(EC.element_to_be_clickable((By.XPATH, f"//label[normalize-space(.)='Recuperação']")))
    botao.click()
    botao2 = wait.until(EC.element_to_be_clickable((By.XPATH, f"//label[normalize-space(.)='{ID} ({value})']")))
    botao2.click()

