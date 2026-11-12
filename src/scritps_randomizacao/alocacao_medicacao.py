import csv
import random
import os

SEED = 42 # TOAAAAAAAAALLHA 🎒👨‍🚀🚀
# SEED = 8001 # É MAIS DE 8MIL 🫪

TOTAL_BLOCOS = 20

REGRAS_DOSE_IMPLANTES = {
    "2": 3, # 300mg -> 3 implantes (0001 a 0060)
    "1": 5  # 200mg -> 5 implantes (0001 a 0100)
}

# Gerar caso não exista o diretório de saída, com a pasta denominada 'csv'
CAMINHO_SAIDA = f'src/csv-{SEED}'
if not os.path.exists(CAMINHO_SAIDA):
    os.makedirs(CAMINHO_SAIDA)
ARQUIVO_SAIDA = os.path.join(CAMINHO_SAIDA, f'alocacao_medicacao_estratificada_{SEED}.csv')

# Defina False se quiser entrega sequencial (0001, 0002, 0003...) dentro de cada grupo
# Defina True se quiser sortear a ordem dos implantes dentro de cada grupo
EMBARALHAR_DENTRO_DA_FAIXA = True

def gerar_alocacao_medicacao(seed: int, arquivo_csv: str) -> None:
    rng_blocos = random.Random(seed)
    
    rng_implantes = random.Random(seed + 1)
    
    total_blocos = TOTAL_BLOCOS
    
    grupos_base = list(REGRAS_DOSE_IMPLANTES.keys())
    
    #1. criação dos dois estoques separados por faixa numérica
    estoque_por_grupo = {
        "2": [f"300MG-{i:04d}" for i in range (1, REGRAS_DOSE_IMPLANTES["2"] * TOTAL_BLOCOS + 1)],
        "1": [f"200MG-{i:04d}" for i in range (1, REGRAS_DOSE_IMPLANTES["1"] * TOTAL_BLOCOS + 1)]
    }
    if EMBARALHAR_DENTRO_DA_FAIXA:
        rng_implantes.shuffle(estoque_por_grupo["2"])
        rng_implantes.shuffle(estoque_por_grupo["1"])
    
    # Ponteiras independentes para controlar o consumo de cada estoque
    indice_por_grupo = {
        "1": 0,
        "2": 0
    }
    linhas = []
    
    for _ in range(total_blocos):
        bloco_atual = grupos_base.copy()
        rng_blocos.shuffle(bloco_atual)
        
        for codigo_grupo in bloco_atual:
            qtd = REGRAS_DOSE_IMPLANTES[codigo_grupo]
            inicio = indice_por_grupo[codigo_grupo]
            fim = inicio + qtd
            
            implantes_alocados = estoque_por_grupo[codigo_grupo][inicio:fim]
            indice_por_grupo[codigo_grupo] = fim
            
            linhas.append({
                "redcap_randomization_number": " | ".join(implantes_alocados),
                "redcap_randomization_group": "",
                "randomizacao_3": codigo_grupo,
            })

    colunas = ["redcap_randomization_number", "redcap_randomization_group", "randomizacao_3"]
        
        
        
        
    with open(arquivo_csv, mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=colunas)
        writer.writeheader()
        writer.writerows(linhas)
        
    print(f"[OK] Arquivo '{arquivo_csv}' gerado com {len(linhas)} alocações ({sum(REGRAS_DOSE_IMPLANTES[grupo] * TOTAL_BLOCOS for grupo in REGRAS_DOSE_IMPLANTES)} implantes distribuídos).")


if __name__ == "__main__":
    gerar_alocacao_medicacao(SEED, ARQUIVO_SAIDA)
