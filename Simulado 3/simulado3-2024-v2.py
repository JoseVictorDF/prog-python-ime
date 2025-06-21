def listaStrToFloat(l):
    '''Recebe uma lista de strings e converte os elementos para float'''
    for i in range(len(l)):
        if l[i]=='N':
            l[i] = 0
        else:
            l[i] = float(l[i])
        
def mediaPonderada(l,p):
    '''(l,p):Recebe a lista l e retorna a media dos elementos
        ponderada pelos pesos da lista p e a soma dos pesos
        cujo valor de l[i] é não nulo'''
    if len(l) != len(p):
        print('[mediaPonderada] Erro nos parâmetros.')
        exit()
    m,total=0,0
    for i in range(len(l)):
        if l[i]>0:
            m += l[i]*p[i]
            total += p[i]
    return m/total , total

nome = 'notas.csv'
try:
    arquivo = open(nome)
except:
    print('Erro na abertura do arquivo ',nome)
    exit()

posicao_codigo_aluno = 0
posicao_codigo_curso = 2
posicao_notas = 4
alunos = {} 
for i in arquivo:
    lista = i.rstrip().split(sep=';')
    if lista[posicao_codigo_curso] in alunos: 
        alunos[lista[posicao_codigo_curso]] += [[lista[posicao_codigo_aluno],lista[posicao_codigo_aluno+1]]+lista[posicao_notas:]]
    else:
        alunos[lista[posicao_codigo_curso]] = [[lista[posicao_codigo_aluno],lista[posicao_codigo_aluno+1]]+lista[posicao_notas:]]
arquivo.close()

nome = 'pesos.csv'
try:
    arquivo = open(nome)
except:
    print('Erro na abertura do arquivo ',nome)
    exit()

for curso in iter(alunos):
    arquivo.seek(0)
    for linha in arquivo:
        if linha.startswith(curso): p = linha.split(sep=';')[1:]
    listaStrToFloat(p)
    d_alunos = {} 
    for n in alunos[curso]:
        aux_l = n[2:]
        listaStrToFloat(aux_l)
        d_alunos[n[1]] = [n[posicao_codigo_aluno],mediaPonderada(aux_l,p)]
    l_alunos_ordenados = list(d_alunos)
    l_alunos_ordenados.sort()
    
    nome = 'alunos_Curso_'+curso+'.csv'
    with open(nome,mode='w') as arquivo_saida:
        for s in l_alunos_ordenados:
            arquivo_saida.write(s+';'+d_alunos[s][0]+';'+str('%.3f' % d_alunos[s][1][0])+';'+str('%d' % d_alunos[s][1][1])+'\n')
       
arquivo.close()
print('Fim da execução')
