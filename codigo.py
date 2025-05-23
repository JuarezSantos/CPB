# %%
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())

# %%
from crewai import Agent, Task, Crew

# %% [markdown]
# ### Agentes
# 
# - Analista       ---ScenarioCollectorAgent---
# - Modelador      ---BDDModelerAgent---
# - Automatizador  ---AutomationCoderAgent--- 
# - Executor       ---TestExecutorAgent---
# - Orquestrador   ---CiCdOrchestratorAgent---
# 
# 
# 

# %%
analista = Agent(
    role="Levantador de Cenários de Testes",
    goal="Analisar a {historia} do usuário e levantar todos os cenários de testes, incluindo casos positivos e negativos.",
    backstory="""
        Você é um analista de testes experiente, especializado em identificar cenários de testes detalhados com base em histórias de usuários. 
        Sua missão é analisar cuidadosamente a {historia} fornecida e extrair todos os caminhos possíveis de execução, considerando fluxos alternativos, exceções e validações.
    """,
    allow_delegation=False,
    verbose=True
)

# %%
modelador = Agent(
    role="Modelador BDD",
    goal="Fazer a modelagem de todos os cenários levantados pelo Lavantador.",
    backstory="""
        Você é um analista de testes especializado, em Modelagem do tipo BDD. 
        Sua missão é modelar cuidadosamente os cenários levantados de maneira que fique facil a sua automação.
""",
    allow_delegation=False,
    verbose=True

)

# %%
automatizador = Agent(
    role="Automatizador de Testes",
    goal="Automatizar, com Cypress, os cenários modelados em BDD pelo Modelador.",
    backstory="""
        Você é um especialista em automação de testes, com foco no framework Cypress.
        Sua missão é implementar os testes automatizados com base nos cenários BDD escritos pelo Modelador,
        garantindo código limpo, de fácil manutenção e execução rápida, seguindo boas práticas de automação.
    """,
    allow_delegation=False,
    verbose=True
)

# %%
executor = Agent(
    role="Executor de Testes",
    goal="Executar os testes automatizados e retornar logs e evidências de execução.",
    backstory="""
        Você é responsável por executar os testes automatizados com Cypress e relatar os resultados de forma clara e objetiva.
        Utilize o comando `npx cypress run` para realizar a execução dos testes e gere um relatório contendo:
        - O status de cada teste (passou/falhou)
        - Prints de tela, quando disponíveis
        - Logs de execução completos
    """,
    allow_delegation=False,
    verbose=True
)

# %%
orquestrador = Agent(
    role="Orquestrador de Testes",
    goal="Coordenar a cadeia de automação de testes entre os agentes especializados.",
    backstory="""
        Você é um agente orquestrador responsável por organizar e controlar a execução da pipeline de testes.
        Sua função é passar os resultados de cada agente para o próximo, garantindo que cada etapa da automação seja concluída com sucesso.
        Comece com uma história de usuário, envie-a para o Levantador de Cenários, e continue o fluxo até a execução final dos testes.
    """,
    allow_delegation=True,
    verbose=True
)

# %%
levantar_cenarios = Task(
    description=(
        "1. Levantar cenários positivos de fluxo principal com base na história: {historia}.\n"
        "2. Levantar cenários negativos (fluxos alternativos e inválidos).\n"
        "3. Levantar cenários para validação de campos obrigatórios.\n"
        "4. Levantar cenários de exceção e falhas esperadas do sistema."
    ),
    expected_output="Documento estruturado contendo todos os cenários baseados na história: {historia}.",
    agent=analista
)

# %%
modelar_cenarios = Task(
    description=(
        "1. Modelar todos os cenários utilizando a abordagem BDD (Behavior Driven Development), com base na história: {historia}.\n"
        "2. Utilizar o formato Gherkin: Given/When/Then para cada cenário identificado."
    ),
    expected_output="Documento estruturado contendo todos os cenários modelados no formato BDD com base na história: {historia}.",
    agent=modelador
)

# %%
automatizar_cenarios = Task(
    description=(
        "1. Você é um especialista em automação de testes, com foco no framework Cypress.\n"
        "2. Sua tarefa é implementar os testes automatizados com base nos cenários BDD escritos pelo Modelador.\n"
        "3. Garantir código limpo, de fácil manutenção e execução rápida.\n"
        "4. Seguir boas práticas de automação e padrões de organização de testes (Page Objects, Fixtures, etc.)."
    ),
    expected_output="Gerar Código-fonte automatizado em Cypress, organizado por funcionalidades e baseado nos cenários BDD.",
    agent=automatizador
)

# %%
executar_testes = Task(
    description=(
        "1. Executar todos os cenários de Testes.\n"
        "2. Evidenciar todas as execuções de testes com capturas de tela ou logs detalhados.\n"
        "3. Gerar relatórios de execução com status (sucesso/falha) para cada cenário.\n"
        "4. Gerar documentação consolidada com o andamento completo da execução dos testes, "
        "incluindo métricas, falhas e evidências visuais."
    ),
    expected_output="Relatórios detalhados e documentação gerada com base nas execuções automatizadas dos testes.",
    agent=executor
)

# %%
orquestrar_testes = Task(
    description=(
        "1. Coordenar as etapas para que ocorram na ordem correta.\n"
        "2. Certificar que cada etapa está sendo executada conforme o planejado.\n"
        "3. Garantir que cada agente tenha a documentação necessária para executar suas tarefas."
    ),
    expected_output="Consolidar todas as documentações geradas em cada etapa em um único relatório de qualidade.",
    agent=orquestrador
)

# %%
crew = Crew(
    agents = [analista, modelador, automatizador, executor, orquestrador],
    tasks = [levantar_cenarios, modelar_cenarios, automatizar_cenarios, executar_testes, orquestrar_testes],
    verbose = True
)
# %%
crew


