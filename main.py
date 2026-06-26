import csv
import sys
import os

# Tratamento para verificar dependências do PDF
try:
    from fpdf import FPDF
    import matplotlib.pyplot as plt
    HAS_PDF = True
except ImportError:
    HAS_PDF = False

def calcular_custo_unitario(custo_pool, capacidade_total):
    """
    Fórmula do Custeio ABC (Activity-Based Costing):
    Taxa do Direcionador (Custo Unitário) = Custo do Pool / Volume Total
    """
    return custo_pool / capacidade_total

def calcular_custo_etapa(custo_unitario, consumo_real):
    """
    Fórmula de Alocação de Custos:
    Custo da Etapa = Taxa do Direcionador (Custo Unitário) * Consumo Real do Mês
    """
    return custo_unitario * consumo_real

def carregar_dados(caminho_csv):
    """
    Lê o CSV preenchido com a capacidade e o custo real.
    """
    dados = []
    try:
        with open(caminho_csv, mode='r', encoding='utf-8') as arquivo:
            leitor_csv = csv.DictReader(arquivo)
            for linha in leitor_csv:
                dados.append({
                    "Etapa": linha["Etapa"],
                    "Capacidade_Total": float(linha["Capacidade_Total"]),
                    "Custo_Pool": float(linha["Custo_Pool"]),
                    "Consumo_Mes": float(linha["Consumo_Mes"])
                })
        return dados
    except FileNotFoundError:
        print(f"Erro: O arquivo '{caminho_csv}' não foi encontrado na pasta.")
        return None

def processar_contabilidade(dados):
    """
    Aplica as funções matemáticas contábeis linha a linha.
    """
    resultados = []
    custo_total_app = 0.0

    for item in dados:
        # Calculamos os dois pilares contábeis
        custo_unit = calcular_custo_unitario(item["Custo_Pool"], item["Capacidade_Total"])
        custo_etapa = calcular_custo_etapa(custo_unit, item["Consumo_Mes"])
        
        # Somatório do centro de custo
        custo_total_app += custo_etapa
        
        resultados.append({
            "Etapa": item["Etapa"],
            "Custo_Unitario": custo_unit,
            "Consumo_Mes": item["Consumo_Mes"],
            "Custo_Total_Etapa": custo_etapa
        })
        
    return resultados, custo_total_app

def exibir_terminal(resultados, custo_total_app):
    """
    Imprime uma tabela direta e limpa no terminal via CLI.
    """
    print("\n" + "=" * 70)
    print(f"{'CUSTO DE PRODUÇÃO DO APP DELIVERY':^70}")
    print("=" * 70)
    print(f"{'Etapa do Software':<25} | {'Custo Unitário':<15} | {'Consumo':<10} | {'Custo da Etapa'}")
    print("-" * 70)
    
    for res in resultados:
        etapa = res['Etapa']
        unit = f"R$ {res['Custo_Unitario']:.2f}"
        cons = str(int(res['Consumo_Mes']))
        total = f"R$ {res['Custo_Total_Etapa']:.2f}"
        
        print(f"{etapa:<25} | {unit:<15} | {cons:<10} | {total}")
        
    print("-" * 70)
    print(f"{'CUSTO TOTAL DO APP':<56} | R$ {custo_total_app:.2f}")
    
    print("\n--- ANÁLISE DE IMPACTO FINANCEIRO ---")
    print("> Mais caras: Empate entre Desenvolvimento e Suporte (R$ 4.000,00 cada).")
    print("> Impacto de menos bugs: Menor gasto na etapa de QA (Testes) e drástica redução de chamados (economia direta no Suporte Técnico).\n")

def gerar_grafico_pizza(resultados):
    """
    Gera uma imagem temporária de um gráfico de pizza.
    """
    etapas = [res["Etapa"] for res in resultados]
    custos = [res["Custo_Total_Etapa"] for res in resultados]
    cores = ['#3498db', '#e74c3c', '#2ecc71', '#f39c12']
    
    plt.figure(figsize=(6, 4))
    plt.pie(custos, labels=etapas, autopct='%1.1f%%', startangle=140, colors=cores)
    plt.title("Distribuicao dos Custos Reais")
    plt.tight_layout()
    plt.savefig("grafico_pizza_temp.png")
    plt.close()

