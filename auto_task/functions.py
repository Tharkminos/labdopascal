
def nota(alunos):
    alunos = alunos.split("\n")
    alunos_geral  = []
    sistema = alunos[1].replace("Média","").split('\t')
    for item in sistema:
        if item == '':
            sistema.remove(item)
    for i,aluno in enumerate(alunos):
        if aluno != "" and i != 1:
            alunos_geral.append(aluno)
    keys = []
    conf = {}
    temp = []
    for i in range(len(sistema)):
        if not (sistema[i].startswith("AV") or ',' in sistema[i]) :
            keys.append(sistema[i])
        else:
            temp.append(sistema[i])
    #print(temp)
    for i in range(0,len(temp),2):
        A = temp[i]
        conf[f"{A}"] = temp[i+1]
        conf[f"R{A}"]= temp[i+1]
    #print(conf) // Notas obtidas até agora
    estudante =  []
    for aluno in alunos_geral:
        tp = aluno.split("\t")
        tp.pop(1)
        alumni = {}

        for c in range(0,4):
            if c < 3:         
                alumni[sistema[c]] = tp[c]
        alumni
        for j,opcao in enumerate(conf):
            alumni[opcao] = tp[j+2]
        estudante.append(alumni)
    return estudante,conf

