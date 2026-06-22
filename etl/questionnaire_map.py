QUESTION_MAP = {
    # Bloco B – Gestão da Demanda e Fila de Espera
    "B01":   "Existe lista formal de espera organizada e acessível?",
    "B02":   "As informações sobre a fila de espera são divulgadas à população?",
    "B04":   "São divulgados os critérios de atendimento da lista de espera?",
    "B061":  "Procedimento formal: prevê tentativas de contato com a família e mediação antes de caracterizar evasão?",
    "B062":  "Procedimento formal: prevê comunicação das ausências à SEMED ou Central de Vagas?",
    "B063":  "Procedimento formal: estabelece acionamento do Conselho Tutelar apenas quando há indícios de violação de direitos?",
    # Bloco C – Infraestrutura e Segurança Física
    "C01":   "A recepção/portaria é organizada e há controles de acesso funcionando (portões fechados, adulto responsável visível)?",
    "C02":   "Há muros e portões com tranca de segurança?",
    "C03":   "A unidade possui Alvará/Certificado de Segurança Contra Incêndio e Pânico (ASCIP/CSCIP) válido?",
    "C04":   "Há extintores em condições de uso (válidos e íntegros)?",
    "C041":  "Extintores – validade/manutenção: etiqueta de manutenção vigente (data dentro do prazo)?",
    "C042":  "Extintores – integridade: lacre e pino intactos; sem amassados, corrosão ou vazamento?",
    "C043":  "Extintores – pressão (se houver manômetro): ponteiro na faixa verde?",
    "C044":  "Extintores – mangueira/bico íntegros e rótulo legível (tipo do agente)?",
    "C045":  "Extintores – acesso visível e desobstruído; com placa/adesivo indicando a posição?",
    "C05":   "Possui licença sanitária válida?",
    "C06":   "A unidade mantém Programa de Controle Integrado de Vetores e Pragas com registros (OS/laudo/certificado)?",
    "C061":  "Há data da última dedetização/desratização registrada?",
    "C07":   "Há fraldário em boas condições de uso?",
    "C08":   "Há sanitários infantis com especificações adequadas à faixa etária?",
    "C09":   "Há local para amamentação?",
    "C10":   "Há berçário (para 0–1 ano) ou sala de repouso?",
    "C11":   "Os materiais perigosos estão armazenados em local fechado, identificado e fora do alcance das crianças?",
    "C12_Tipo": "Itens de acessibilidade física presentes na unidade (múltipla escolha agregada)",
    "C13":   "Há acesso à água potável por bebedouros/pontos de consumo em funcionamento, limpos e acessíveis?",
    "C14":   "Há itens estruturais com risco visível?",
    # Bloco D – Ambiente Pedagógico
    "D01":   "Existem materiais pedagógicos e brinquedos disponíveis nas salas, ao alcance das crianças, de uso autônomo e supervisionado?",
    "D02":   "Há materiais de artes/grafismo disponíveis, em bom estado e acessíveis às crianças?",
    "D03":   "Há livros de literatura infantil disponíveis, acessíveis e adequados à faixa etária atendida?",
    "D04":   "Os móveis possuem cantos arredondados ou quinas protegidas para evitar que crianças e bebês se machuquem?",
    "D05":   "Há sala multiuso/brinquedoteca?",
    "D06":   "Brinquedos de uso coletivo intenso estão íntegros e sem riscos aparentes (pontas, rebarbas, partes soltas)?",
    "D07":   "Materiais e brinquedos são acessíveis às diferentes necessidades educacionais?",
    "D08":   "Há espaço suficiente para deslocamento seguro durante a brincadeira (inclusive para quem engatinha)?",
    "D09":   "A rotina das crianças está afixada em mural ou local visível?",
    "D091":  "A rotina afixada prevê momentos diários de brincadeira, uso dos espaços externos, alimentação, descanso e higiene?",
    "D10":   "Há kits de higiene (escova, pasta, sabonete)?",
    "D11":   "Há kit de primeiros socorros disponível, identificado e acessível, com itens íntegros e dentro do prazo de validade?",
    "D12":   "As salas são limpas e bem iluminadas?",
    "D13":   "O parquinho está em boas condições de uso?",
    "D131":  "Parquinho – existe rota acessível até o parquinho (do portão/sala até a área externa)?",
    "D132":  "Parquinho – há rota acessível entre os equipamentos/áreas dentro do parquinho?",
    "D133":  "Parquinho – existem áreas com sombra e áreas ensolaradas disponíveis no espaço externo?",
    "D134":  "Parquinho – os equipamentos estão limpos e conservados?",
    "D135":  "Parquinho – é realizada inspeção diária para retirar objetos estranhos e verificar presença de animais peçonhentos?",
    "D136":  "Parquinho – há piso amortecedor cobrindo toda a zona de queda do equipamento?",
    "D137":  "Parquinho – os equipamentos possuem partes estruturais íntegras (sem trincas, farpas, rebarbas, pontas cortantes)?",
    "D138":  "Parquinho – os equipamentos estão sem pontos evidentes de aprisionamento de cabeça/pescoço/dedos?",
    "D139":  "Parquinho – os equipamentos possuem fixação e ancoragem não expostas (bases firmes, estáveis ao toque)?",
    "D1310": "Parquinho – os equipamentos possuem zonas de queda desobstruídas?",
    "D1311": "Parquinho – há brinquedos acessíveis para crianças com mobilidade reduzida?",
    # Bloco E – Recursos Humanos e Atendimento
    "E01":   "Os professores têm a formação exigida para atuar na Educação Infantil (licenciatura plena ou magistério/curso Normal)?",
    "E02":   "A proporção de crianças por professor habilitado está conforme os limites do CEE-MT para a faixa etária?",
    "E03":   "Quando a turma é multietária, foi adotada a proporção da menor faixa etária presente?",
    "E04":   "Foi realizada capacitação anual em primeiros socorros para professores e funcionários (2025/2026)?",
    "E05":   "Há serviço de Atenção Precoce (multidisciplinar) para crianças com sinais de alerta para o desenvolvimento?",
    "E06":   "Há fluxo/POP definido para casos de suspeita ou confirmação de violência contra crianças?",
    # Bloco F – Comunicação com as Famílias
    "F01":   "Há registros de avaliação do desenvolvimento das crianças?",
    "F02":   "Há elaboração de documentação pedagógica contínua do desenvolvimento (portfólios, relatórios, registros de observação)?",
    "F03":   "As informações sobre o desenvolvimento das crianças são repassadas às famílias?",
    "F04_Tipo": "Forma(s) de comunicação com as famílias adotada(s) pela unidade (múltipla escolha agregada)",
    "F05":   "Está definido o responsável pelo recebimento/entrega das crianças na saída do período escolar?",
    # Bloco G – Alimentação Escolar
    "G01":   "O cardápio é elaborado por nutricionista responsável técnico?",
    "G02":   "A consistência dos alimentos é adequada à faixa etária?",
    "G03":   "As boas práticas de manipulação dos alimentos são adotadas na cozinha/refeitório?",
    "G031":  "Cozinha – piso, paredes e teto possuem revestimento liso, impermeável e lavável, íntegros e sem rachaduras?",
    "G032":  "Cozinha – há abastecimento de água corrente, rede de esgoto ou fossa séptica e ralos sifonados?",
    "G033":  "Cozinha – as caixas de gordura/esgoto estão dimensionadas e em bom estado, fora da área de preparo?",
    "G034":  "Cozinha – ambientes internos/externos livres de objetos em desuso e sem animais?",
    "G035":  "Cozinha – há iluminação suficiente e luminárias protegidas contra explosão/queda nas áreas de preparo?",
    "G036":  "Cozinha – sanitários/vestiários sem comunicação direta com a área de preparo/armazenamento?",
    "G0371": "Resíduos – existem recipientes identificados, íntegros, laváveis e de fácil transporte?",
    "G0372": "Resíduos – nas áreas de preparo, os coletores têm tampas acionadas sem contato manual (pedal/joelho/sensor)?",
    "G0373": "Resíduos – a coleta é frequente e os resíduos ficam em local fechado e isolado da área de preparo?",
    "G04":   "Possui refeitório separado do ambiente da cozinha, com mesas adequadas ao tamanho das crianças?",
}

BLOCK_MAP = {
    "B": "B – Gestão da Demanda e Fila de Espera",
    "C": "C – Infraestrutura e Segurança Física",
    "D": "D – Ambiente Pedagógico",
    "E": "E – Recursos Humanos e Atendimento",
    "F": "F – Comunicação com as Famílias",
    "G": "G – Alimentação Escolar",
}

# Excluded from compliance analysis (free-text fields)
FREE_TEXT_COLS = ["B03", "B05", "C062", "C145"]

# Generate duplicate rows (multiple-choice) – will be aggregated per unit
MULTI_CHOICE_COLS = ["C12_Tipo", "F04_Tipo"]

VALID_RESPONSES = {"Sim", "Não", "Parcialmente"}

# Questions where "Sim" = bad outcome and "Não" = conforming
INVERTED_QUESTIONS = {"C14"}
