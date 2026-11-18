# classes.py
import sqlite3
from datetime import date
from decimal import Decimal

class Tecnico:
    def __init__(self, matricula: str, nome: str, setor: str = None):
        self.matricula = matricula
        self.nome = nome
        self.setor = setor
        # inserir mais fatores conforme o necessario


class Equipamento:
    def __init__(self, codigo_tag: str, descricao: str, fabricante: str = None):
        self.codigo_tag = codigo_tag
        self.descricao = descricao
        self.fabricante = fabricante
        # inserir mais fatores conforme o necessario


class Medicao:
    def __init__(self, id_tecnico: int, id_equipamento: int, data_calibracao: str, params: list = None):
        self.id_tecnico = id_tecnico
        self.id_equipamento = id_equipamento
        self.data_calibracao = data_calibracao
        self.params = params if params else []
        self.status_final = None

    def validar_tolerancias(self):
        """Validação metrológica completa de todas as medições."""
        for p in self.params:
            if p["valor_obtido"] is None or p["valor_obtido"] == 0:
                p["status"] = "REPROVADO"
                p["motivo"] = "Valor obtido inválido (zero)"
                continue
            tolerancia_percentual = Decimal(str(p["tolerancia"]))       # tolerancia calculada baseado no valor percentual (e.g tolerancia 0.5 significa 0.5% sobre o valor nominal)

            valor_nominal = Decimal(str(p["valor_nominal"]))
            valor_obtido = Decimal(str(p["valor_obtido"]))

            tolerancia_absoluta = valor_nominal * (tolerancia_percentual / Decimal("100"))

            diferenca = abs(valor_obtido - valor_nominal)
            if diferenca <= tolerancia_absoluta:
                p["status"] = "APROVADO"
            else:
                p["status"] = "REPROVADO"
                
        self.status_final = "APROVADO" if all(p["status"] == "APROVADO" for p in self.params) else "REPROVADO"


class ConexaoDB:
    def __init__(self, db_path: str = "database/03_banco.db"):
        self.db_path = db_path
        self.conn = sqlite3.connect(self.db_path)
        self.conn.row_factory = sqlite3.Row
        self.c = self.conn.cursor()
        self.criar_tabelas()

    def criar_tabelas(self):
        self.c.execute('''
            CREATE TABLE IF NOT EXISTS tecnico (
                id_tecnico INTEGER PRIMARY KEY AUTOINCREMENT,
                matricula TEXT UNIQUE NOT NULL,
                nome TEXT NOT NULL,
                setor TEXT
            )
        ''')
        self.c.execute('''
            CREATE TABLE IF NOT EXISTS equipamento (
                id_equipamento INTEGER PRIMARY KEY AUTOINCREMENT,
                codigo_tag TEXT UNIQUE NOT NULL,
                descricao TEXT,
                fabricante TEXT
            )
        ''')
        self.c.execute('''
            CREATE TABLE IF NOT EXISTS medicao (
                id_medicao INTEGER PRIMARY KEY AUTOINCREMENT,
                id_tecnico INTEGER,
                id_equipamento INTEGER,
                data_calibracao TEXT,
                status_final TEXT,
                FOREIGN KEY (id_tecnico) REFERENCES tecnico(id_tecnico),
                FOREIGN KEY (id_equipamento) REFERENCES equipamento(id_equipamento)
            )
        ''')
        self.conn.commit()

    def inserir_tecnico(self, tecnico: Tecnico) -> int:
        self.c.execute('''
            INSERT INTO tecnico (matricula, nome, setor)
            VALUES (?, ?, ?)
        ''', (tecnico.matricula, tecnico.nome, tecnico.setor))
        self.conn.commit()
        return self.c.lastrowid

    def inserir_equipamento(self, equipamento: Equipamento) -> int:
        self.c.execute('''
            INSERT INTO equipamento (codigo_tag, descricao, fabricante)
            VALUES (?, ?, ?)
        ''', (equipamento.codigo_tag, equipamento.descricao, equipamento.fabricante))
        self.conn.commit()
        return self.c.lastrowid

    def inserir_medicao(self, medicao: Medicao) -> int:
        self.c.execute('''
            INSERT INTO medicao (id_tecnico, id_equipamento, data_calibracao, status_final)
            VALUES (?, ?, ?, ?)
        ''', (medicao.id_tecnico, medicao.id_equipamento, medicao.data_calibracao, medicao.status_final))
        self.conn.commit()
        return self.c.lastrowid

    def obter_medicoes_completo(self, id_equipamento: int = None):
        query = '''
            SELECT 
                m.id_medicao, m.data_calibracao, m.status_final,
                t.nome as tecnico_nome, t.matricula,
                e.codigo_tag, e.descricao, e.fabricante
            FROM medicao m
            JOIN tecnico t ON m.id_tecnico = t.id_tecnico
            JOIN equipamento e ON m.id_equipamento = e.id_equipamento
        '''
        params = []
        if id_equipamento:
            query += " WHERE m.id_equipamento = ?"
            params.append(id_equipamento)
        self.c.execute(query, params)
        return self.c.fetchall()

    def fechar(self):
        self.conn.close()