def gerar_pdf(resultados, custo_total_app):
    """
    Gera o relatório em PDF com as tabelas e o gráfico (usando FPDF).
    """
    if not HAS_PDF:
        print("\n[!] Erro: Bibliotecas 'fpdf' e/ou 'matplotlib' não instaladas.")
        return

    # Gera a imagem no PDF
    gerar_grafico_pizza(resultados)

    pdf = FPDF()
    pdf.add_page()
    
    # Cabeçalho
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(0, 10, "Relatorio de Custos - App Delivery (Custeio ABC)", ln=True, align='C')
    pdf.ln(5)
    
    # Tabela Cabeçalhos
    pdf.set_font("Arial", 'B', 10)
    pdf.set_fill_color(52, 73, 94) # Fundo escuro
    pdf.set_text_color(255, 255, 255) # Texto branco
    pdf.cell(50, 10, "Etapa", border=1, fill=True)
    pdf.cell(40, 10, "Custo Unitario", border=1, fill=True, align='C')
    pdf.cell(30, 10, "Consumo", border=1, fill=True, align='C')
    pdf.cell(45, 10, "Custo da Etapa", border=1, fill=True, align='C')
    pdf.ln()
    
    # Tabela Dados
    pdf.set_font("Arial", '', 10)
    pdf.set_text_color(0, 0, 0)
    for res in resultados:
        pdf.cell(50, 10, res['Etapa'], border=1)
        pdf.cell(40, 10, f"R$ {res['Custo_Unitario']:.2f}", border=1, align='C')
        pdf.cell(30, 10, str(int(res['Consumo_Mes'])), border=1, align='C')
        pdf.cell(45, 10, f"R$ {res['Custo_Total_Etapa']:.2f}", border=1, align='C')
        pdf.ln()
        
    # Tabela Total
    pdf.set_font("Arial", 'B', 10)
    pdf.set_fill_color(230, 240, 250)
    pdf.cell(120, 10, "CUSTO TOTAL DO APP", border=1, fill=True, align='R')
    pdf.cell(45, 10, f"R$ {custo_total_app:.2f}", border=1, fill=True, align='C')
    pdf.ln(15)
    
    # Inserção do Gráfico
    pdf.image("grafico_pizza_temp.png", x=35, w=140)
    
    # Conclusões Qualitativas
    pdf.ln(5)
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(0, 10, "Analise de Impacto e Respostas:", ln=True)
    pdf.set_font("Arial", '', 10)
    
    t1 = "1. Qual das quatro etapas custou mais caro?"
    r1 = "Empate entre Desenvolvimento e Suporte Tecnico, custando R$ 4.000,00 cada."
    t2 = "2. Qual o impacto de lançar o aplicativo com menos bugs?"
    r2 = "Menos bugs reduzem o consumo na etapa de Testes (QA). Adicionalmente, isso gera maior estabilidade no aplicativo, o que diminui sensivelmente as reclamacoes, enxugando de forma consideravel os altos custos do Suporte Tecnico."
    
    pdf.multi_cell(0, 7, t1)
    pdf.multi_cell(0, 7, r1)
    pdf.ln(3)
    pdf.multi_cell(0, 7, t2)
    pdf.multi_cell(0, 7, r2)
    
    # Salvando e limpando resquícios
    pdf.output("Resultados.pdf")
    os.remove("grafico_pizza_temp.png")
    print("\n[+] Sucesso: O arquivo 'Resultados.pdf' foi gerado e salvo na mesma pasta!")

def main():
    caminho = "dados_app_delivery.csv" 
    dados = carregar_dados(caminho)
    
    if not dados:
        return
        
    resultados, custo_total = processar_contabilidade(dados)
    
    while True:
        print("\n")
        print("MENU:")
        print("1 - Exibir respostas em terminal")
        print("2 - Gerar pdf com resultados")
        print("3 - Sair")
        print("\n")
        
        opcao = input("Escolha uma opcao: ")
        
        if opcao == '1':
            exibir_terminal(resultados, custo_total)
        elif opcao == '2':
            gerar_pdf(resultados, custo_total)
        elif opcao == '3':
            print("\nFinalizando sistema...\n")
            sys.exit(0)
        else:
            print("\nOpção invalida. Tente novamente.")

if __name__ == "__main__":
    main()