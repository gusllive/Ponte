class Componente: 
    def __init__(self, nome: str, Tc: float, Pc: float, omega: float):
        self.nome   = nome    
        self.Tc     = Tc    # Temperatura crítica (K)
        self.Pc     = Pc    # Pressão Crítica (bar)
        self.omega  = omega # Fator Acêntrico