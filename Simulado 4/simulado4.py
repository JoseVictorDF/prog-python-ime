import numpy as np

def erro(a1, a2):
    """Retorna um array com o valor absoluto do erro entre a1 e a2.
    Considera arrays de mesmo comprimento"""
    return abs(a1-a2)

def verificarNeg(arr):
    """Retorna True se dados no array arr contem valor negativo."""
    if (arr<0).any():
        return True
    else:            
        return False

def main():
    nome = 'tabela.txt'
    try:
        tabela = np.loadtxt(nome)
    except:
        print('Erro no acesso ao arquivo ',nome)
        return -1

    nome = 'info.txt'
    try:
        info = np.loadtxt(nome)
    except:
        print('Erro no acesso ao arquivo ',nome)
        return -1
    else:
        if verificarNeg(info):
            print(f"Dados no arquivo {nome} não atendem o padrão esperado. Erro: presença de valor negativo.")

    col = 2
    coluna = tabela[:,col]
    coluna.sort()
    info.sort()
    n_coluna = coluna.shape[0]
    n_info = info.shape[0]
    completar = False
    if n_info < n_coluna:
        completar = True
        n = n_info
        erro_ = erro(coluna[:n],info)
        colunaStr = []
        for i in range(n,n_coluna): colunaStr += [f"{coluna[i]:.6f}"]
        qtd = n_coluna-n
        saidaNull = np.concatenate((np.array(colunaStr[0:qtd]).reshape(qtd,1),np.full(qtd,"null").reshape(qtd,1),np.full(qtd,"null").reshape(qtd,1)),axis=1)
    else:
        n = n_coluna
        erro_ = erro(coluna,info[:n])
        
    coluna_ = coluna[:n]
    info_ = info[:n]
    saida = np.concatenate((coluna_.reshape(n,1),info_.reshape(n,1),erro_.reshape(n,1)),axis=1)    

    nome = 'saida.txt'
    try:
        f = open(nome,'w')
        np.savetxt(f,saida,fmt='%.6f')
        f.close()
        if completar:
            f = open(nome,'a')
            np.savetxt(f,saidaNull,fmt='%s')
            f.close()
    except:
        print('Erro na escrita do arquivo ',nome)
        return -1
    print("Fim.")

if __name__=="__main__":
    main()