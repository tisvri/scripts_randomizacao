import csv
import random
import os


SEED = 42 # TOAAAAAAAAALLHA 🎒👨‍🚀🚀
# SEED = 8001 # É MAIS DE 8MIL 🫪

TOTAL_BLOCOS = 20
GRUPOS = ["1", "2"]




# Gerar caso não exista o diretório de saída, com a pasta denominada 'csv'
CAMINHO_SAIDA = f'src/csv-{SEED}'
if not os.path.exists(CAMINHO_SAIDA):
    os.makedirs(CAMINHO_SAIDA)

ARQUIVO_SAIDA = os.path.join(CAMINHO_SAIDA, f'randomizacao_participantes_{SEED}.csv')

def gerar_randomizacao_participantes(seed: int, arquivo_csv: str) -> None:
    """Gera a randomização dos participantes e salva em um arquivo CSV.

    Args:
        seed (int): Semente para o gerador de números aleatórios.
        arquivo_csv (str): Caminho do arquivo CSV de saída.
    """
    rng = random.Random(seed)
    
    total_blocos = TOTAL_BLOCOS
    grupos_base = GRUPOS.copy()
    
    #-----------------------------------------------
    # PADRÃO REDCAP
    linhas = []
    for _ in range(total_blocos):
        bloco_atual = grupos_base.copy()
        rng.shuffle(bloco_atual)
        
        for codigo_grupo in bloco_atual:
            linhas.append({
                "redcap_randomization_number": "", # Opcional para single-select (open allocation)
                "redcap_randomization_group": codigo_grupo
            })
    
    colunas = ["redcap_randomization_number", "redcap_randomization_group"]
    #utf-8-sig  mantém a compatibilidade com o Excel ao abrir arquivos CSV, identico ao template do REDCAP
    with open(arquivo_csv, mode='w', newline="", encoding='utf-8-sig') as f:
        writer = csv.DictWriter(f, fieldnames=colunas)
        writer.writeheader()
        writer.writerows(linhas)
    
    print(f"[OK] '{arquivo_csv}' gerado com {len(linhas)} linhas (20x grupo 1 [200mg] e 20x grupo 2 [300mg]).")
    
    
    
if __name__ == "__main__":
    gerar_randomizacao_participantes(SEED, ARQUIVO_SAIDA)
    

    
    
    