def listaFloat(l):
    '''Recebe uma lista e converte os elementos para float'''
    for i in range(len(l)):
        l[i] = float(l[i])
        
def media(l):
    '''Recebe uma lista e retorna a media dos elementos'''
    m=0
    for i in l:
        m += i
    return m/len(l)

nome = 'produtos_s2.csv'
try:
    arquivo = open(nome)
except:
    print('Erro na abertura do arquivo ',nome)
    exit()
    
historico = {} 
for i in arquivo:
    lista_produto = i.rstrip().split(sep=';')
    if lista_produto[-1] in historico:
        historico[lista_produto[-1]] += [lista_produto[:-1]]
    else:
        historico[lista_produto[-1]] = [lista_produto[:-1]]
arquivo.close()
print('Produtos separados por supermercado:\n',historico)

for k in iter(historico):
    d_produtos = {} 
    for p in historico[k]:
        aux_l = p[1:]
        listaFloat(aux_l)
        d_produtos[p[0]] = media(aux_l)        
    l_produtos_ordenados = list(d_produtos)
    l_produtos_ordenados.sort()
    nome = 'amostra_'+k+'.csv'
    with open(nome,mode='w') as arquivo_saida:
        for s in l_produtos_ordenados:
            arquivo_saida.write(s+';'+str('%.2f' % d_produtos[s])+'\n')
