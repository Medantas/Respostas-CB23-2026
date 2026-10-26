"""Seus testes do Marco 3 (veja a seção 5 do ENUNCIADO_MARCO3.md).

Regras: pelo menos 4 testes seus (o exemplo abaixo não conta), uma docstring em cada teste
dizendo qual caso ele cobre, e floats comparados com assertAlmostEqual ou math.isclose, a não
ser que a igualdade exata seja justamente o que você quer testar.
"""
import math
import unittest

from elevatoria.raizes import Bisseccao, Newton


class TestBisseccaoExemplo(unittest.TestCase):
    """Exemplo do formato. `Bisseccao` é código existente da base."""

    def test_raiz_na_ponta(self):
        """Se f(a) já é zero, a bissecção devolve a sem iterar."""
        resultado = Bisseccao().encontrar(lambda x: x - 1.0, 1.0, 3.0)
        self.assertEqual((resultado.raiz, resultado.iteracoes), (1.0, 0))


class TestNewtonRegressao(unittest.TestCase):
    """Testes de regressão da issue #9: o Newton precisa recalcular a derivada a cada passo."""

    def test_recalcula_a_derivada_a_cada_iteracao(self):
        """Issue #9: a derivada é avaliada uma vez por iteração, e não uma vez só."""
        chamadas = []

        def df(x):
            chamadas.append(x)
            return 2.0 * x

        resultado = Newton(tol=1e-10, df=df).encontrar(lambda x: x * x - 2.0, 0.0, 4.0)
        self.assertEqual(len(chamadas), resultado.iteracoes)

    def test_converge_em_poucas_iteracoes(self):
        """Issue #9: x² - 2 a partir de 2 converge quadraticamente, em no máximo 6 iterações."""
        resultado = Newton(tol=1e-10).encontrar(lambda x: x * x - 2.0, 0.0, 4.0)
        self.assertAlmostEqual(resultado.raiz, math.sqrt(2.0), places=9)
        self.assertLessEqual(resultado.iteracoes, 6)


if __name__ == "__main__":
    unittest.main()