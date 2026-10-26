"""Seus testes do Marco 2 (veja a seção 5 do ENUNCIADO_MARCO2.md).

Regras: pelo menos 4 testes seus (o exemplo abaixo não conta), uma docstring em cada teste
dizendo qual caso ele cobre, e floats comparados com assertAlmostEqual, math.isclose ou
np.allclose, a não ser que a igualdade exata seja justamente o que você quer testar.
"""
import unittest
from datetime import datetime

from elevatoria.acumuladores import AcumuladorIngenuo, AcumuladorKahan
from elevatoria.calibracao import CurvaCalibracao
from elevatoria.dados import Registro
from elevatoria.medicao import medir


class TestAcumuladorIngenuoExemplo(unittest.TestCase):
    """Exemplo do formato. `AcumuladorIngenuo` é código existente da base."""

    def test_sem_parcelas(self):
        """Sem nenhuma parcela, o total é zero."""
        self.assertEqual(AcumuladorIngenuo().total, 0.0)


class TestAcumuladorKahanRegressao(unittest.TestCase):
    """Testes de regressão da issue #7: o Kahan precisa compensar o arredondamento."""

    def test_um_milhao_de_pulsos(self):
        """Issue #7: 1 000 000 de pulsos de 0,1 L somam 100000.0 com o Kahan."""
        acumulador = AcumuladorKahan()
        for _ in range(1_000_000):
            acumulador.adicionar(0.1)
        self.assertAlmostEqual(acumulador.total, 100000.0, delta=1e-9)

    def test_mais_preciso_que_o_ingenuo(self):
        """Issue #7: com as mesmas parcelas, o erro do Kahan é menor que o do ingênuo."""
        kahan, ingenuo = AcumuladorKahan(), AcumuladorIngenuo()
        for _ in range(1_000_000):
            kahan.adicionar(0.1)
            ingenuo.adicionar(0.1)
        self.assertLess(abs(kahan.total - 100000.0), abs(ingenuo.total - 100000.0))


class TestMedir(unittest.TestCase):
    """Testes da função `medir` (issue #6), com registros sintéticos."""

    def setUp(self):
        # Curva linear que não muda o valor (contagem = kPa), só para os testes.
        self.curva = CurvaCalibracao([0, 2500, 5000], [0, 2500, 5000], "linear")

    def _registros(self, contagens):
        return [Registro(datetime(2026, 1, 1, 0, 0, i), "INFO", "PT101",
                         {"contagens": float(c)}) for i, c in enumerate(contagens)]

    def test_descarta_leitura_espuria(self):
        """medir: uma leitura absurda (3000 entre valores perto de 100) fica fora da média."""
        contagens = [100, 101, 99, 100, 102, 98, 100, 101, 99, 100, 3000]
        m = medir(self._registros(contagens), "PT101", self.curva)
        self.assertEqual(m.espurias, [10])
        self.assertEqual(m.n_validas, 10)
        self.assertAlmostEqual(m.medida.valor, 100.0)

    def test_u_sistematica_negativa(self):
        """medir: u_sistematica negativa levanta ValueError."""
        with self.assertRaises(ValueError):
            medir(self._registros([100, 101, 99]), "PT101", self.curva, u_sistematica=-1.0)


if __name__ == "__main__":
    unittest.main()
