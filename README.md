# Randomização e alocação de implantes

Os scripts geram tabelas para dois modelos de randomização no REDCap:

- `gerar_participantes.py`: `randomizacao_3` recebe grupo `1` (200 mg) ou `2` (300 mg), em blocos de dois.
- `alocacao_medicacao.py`: `randomizacao_4` recebe um kit por participante. A tabela usa `randomizacao_3` como estrato: grupo `1` recebe cinco implantes identificados como 200 mg e grupo `2` recebe três identificados como 300 mg.

A tabela de implantes tem as colunas do template estratificado: `redcap_randomization_number`, `redcap_randomization_group` (vazia, conforme permitido para o campo de texto) e `randomizacao_3`. A seleção do kit depende do estrato registrado no REDCap, não da ordem das linhas entre os dois arquivos.

Na raiz do projeto, execute:

```sh
python src/scritps_randomizacao/gerar_participantes.py
python src/scritps_randomizacao/alocacao_medicacao.py
```

O segundo comando gera `src/csv/alocacao_medicacao_estratificada.csv`, sem substituir o arquivo de medicação anterior. O primeiro comando substitui `src/csv/randomizacao_participantes.csv` se ele já existir. Ambos os arquivos gerados devem ser tratados como tabelas de teste.

Antes do uso, confirme no REDCap que o modelo de `randomizacao_4` está configurado com `randomizacao_3` como estrato, importe as tabelas no ambiente de desenvolvimento e teste participantes fictícios de ambos os grupos, inclusive em ordens diferentes. Confirme também se os códigos e quantidades de implantes correspondem ao estoque físico e se o campo aceita o texto completo do kit. A geração do CSV, por si só, não valida a configuração ou a dispensação.

A semente fixa permite reproduzir as tabelas, mas torna a sequência previsível para quem conhece o código e a semente. Proteja as tabelas de alocação e valide o procedimento de randomização e o estoque com os responsáveis pelo estudo antes de qualquer uso real.