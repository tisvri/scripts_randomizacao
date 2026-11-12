import csv
import tempfile
import unittest
from collections import Counter
from pathlib import Path
from unittest.mock import patch

from scritps_randomizacao import alocacao_medicacao, gerar_participantes


class TestAlocacaoEstratificada(unittest.TestCase):
    def test_kits_correspondem_aos_grupos_com_ou_sem_embaralhamento(self):
        for embaralhar in (False, True):
            with self.subTest(embaralhar=embaralhar), tempfile.TemporaryDirectory() as diretorio:
                participantes = Path(diretorio) / "participantes.csv"
                medicacao = Path(diretorio) / "medicacao.csv"

                gerar_participantes.gerar_randomizacao_participantes(42, str(participantes))
                with patch.object(alocacao_medicacao, "EMBARALHAR_DENTRO_DA_FAIXA", embaralhar):
                    alocacao_medicacao.gerar_alocacao_medicacao(42, str(medicacao))

                with participantes.open(encoding="utf-8-sig", newline="") as arquivo:
                    grupos = Counter(
                        linha["redcap_randomization_group"] for linha in csv.DictReader(arquivo)
                    )

                with medicacao.open(encoding="utf-8-sig", newline="") as arquivo:
                    leitor = csv.DictReader(arquivo)
                    self.assertEqual(leitor.fieldnames, [
                        "redcap_randomization_number",
                        "redcap_randomization_group",
                        "randomizacao_3",
                    ])
                    kits = list(leitor)

                self.assertEqual(grupos, {"1": 20, "2": 20})
                self.assertEqual(Counter(kit["randomizacao_3"] for kit in kits), grupos)

                implantes = []
                for kit in kits:
                    grupo = kit["randomizacao_3"]
                    itens = kit["redcap_randomization_number"].split(" | ")
                    dose, quantidade = {"1": ("200", 5), "2": ("300", 3)}[grupo]
                    self.assertEqual(kit["redcap_randomization_group"], "")
                    self.assertEqual(len(itens), quantidade)
                    self.assertTrue(all(item.startswith(f"IMPLANTE {dose}MG-") for item in itens))
                    implantes.extend(itens)
                self.assertEqual(len(implantes), 160)
                self.assertEqual(len(set(implantes)), 160)


if __name__ == "__main__":
    unittest.main()
