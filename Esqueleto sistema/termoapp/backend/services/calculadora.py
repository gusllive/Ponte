import numpy as np
from core.constantes import R_IG_BAR
from models.component import Componente


class CalculadoraTermodinamica:
    def __init__(self, componente: Componente):
        self.comp = componente

    def calcular_propriedades_reduzidas(self, T: float, P: float):
        Tr = T / self.comp.Tc
        Pr = P / self.comp.Pc
        return Tr, Pr

    # --- Método da Equação Virial (Pitzer 2 Coeficientes) ---
    def calcular_Z_Pitzer_2c(self, T: float, P: float) -> dict:
        Tr, Pr = self.calcular_propriedades_reduzidas(T, P)
        
        B0 = 0.083 - (0.422 / (Tr ** 1.6))
        B1 = 0.139 - (0.172 / (Tr ** 4.2))
        
        Z0 = 1 + B0 * (Pr / Tr)
        Z1 = B1 * (Pr / Tr)
        Z = Z0 + self.comp.omega * Z1
        
        # Exemplo de cálculo de volume molar derivado usando nossa constante do core
        V = (Z * R_IG_BAR * T) / P if P > 0 else 0
        
        return {
            "componente": self.comp.nome,
            "Tr": round(Tr, 4),
            "Pr": round(Pr, 4),
            "Z0": round(Z0, 5),
            "Z1": round(Z1, 5),
            "Z_final": round(Z, 5),
            "V_molar": round(V, 2)
        }

    # --- Método Lee Kesler utilizando as tabelas pré-carregadas ---
    @staticmethod
    def f_interp_F1(x0, x, y):
        return float(((x[1] - x0)/(x[1] - x[0]))*y[0] + ((x0 - x[0])/(x[1] - x[0]))*y[1])

    @classmethod
    def f_interp_F2(cls, x0, x, y1, y2, z0, z):
        z1 = cls.f_interp_F1(x0, x, y1)
        z2 = cls.f_interp_F1(x0, x, y2)
        return cls.f_interp_F1(z0, z, (z1, z2))

    def calcular_Z_Lee_Kesler(self, T: float, P: float, tabelas_lk: dict) -> dict:
        Tr, Pr = self.calcular_propriedades_reduzidas(T, P)
        
        Z0_dados = tabelas_lk['Z0']
        Z1_dados = tabelas_lk['Z1']
        Pr_dados = tabelas_lk['Pr']

        v_Pr = Pr_dados['Pr'].to_numpy()
        v_Tr = Z0_dados['Tr'].to_numpy()

        i = np.searchsorted(v_Tr, Tr, 'left')
        j = np.searchsorted(v_Pr, Pr, 'left')

        x0, x = Tr, (v_Tr[i-1], v_Tr[i])
        z0, z = Pr, (v_Pr[j-1], v_Pr[j])

        y1_0 = (Z0_dados.loc[i-1].to_numpy()[j-1], Z0_dados.loc[i].to_numpy()[j-1])
        y2_0 = (Z0_dados.loc[i-1].to_numpy()[j], Z0_dados.loc[i].to_numpy()[j])
        Z_0 = self.f_interp_F2(x0, x, y1_0, y2_0, z0, z)

        y1_1 = (Z1_dados.loc[i-1].to_numpy()[j-1], Z1_dados.loc[i].to_numpy()[j-1])
        y2_1 = (Z1_dados.loc[i-1].to_numpy()[j], Z1_dados.loc[i].to_numpy()[j])
        Z_1 = self.f_interp_F2(x0, x, y1_1, y2_1, z0, z)

        Z_lk = Z_0 + self.comp.omega * Z_1
        return {"Z_final": round(Z_lk, 5), "Z0": round(Z_0, 5), "Z1": round(Z_1, 5)}