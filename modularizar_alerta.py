import os

# Estrutura modularizada para o projeto Alerta de Onibus
# Cada módulo com responsabilidade única

BASE_DIR = r"C:\Users\yuri\OneDrive\Desktop\Claude\AlertaDeOnibus"
os.makedirs(os.path.join(BASE_DIR, "src"), exist_ok=True)

# 1. config.py - Configurações e rotas/paradas de Belém
config_py = r'''# Configurações do Alerta de Ônibus — Belém (UFPA-Pedreira)

ROTAS = {
    "ufpa-pedreira": {
        "nome": "UFPA - Pedreira",
        "paradas_ida": [
            "Terminal UFPA (Portão I)",
            "Av. Perimetral (HUAPA)",
            "Av. Bernardo Sayão",
            "Av. Gentil Bittencourt",
            "Praça do Relógio / Pedreira"
        ],
        "paradas_volta": [
            "Pedreira (Praça Brasil)",
            "Av. Pedro Álvares Cabral",
            "Av. Almirante Barroso",
            "Av. Perimetral (Saída)",
            "Terminal UFPA"
        ]
    }
}

VELOCIDADE_MEDIA_MS = 6.0 # ~21 km/h em Belém nos horários de pico
VELOCIDADE_CAMINHADA_MS = 1.2 # ~4.3 km/h (~80m/min)
'''

with open(os.path.join(BASE_DIR, "src", "config.py"), "w", encoding="utf-8") as f:
    f.write(config_py)

# 2. simulador_api.py - Simula chamadas ao Vem Busão / GPS em tempo real
simulador_py = r'''import random
from src.config import ROTAS, VELOCIDADE_MEDIA_MS

class VemBusaoAPI:
    @staticmethod
    def consultar_veiculos(linha):
        # Simula a posição dos ônibus da linha UFPA-Pedreira em metros a partir da origem
        # Em produção, aqui entraria a requisição HTTP real para a API do Vem Busão Belém
        posicoes_ficticias = [random.randint(500, 4500) for _ in range(3)]
        return {
            "linha": ROTAS.get(linha, {}).get("nome", linha),
            "veiculos_ativos": len(posicoes_ficticias),
            "distancias_metros": posicoes_ficticias
        }
'''

with open(os.path.join(BASE_DIR, "src", "simulador_api.py"), "w", encoding="utf-8") as f:
    f.write(simulador_py)

# 3. calculador.py - Algoritmos de cálculo de tempo e decisão de saída
calculador_py = r'''from src.config import VELOCIDADE_CAMINHADA_MS, VELOCIDADE_MEDIA_MS

def calcular_tempo_saida(distancia_casa_m, distancia_onibus_m):
    tempo_caminhada_min = (distancia_casa_m / VELOCIDADE_CAMINHADA_MS) / 60.0
    tempo_onibus_min = (distancia_onibus_m / VELOCIDADE_MEDIA_MS) / 60.0

    diff = tempo_onibus_min - tempo_caminhada_min

    if diff > 2.0:
        recomendacao = "Pode Relaxar! O ônibus está vindo com folga."
        minutos_espera = round(tempo_onibus_min - tempo_caminhada_min, 1)
        status = "ok"
    elif 0.0 <= diff <= 2.0:
        recomendacao = "Atenção Imediata! Saia agora mesmo para não perder."
        minutos_espera = 0
        status = "atencao"
    else:
        recomendacao = "Cuidado! Este ônibus vai passar antes de você chegar. Espere o próximo."
        minutos_espera = round(tempo_onibus_min, 1)
        status = "perigo"

    return {
        "tempo_caminhada_min": round(tempo_caminhada_min, 1),
        "tempo_onibus_min": round(tempo_onibus_min, 1),
        "recomendacao": recomendacao,
        "status": status,
        "minutos_para_sair": max(0, round(tempo_onibus_min - tempo_caminhada_min - 1, 1))
    }
'''

with open(os.path.join(BASE_DIR, "src", "calculador.py"), "w", encoding="utf-8") as f:
    f.write(calculador_py)

# 4. main.py - Ponto de entrada CLI / GUI python e integrador do projeto
main_py = r'''import sys
import os

# Garantir importações locais
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.config import ROTAS
from src.simulador_api import VemBusaoAPI
from src.calculador import calcular_tempo_saida

def main():
    print("==================================================")
    print("      ALERTA DE ÔNIBUS — BELÉM (UFPA-PEDREIRA)    ")
    print("==================================================")

    linha = "ufpa-pedreira"
    distancia_casa = 450 # metros

    print(f"\nConsultando o sistema 'Vem Busão' para a linha: {ROTAS[linha]['nome']}...")
    dados = VemBusaoAPI.consultar_veiculos(linha)

    print(f"Veículos ativos na rota: {dados['veiculos_ativos']}")

    # Pegar o ônibus mais próximo
    distancia_onibus = min(dados['distancias_metros'])
    print(f"Ônibus mais próximo a ~{distancia_onibus} metros da sua parada.")

    resultado = calcular_tempo_saida(distancia_casa, distancia_onibus)

    print("\n--- RELATÓRIO INTELIGENTE DE SAÍDA ---")
    print(f"Sua caminhada estimada: {resultado['tempo_caminhada_min']} minutos")
    print(f"Chegada estimada do ônibus: {resultado['tempo_onibus_min']} minutos")
    print(f"Status: {resultado['status'].upper()}")
    print(f"Recomendação: {resultado['recomendacao']}")
    if resultado['status'] == 'ok':
        print(f"👉 Dica: Saia daqui a {resultado['minutos_para_sair']} minutos.")
    print("==================================================")

if __name__ == "__main__":
    main()
'''

with open(os.path.join(BASE_DIR, "main.py"), "w", encoding="utf-8") as f:
    f.write(main_py)

print("Modularização concluída com sucesso na pasta AlertaDeOnibus!")
