import matplotlib.pyplot as plt

def gerar_grafico(dados, tipo='pizza', caminho='grafico.png'):
    categorias = [item[0] for item in dados]
    valores = [item[1] for item in dados]

    plt.figure(figsize=(6,6))
    if tipo == 'pizza':
        plt.pie(valores, labels=categorias, autopct='%1.1f%%')
    elif tipo == 'barras':
        plt.bar(categorias, valores)
        plt.ylabel('Valor gasto (R$)')
        plt.xticks(rotation=45)
    else:
        raise ValueError("Tipo de gráfico inválido.")
    plt.title('Gastos do mês por categoria')
    plt.tight_layout()
    plt.savefig(caminho)
    plt.close()