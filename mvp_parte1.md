# mvp_parte1.md

# MVP Parte 1 - Projeto Aplicado I
## Schulz S.A. - Automação de Certificados de Calibração

---

## 1. Introdução

Esta entrega implementa o **MVP (Minimum Viable Product)** da solução proposta para a Schulz S.A.  
O objetivo é criar um sistema simples que receba medições de calibração, valida automaticamente contra as tolerâncias metrológicas e gere o certificado oficial, substituindo o fluxo manual das planilhas Excel.

Todas as regras de negócio (validação de tolerâncias, status "APROVADO"/"REPROVADO") estão 100% encapsuladas dentro das classes de domínio, garantindo integridade e segurança para o banco de dados.

---

## 2. Arquitetura em Programação Orientada a Objetos (POO)

### Padrões utilizados
- **Encapsulamento**: Todos os atributos e regras de negócio (validação de tolerâncias) estão dentro das classes.
- **Abstração**: Classes `Tecnico`, `Equipamento` e `Medicao` representam conceitos reais do domínio da metrologia.
- **Separação de responsabilidades**: A classe `ConexaoDB` é responsável exclusivamente pelo acesso e persistência ao SQLite.
- **Reutilização e manutenção**: Fácil de estender (adicionar mais parâmetros, outros tipos de instrumentos, integração com API, etc.).

### Diagrama das classes
┌─────────────────────┐

│|      Tecnico      |│

├─────────────────────┤

│ - matricula: str    │

│ - nome: str         │

│ - setor: str        │

│ - init(...)         │

└─────────────────────┘
┌─────────────────────┐

│|    Equipamento    |│

├─────────────────────┤

│ - codigo_tag: str   │

│ - descricao: str    │

│ - fabricante: str   │

│ - init(...)         │

└─────────────────────┘
┌────────────────────────┐

│|       Medicao        |│

├────────────────────────┤

│ - id_tecnico: int      │

│ - id_equipamento: int  │

│ - data_calibracao: str │

│ - params: list[dict]   │

│ - status_final: str    │

│ - validar_tolerancias()│

│ - init(...)            │

└────────────────────────┘
┌────────────────────────────┐

│|        ConexaoDB         |│

├────────────────────────────┤

│ - db_path: str             │

│ - conn: sqlite3            │

│ - criar_tabelas()          │

│ - inserir_tecnico()        │

│ - inserir_equipamento()    │

│ - inserir_medicao()        │

│ - obter_medicoes_completo()│

│ - fechar()                 │

└────────────────────────────┘



---

## 3. Regras de Negócio Implementadas (Metrologia)

- Validação de tolerância: `diferenca <= tolerancia_percentual * valor_nominal`
- Status final do certificado: "APROVADO" se **todos** os parâmetros estiverem aprovados
- Tratamento de erros SQL e valores inválidos (zero, None)
- Histórico completo (JOIN entre Técnico, Equipamento e Medição)

---

## 4. Fluxo de Execução do MVP

1. Criação dos objetos de domínio (`Tecnico`, `Equipamento`, `Medicao`)
2. Validação automática das tolerâncias dentro da classe `Medicao`
3. Inserção dos dados no SQLite via `ConexaoDB`
4. Consulta com JOIN e impressão formatada do certificado no terminal

---

## 5. Testes e Demonstração

O script `main.py` contém dados de teste reais de calibração (pressão e temperatura). Ao executar, o programa gera o certificado completo com status final.

**Exemplo de saída esperado:**

CERTIFICADO DE CALIBRAÇÃO - SCHULZ S.A.

Data da calibração: 2026-7-27

Técnico: João da Silva (Matricula: T987)

Equipamento: E-6767 - Manômetro Digital (Fluke)

PARÂMETROS MENSURADOS:

• Pressão (bar): 10.01 (nominal 10.0) | Status: APROVADO

• Pressão (bar): 4.99 (nominal 5.0) | Status: APROVADO

• Temperatura (°C): 19.9 (nominal 20.0) | Status: APROVADO

STATUS FINAL DO CERTIFICADO: APROVADO


---

## 6. Conclusão

Atendendo aos requisitos da Entrega 03:
- 3 classes de domínio com lógica de negócio
- Conexão com SQLite
- Validação metrológica automática
- Relatório de certificado
