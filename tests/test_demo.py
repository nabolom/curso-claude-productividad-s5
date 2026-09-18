import json
import unittest
from pathlib import Path

from demo_hill_climbing import ACCOUNT, REFERENCE_RUN, ejecutar_demo, evaluar_mensaje


class DemoHillClimbingTests(unittest.TestCase):
    def setUp(self) -> None:
        with Path(REFERENCE_RUN).open(encoding="utf-8") as archivo:
            self.referencia = json.load(archivo)

    def test_la_metrica_reproduce_los_cinco_puntajes_publicados(self) -> None:
        puntajes = [
            evaluar_mensaje(registro["mensaje"], ACCOUNT)["tasa_respuesta"]
            for registro in self.referencia["historial"]
        ]
        self.assertEqual(puntajes, [5.0, 50.0, 62.0, 62.0, 70.0])

    def test_el_grafo_replay_conserva_el_mejor_resultado(self) -> None:
        resultado = ejecutar_demo(modo="replay", max_iteraciones=5)
        intentos = [registro["metrica"] for registro in resultado["historial"]]
        mejores = [
            punto["mejor_acumulado"] for punto in resultado["curva_mejor_acumulado"]
        ]

        self.assertEqual(intentos, [5.0, 50.0, 62.0, 62.0, 70.0])
        self.assertEqual(mejores, [5.0, 50.0, 62.0, 62.0, 70.0])
        self.assertEqual(resultado["mejor_metrica"], 70.0)
        self.assertEqual(resultado["iteracion"], 5)
        self.assertEqual(resultado["modo"], "replay")

    def test_el_modo_replay_no_admite_mas_borradores_que_la_referencia(self) -> None:
        with self.assertRaises(ValueError):
            ejecutar_demo(modo="replay", max_iteraciones=6)


if __name__ == "__main__":
    unittest.main()
