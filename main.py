# main.py
from datetime import date
from decimal import Decimal
from classes import *

# ======================== DADOS DE TESTE (exemplo) ========================
tecnico = Tecnico(matricula="T987", nome="João da Silva ", setor="Manutenção")
equipamento = Equipamento(codigo_tag="E-6767", descricao="Manômetro Digital", fabricante="Fluke")

medicoes = [
    Medicao(
        id_tecnico=1,
        id_equipamento=1,
        data_calibracao="2026-7-28",
        params=[
            {
                "parametro": "Pressão (bar)",
                "valor_nominal": 10.0,
                "tolerancia": 2.0,
                "valor_obtido": 10.02,
            },
            {
                "parametro": "Pressão (bar)",
                "valor_nominal": 5.0,
                "tolerancia": 1.5,
                "valor_obtido": 4.925,
            },
            {
                "parametro": "Temperatura (°C)",
                "valor_nominal": 20.0,
                "tolerancia": 0.5,
                "valor_obtido": 19.8,
            },
        ]
    )
]       # em situacao real, poderiam ser obtidos valores por metodo de input()

# ======================== EXECUÇÃO ========================
db = ConexaoDB()

# inserir dados (IDs gerados automaticamente)
id_tecnico = db.inserir_tecnico(tecnico)
id_equipamento = db.inserir_equipamento(equipamento)

for m in medicoes:
    m.id_tecnico = id_tecnico
    m.id_equipamento = id_equipamento
    m.validar_tolerancias()

medicao_obj = medicoes[0]
db.inserir_medicao(medicao_obj)

# consulta e print do certificado
resultados = db.obter_medicoes_completo()
print("=" * 70)
print("CERTIFICADO DE CALIBRAÇÃO - SCHULZ S.A.")
print("=" * 70)
print(f"Data da calibração: {resultados[0]['data_calibracao']}")
print(f"Técnico: {resultados[0]['tecnico_nome']} (Matrícula: {resultados[0]['matricula']})")
print(f"Equipamento: {resultados[0]['codigo_tag']} - {resultados[0]['descricao']} ({resultados[0]['fabricante']})")
print("-" * 70)
print("PARÂMETROS MENSURADOS:")
for p in medicoes[0].params:
    print(f"  • {p['parametro']}: {p['valor_obtido']} (nominal {p['valor_nominal']}) | Status: {p['status']}")
print("-" * 70)
print(f"STATUS FINAL DO CERTIFICADO: {medicao_obj.status_final}")
print("=" * 70)

db.fechar()
