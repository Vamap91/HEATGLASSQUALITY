import streamlit as st
# Configurações da página - DEVE ser a primeira chamada Streamlit
st.set_page_config(page_title="MonitorAI (Quality) - dev", page_icon="🔴", layout="centered")

from openai import OpenAI
import tempfile
import json
import base64
from datetime import datetime
from fpdf import FPDF

# Inicializa o novo cliente da OpenAI
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# Dados estruturados dos formulários
FORMULARIOS = {
    "NPS": [
        {
            "categoria": "🟣 BORA ENCANTAR",
            "criterio": "Aplicou a técnica de Abordar Ativamente para fazer o cliente se sentir especial e único.",
            "percentual": 0.02
        },
        {
            "categoria": "🟣 BORA ENCANTAR",
            "criterio": "Demonstrou compreensão, aplicando frases empáticas para se conectar emocionalmente com o cliente.",
            "percentual": 0.02
        },
        {
            "categoria": "🟣 BORA ENCANTAR",
            "criterio": "Se apresentou e citou o nome da empresa durante a saudação.",
            "percentual": 0.02
        },
        {
            "categoria": "🟣 BORA ENCANTAR",
            "criterio": "Chamou o cliente pelo nome durante a pesquisa NPS.",
            "percentual": 0.02
        },
        {
            "categoria": "🟣 BORA ENCANTAR",
            "criterio": "Aplicou um fato positivo para demonstrar mais humanização e menos frieza no atendimento.",
            "percentual": 0.02
        },
        {
            "categoria": "🟣 BORA ENCANTAR",
            "criterio": "Evitou usar 'não' ou 'infelizmente' no início das frases para manter o tom positivo.",
            "percentual": 0.02
        },
        {
            "categoria": "🟣 BORA ENCANTAR",
            "criterio": "Aplicou a técnica da inversão de força (agradecimento, agradecimento e reverter).",
            "percentual": 0.02
        },
        {
            "categoria": "🟣 BORA ENCANTAR",
            "criterio": "Aplicou entonação enérgica com a técnica do sorriso na voz.",
            "percentual": 0.02
        },
        {
            "categoria": "🟣 BORA ENCANTAR",
            "criterio": "Aplicou entonação segura, com ênfase nas palavras de confiança.",
            "percentual": 0.02
        },
        {
            "categoria": "🟣 BORA ENCANTAR",
            "criterio": "Aplicou entonação empática, demonstrando compreensão e acolhimento.",
            "percentual": 0.02
        },
        {
            "categoria": "🟣 BORA ENCANTAR",
            "criterio": "Realizou um breve resumo do contato e confirmou se o cliente tinha dúvidas.",
            "percentual": 0.02
        },
        {
            "categoria": "🟣 BORA ENCANTAR",
            "criterio": "Em caso de elogio, utilizou a frase: 'Imagina, esse é o Jeito Cargalss de Encantar.'",
            "percentual": 0.02
        },
        {
            "categoria": "🟣 BORA ENCANTAR",
            "criterio": "Finalizou de forma surpreendente e agradeceu de maneira especial.",
            "percentual": 0.02
        },
        {
            "categoria": "💬 Análise do Atendimento / Manifestação",
            "criterio": "Houve identificação correta do serviço e local mencionado pelo cliente.",
            "percentual": 0.05
        },
        {
            "categoria": "⚙️ Procedimentos",
            "criterio": "Fez as perguntas da pesquisa NPS corretamente.",
            "percentual": 0.1
        },
        {
            "categoria": "⚙️ Procedimentos",
            "criterio": "Soube contornar conversas fora de contexto ou questionamentos não pertinentes à pesquisa.",
            "percentual": 0.05
        },
        {
            "categoria": "⚙️ Procedimentos",
            "criterio": "Utilizou conceitos do script Bora Encantar durante o atendimento (quando aplicável).",
            "percentual": 0.02
        },
        {
            "categoria": "⚙️ Procedimentos",
            "criterio": "Informou corretamente o prazo de retorno da Qualidade (quando for aberto uma reclamação).",
            "percentual": 0.02
        },
        {
            "categoria": "🔁 Tentativas de Contato",
            "criterio": "Realizou corretamente as tentativas de contato com o cliente (verbalmente perceptível).",
            "percentual": 0.1
        },
        {
            "categoria": "💼 Comportamento / Atitude",
            "criterio": "Conduziu o atendimento sem interromper ou abandonar o contato.",
            "percentual": 0.1
        },
        {
            "categoria": "💼 Comportamento / Atitude",
            "criterio": "Demonstrou cuidado com a imagem da empresa e parceiros.",
            "percentual": 0.1
        },
        {
            "categoria": "💼 Comportamento / Atitude",
            "criterio": "Após queda de contato, informou que retornaria o contato.",
            "percentual": 0.1
        },
        {
            "categoria": "💼 Comportamento / Atitude",
            "criterio": "Resolveu sem induzir o cliente a registrar reclamação em órgãos externos.",
            "percentual": 0.1
        }
    ],
    "Qualidade": [
        {
            "categoria": "🗣️ Abertura – “BORA ENCANTAR”",
            "criterio": "Se apresentou e citou o nome da empresa durante a saudação.",
            "percentual": 0.05
        },
        {
            "categoria": "🗣️ Abertura – “BORA ENCANTAR”",
            "criterio": "Aplicou a técnica de Abordar Ativamente para fazer o cliente se sentir especial e único.",
            "percentual": 0.05
        },
        {
            "categoria": "🗣️ Abertura – “BORA ENCANTAR”",
            "criterio": "Demonstrou compreensão, aplicando frases empáticas para se conectar emocionalmente com o cliente.",
            "percentual": 0.05
        },
        {
            "categoria": "🗣️ Abertura – “BORA ENCANTAR”",
            "criterio": "Chamou o cliente pelo nome durante o atendimento.",
            "percentual": 0.05
        },
        {
            "categoria": "🗣️ Abertura – “BORA ENCANTAR”",
            "criterio": "Aplicou um fato positivo para demonstrar humanização e empatia.",
            "percentual": 0.05
        },
        {
            "categoria": "🗣️ Abertura – “BORA ENCANTAR”",
            "criterio": "Evitou iniciar frases com 'não' ou 'infelizmente', mantendo o tom positivo.",
            "percentual": 0.05
        },
        {
            "categoria": "🗣️ Abertura – “BORA ENCANTAR”",
            "criterio": "Aplicou entonação enérgica e natural, com sorriso na voz.",
            "percentual": 0.1
        },
        {
            "categoria": "🗣️ Abertura – “BORA ENCANTAR”",
            "criterio": "Aplicou entonação segura e confiante.",
            "percentual": 0.05
        },
        {
            "categoria": "🗣️ Abertura – “BORA ENCANTAR”",
            "criterio": "Aplicou entonação empática, demonstrando acolhimento e compreensão.",
            "percentual": 0.05
        },
        {
            "categoria": "🗣️ Abertura – “BORA ENCANTAR”",
            "criterio": "Realizou um breve resumo do contato e confirmou se o cliente tinha dúvidas.",
            "percentual": 0.05
        },
        {
            "categoria": "🗣️ Abertura – “BORA ENCANTAR”",
            "criterio": "Em caso de elogio, utilizou a frase: 'Imagina, esse é o Jeito Cargalss de Encantar.'",
            "percentual": 0.02
        },
        {
            "categoria": "🗣️ Abertura – “BORA ENCANTAR”",
            "criterio": "Finalizou de forma positiva e agradeceu de maneira especial.",
            "percentual": 0.03
        },
        {
            "categoria": "🔁 Pós-contato / Retorno",
            "criterio": "Após queda de ligação, informa que retornará o contato.",
            "percentual": 0.05
        },
        {
            "categoria": "🔁 Pós-contato / Retorno",
            "criterio": "Demonstra intenção de manter o cliente assistido até a resolução.",
            "percentual": 0.05
        },
        {
            "categoria": "💼 Comportamento e Atitude Profissional",
            "criterio": "Conduz o atendimento de forma respeitosa e empática, evitando atritos.",
            "percentual": 0.1
        },
        {
            "categoria": "💼 Comportamento e Atitude Profissional",
            "criterio": "Mantém o foco no cliente, sem dispersões ou interrupções inadequadas.",
            "percentual": 0.1
        },
        {
            "categoria": "💼 Comportamento e Atitude Profissional",
            "criterio": "Zela pela imagem da empresa e fala com profissionalismo.",
            "percentual": 0.1
        }
    ],
    "SAC": [
        {
            "categoria": "🟣 BORA ENCANTAR",
            "criterio": "Saudação cordial e apresentação do atendente e da empresa.",
            "percentual": 0.01
        },
        {
            "categoria": "🟣 BORA ENCANTAR",
            "criterio": "Demonstra prontidão em falar com o cliente logo após atender.",
            "percentual": 0.01
        },
        {
            "categoria": "🟣 BORA ENCANTAR",
            "criterio": "Aplicou a técnica de priorização para fazer o cliente se sentir especial e único.",
            "percentual": 0.01
        },
        {
            "categoria": "🟣 BORA ENCANTAR",
            "criterio": "Demonstra empatia e prontidão para ajudar.",
            "percentual": 0.01
        },
        {
            "categoria": "🟣 BORA ENCANTAR",
            "criterio": "Usa linguagem clara, objetiva e profissional (sem vícios, diminutivos ou gerúndios).",
            "percentual": 0.01
        },
        {
            "categoria": "🟣 BORA ENCANTAR",
            "criterio": "Chama o cliente pelo nome ao longo do atendimento (mínimo 3x).",
            "percentual": 0.01
        },
        {
            "categoria": "🟣 BORA ENCANTAR",
            "criterio": "Demonstra paciência e empatia, especialmente em casos de reclamação.",
            "percentual": 0.01
        },
        {
            "categoria": "🟣 BORA ENCANTAR",
            "criterio": "Utiliza frases positivas e evita negativas diretas.",
            "percentual": 0.01
        },
        {
            "categoria": "🟣 BORA ENCANTAR",
            "criterio": "Aplica a técnica da inversão de força (agradecimento, reconhecimento e reversão).",
            "percentual": 0.01
        },
        {
            "categoria": "🟣 BORA ENCANTAR",
            "criterio": "Mantém tom de voz agradável e adequado.",
            "percentual": 0.02
        },
        {
            "categoria": "🟣 BORA ENCANTAR",
            "criterio": "Aplica entonação segura, com informação coerente e sem contradições.",
            "percentual": 0.01
        },
        {
            "categoria": "🟣 BORA ENCANTAR",
            "criterio": "Demonstra acolhimento e compreensão para contornar objeções ou situações negativas.",
            "percentual": 0.01
        },
        {
            "categoria": "🟣 BORA ENCANTAR",
            "criterio": "Segue scripts de fala em situações de espera ou transferência.",
            "percentual": 0.01
        },
        {
            "categoria": "🟣 BORA ENCANTAR",
            "criterio": "Realiza um breve resumo do contato e confirma se o cliente tem dúvidas.",
            "percentual": 0.01
        },
        {
            "categoria": "🟣 BORA ENCANTAR",
            "criterio": "Em caso de elogio, utiliza a frase: 'Imagina, esse é o Jeito Cargalss de Encantar.'",
            "percentual": 0.01
        },
        {
            "categoria": "🟣 BORA ENCANTAR",
            "criterio": "Finaliza o atendimento de forma positiva, agradecendo de maneira especial.",
            "percentual": 0.01
        },
        {
            "categoria": "💬 Análise do Atendimento / Manifestação",
            "criterio": "Confirma o entendimento do cliente antes de prosseguir.",
            "percentual": 0.02
        },
        {
            "categoria": "💬 Análise do Atendimento / Manifestação",
            "criterio": "Faz perguntas objetivas e direcionadas para identificar o problema.",
            "percentual": 0.02
        },
        {
            "categoria": "💬 Análise do Atendimento / Manifestação",
            "criterio": "Demonstra escuta ativa ao compreender a solicitação do cliente.",
            "percentual": 0.02
        },
        {
            "categoria": "💬 Análise do Atendimento / Manifestação",
            "criterio": "Demonstra domínio dos processos ao se comunicar (explicações claras e seguras).",
            "percentual": 0.02
        },
        {
            "categoria": "⚙️ Procedimentos",
            "criterio": "Confirma número de telefone para contato em caso de queda de ligação.",
            "percentual": 0.05
        },
        {
            "categoria": "⚙️ Procedimentos",
            "criterio": "Identifica corretamente o cliente (nome, número de pedido).",
            "percentual": 0.05
        },
        {
            "categoria": "⚙️ Procedimentos",
            "criterio": "Apresenta soluções claras e viáveis durante o atendimento.",
            "percentual": 0.05
        },
        {
            "categoria": "⚙️ Procedimentos",
            "criterio": "Incentiva o cliente a avaliar o atendimento (quando aplicável).",
            "percentual": 0.05
        },
        {
            "categoria": "⚙️ Procedimentos",
            "criterio": "Oferece reembolso quando aplicável e o faz de forma clara.",
            "percentual": 0.05
        },
        {
            "categoria": "⚙️ Procedimentos",
            "criterio": "Informa prazos, carências, limites, franquias ou valores corretamente.",
            "percentual": 0.02
        },
        {
            "categoria": "⚙️ Procedimentos",
            "criterio": "Verifica se o cliente tem alguma dúvida antes de encerrar.",
            "percentual": 0.05
        },
        {
            "categoria": "⚙️ Procedimentos",
            "criterio": "Tenta reverter reclamações ou insatisfações antes do encerramento.",
            "percentual": 0.05
        },
        {
            "categoria": "⚙️ Procedimentos",
            "criterio": "Esclarece dúvidas sobre links (vistoria, acompanhamento, reembolso).",
            "percentual": 0.05
        },
        {
            "categoria": "⚙️ Procedimentos",
            "criterio": "Ao transferir a ligação, explica brevemente o motivo e o contexto para o próximo atendente.",
            "percentual": 0.02
        },
        {
            "categoria": "⚙️ Procedimentos",
            "criterio": "Busca ser objetivo(a) sem prejudicar a qualidade do atendimento (equilíbrio de tempo e atenção).",
            "percentual": 0.02
        },
        {
            "categoria": "🔁 Retorno / FUP",
            "criterio": "Após queda de contato, informa que retornará o contato.",
            "percentual": 0.02
        },
        {
            "categoria": "🔁 Retorno / FUP",
            "criterio": "Demonstra disposição para manter o cliente assistido até a conclusão.",
            "percentual": 0.02
        },
        {
            "categoria": "💼 Comportamento / Atitude",
            "criterio": "Conduz o atendimento de forma respeitosa e empática.",
            "percentual": 0.05
        },
        {
            "categoria": "💼 Comportamento / Atitude",
            "criterio": "Evita induzir o cliente a registrar reclamações externas.",
            "percentual": 0.1
        },
        {
            "categoria": "💼 Comportamento / Atitude",
            "criterio": "Demonstra cuidado com a imagem da empresa, seguradoras e parceiros.",
            "percentual": 0.05
        },
        {
            "categoria": "💼 Comportamento / Atitude",
            "criterio": "Mantém o foco no cliente sem abandonar o atendimento.",
            "percentual": 0.05
        }
    ]
}

# Função para gerar prompt específico por tipo de avaliação
def gerar_prompt(tipo_avaliacao, transcript_text):
    criterios = FORMULARIOS[tipo_avaliacao]
    
    # Agrupar critérios por categoria com porcentagens
    grupos = {}
    for item in criterios:
        cat = item["categoria"]
        if cat not in grupos:
            grupos[cat] = []
        grupos[cat].append({"criterio": item["criterio"], "percentual": item["percentual"]})
    
    # Construir lista de critérios formatada com porcentagens
    criterios_texto = ""
    item_num = 1
    for categoria, lista_criterios in grupos.items():
        criterios_texto += f"\n### {categoria}\n"
        for crit_item in lista_criterios:
            percentual_str = f"{crit_item['percentual']*100:.0f}%"
            criterios_texto += f"{item_num}. {crit_item['criterio']} ({percentual_str})\n"
            item_num += 1
    
    prompt = f"""
Você é um especialista em avaliação de atendimento ao cliente. Avalie a transcrição a seguir de acordo com os critérios do formulário de {tipo_avaliacao}.

TRANSCRIÇÃO:
\"\"\"{transcript_text}\"\"\"

CRITÉRIOS DE AVALIAÇÃO:
{criterios_texto}

Retorne APENAS um JSON com a seguinte estrutura, sem texto adicional antes ou depois:

{{
  "tipo_avaliacao": "{tipo_avaliacao}",
  "grupos": [
    {{
      "nome_grupo": "Nome da Categoria",
      "criterios": [
        {{
          "item": 1,
          "criterio": "Texto do critério",
          "percentual": 0.05,
          "resposta": "sim" ou "não",
          "justificativa": "Justificativa detalhada baseada na transcrição"
        }}
      ]
    }}
  ],
  "resumo_geral": "Resumo geral da avaliação do atendimento",
  "observacoes": "Observações adicionais relevantes"
}}

INSTRUÇÕES IMPORTANTES:
- Avalie cada critério com rigor, baseando-se exclusivamente na transcrição fornecida
- Responda "sim" apenas se houver evidência clara na transcrição
- Responda "não" se não houver evidência ou se o critério não foi atendido
- Forneça justificativas específicas citando trechos da transcrição quando possível
- Mantenha a estrutura de grupos conforme as categorias listadas acima
- Seja objetivo e profissional nas avaliações

IMPORTANTE: Retorne APENAS o JSON, sem nenhum texto adicional, sem decoradores de código como ```json ou ```, e sem explicações adicionais.
"""
    return prompt


# Função auxiliar para normalizar texto para PDF (remover caracteres problemáticos)
def normalizar_texto_pdf(texto):
    if not texto:
        return ""
    # Substituir caracteres especiais e remover emojis
    texto = str(texto)
    # Remover caracteres não-ASCII problemáticos
    texto_limpo = ""
    for char in texto:
        if ord(char) < 256:
            texto_limpo += char
        else:
            texto_limpo += " "
    return texto_limpo


# Função auxiliar para normalizar texto para PDF (remover caracteres problemáticos)
def create_pdf(analysis, transcript_text, tipo_avaliacao):
    pdf = FPDF()
    pdf.add_page()
    
    # Configurações de fonte
    pdf.set_font("Arial", "B", 16)
    
    # Cabeçalho
    pdf.set_fill_color(193, 0, 0)
    pdf.set_text_color(255, 255, 255)
    pdf.cell(0, 10, f"MonitorAI - Relatorio {tipo_avaliacao}", 1, 1, "C", True)
    pdf.ln(5)
    
    # Informações gerais
    pdf.set_text_color(0, 0, 0)
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 10, f"Data da analise: {datetime.now().strftime('%d/%m/%Y %H:%M')}", 0, 1)
    pdf.cell(0, 10, f"Tipo de Avaliacao: {tipo_avaliacao}", 0, 1)
    
    # Calcular pontuação total
    grupos = analysis.get("grupos", [])
    pontuacao_total = 0
    pontuacao_obtida = 0
    for grupo in grupos:
        for criterio in grupo.get("criterios", []):
            percentual = criterio.get("percentual", 0)
            pontuacao_total += percentual
            if criterio.get("resposta", "").lower() == "sim":
                pontuacao_obtida += percentual
    
    percentual_final = (pontuacao_obtida / pontuacao_total * 100) if pontuacao_total > 0 else 0
    pdf.cell(0, 10, f"Pontuacao Total: {percentual_final:.1f}% ({pontuacao_obtida*100:.0f}/{pontuacao_total*100:.0f} pontos)", 0, 1)
    pdf.ln(5)
    
    # Resumo Geral
    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 10, "Resumo Geral", 0, 1)
    pdf.set_font("Arial", "", 12)
    pdf.multi_cell(0, 10, normalizar_texto_pdf(analysis.get("resumo_geral", "N/A")))
    pdf.ln(5)
    
    # Observações
    if analysis.get("observacoes"):
        pdf.set_font("Arial", "B", 14)
        pdf.cell(0, 10, "Observacoes", 0, 1)
        pdf.set_font("Arial", "", 12)
        pdf.multi_cell(0, 10, normalizar_texto_pdf(analysis.get("observacoes", "N/A")))
        pdf.ln(5)
    
    # Avaliação por grupos
    pdf.add_page()
    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 10, "Avaliacao Detalhada por Categoria", 0, 1)
    pdf.ln(5)
    
    grupos = analysis.get("grupos", [])
    for grupo in grupos:
        # Nome do grupo
        pdf.set_font("Arial", "B", 13)
        pdf.multi_cell(0, 10, normalizar_texto_pdf(grupo.get("nome_grupo", "")))
        pdf.ln(2)
        
        # Calcular pontuação do grupo
        criterios = grupo.get("criterios", [])
        pontos_grupo = sum(c.get("percentual", 0) for c in criterios if c.get("resposta", "").lower() == "sim")
        total_grupo = sum(c.get("percentual", 0) for c in criterios)
        percentual_grupo = (pontos_grupo / total_grupo * 100) if total_grupo > 0 else 0
        
        pdf.set_font("Arial", "I", 11)
        pdf.cell(0, 8, f"Pontuacao do grupo: {percentual_grupo:.1f}%", 0, 1)
        pdf.ln(2)
        
        # Critérios do grupo
        for criterio in criterios:
            item_num = criterio.get('item', '')
            criterio_texto = criterio.get('criterio', '')
            percentual = criterio.get('percentual', 0) * 100
            resposta = str(criterio.get('resposta', '')).upper()
            justificativa = criterio.get('justificativa', '')
            
            pdf.set_font("Arial", "B", 11)
            pdf.multi_cell(0, 8, normalizar_texto_pdf(f"{item_num}. {criterio_texto} ({percentual:.0f}%)"))
            pdf.set_font("Arial", "", 11)
            pdf.cell(0, 8, f"Resposta: {resposta}", 0, 1)
            pdf.multi_cell(0, 8, normalizar_texto_pdf(f"Justificativa: {justificativa}"))
            pdf.ln(3)
        
        pdf.ln(5)
    
    # Transcrição na última página
    pdf.add_page()
    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 10, "Transcricao da Ligacao", 0, 1)
    pdf.set_font("Arial", "", 10)
    pdf.multi_cell(0, 10, normalizar_texto_pdf(transcript_text))
    
    # Gerar PDF como bytes usando modo compatível com UTF-8
    pdf_output = pdf.output(dest="S")
    # Retornar como bytes, tratando encoding
    if isinstance(pdf_output, str):
        return pdf_output.encode("latin1", errors="ignore")
    return pdf_output

# Função para criar link de download do PDF
def get_pdf_download_link(pdf_bytes, filename):
    b64 = base64.b64encode(pdf_bytes).decode()
    href = f'<a href="data:application/pdf;base64,{b64}" download="{filename}">Baixar Relatório em PDF</a>'
    return href

# Estilo visual
st.markdown("""
<style>
h1, h2, h3 {
    color: #C10000 !important;
}
.result-box {
    background-color: #ffecec;
    padding: 1em;
    border-left: 5px solid #C10000;
    border-radius: 6px;
    font-size: 1rem;
    white-space: pre-wrap;
    line-height: 1.5;
}
.stButton>button {
    background-color: #C10000;
    color: white;
    font-weight: 500;
    border-radius: 6px;
    padding: 0.4em 1em;
    border: none;
}
.grupo-box {
    padding: 15px;
    border-radius: 8px;
    margin-bottom: 20px;
    background-color: #f8f9fa;
    border-left: 5px solid #C10000;
}
.criterio-sim {
    background-color: #e6ffe6;
    padding: 10px;
    border-radius: 6px;
    margin-bottom: 10px;
    border-left: 5px solid #00C100;
}
.criterio-nao {
    background-color: #ffcccc;
    padding: 10px;
    border-radius: 6px;
    margin-bottom: 10px;
    border-left: 5px solid #FF0000;
}
</style>
""", unsafe_allow_html=True)

# Modelo fixo: GPT-4 Turbo
modelo_gpt = "gpt-4-turbo"

# Título
st.title("MonitorAI (Quality) - dev")
st.write("Análise inteligente de ligações: avaliação de atendimento ao cliente com múltiplos formulários.")

# Seletor de tipo de avaliação
tipo_avaliacao = st.selectbox(
    "Selecione o tipo de avaliação:",
    ["NPS", "Qualidade", "SAC"],
    help="Escolha o formulário de avaliação apropriado para o tipo de atendimento"
)

st.info(f"**Formulário selecionado:** {tipo_avaliacao} ({len(FORMULARIOS[tipo_avaliacao])} critérios)")

# Upload de áudio
uploaded_file = st.file_uploader("Envie o áudio da ligação (.mp3)", type=["mp3"])

if uploaded_file is not None:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp:
        tmp.write(uploaded_file.read())
        tmp_path = tmp.name

    st.audio(uploaded_file, format='audio/mp3')

    if st.button("🔍 Analisar Atendimento"):
        # Transcrição via Whisper
        with st.spinner("Transcrevendo o áudio..."):
            try:
                with open(tmp_path, "rb") as audio_file:
                    transcript = client.audio.transcriptions.create(
                        model="whisper-1",
                        file=audio_file
                    )
                transcript_text = transcript.text
            except Exception as e:
                st.error(f"❌ Erro ao transcrever áudio: {str(e)}")
                st.warning("💡 Possíveis causas: arquivo muito grande, formato inválido, ou problema com a API da OpenAI.")
                st.info("🔧 Sugestões: Verifique se o arquivo é um MP3 válido e menor que 25MB.")
                st.stop()

        with st.expander("Ver transcrição completa"):
            st.code(transcript_text, language="markdown")

        # Gerar prompt específico
        prompt = gerar_prompt(tipo_avaliacao, transcript_text)

        with st.spinner(f"Analisando com formulário {tipo_avaliacao}..."):
            try:
                response = client.chat.completions.create(
                    model=modelo_gpt,
                    messages=[
                        {"role": "system", "content": "Você é um analista especializado em atendimento. Responda APENAS com o JSON solicitado, sem texto adicional, sem marcadores de código como ```json, e sem explicações."},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.3,
                    response_format={"type": "json_object"}
                )
                result = response.choices[0].message.content.strip()

                # Mostrar resultado bruto para depuração
                with st.expander("Debug - Resposta bruta"):
                    st.code(result, language="json")
                
                # Processar JSON
                try:
                    analysis = json.loads(result)
                except Exception as json_error:
                    st.error(f"Erro ao processar JSON: {str(json_error)}")
                    st.text_area("Resposta da IA:", value=result, height=300)
                    st.stop()

                # Exibir resumo geral
                st.subheader("📝 Resumo Geral")
                st.markdown(f"<div class='result-box'>{analysis.get('resumo_geral', 'N/A')}</div>", unsafe_allow_html=True)
                
                if analysis.get("observacoes"):
                    st.subheader("💡 Observações")
                    st.markdown(f"<div class='result-box'>{analysis.get('observacoes', '')}</div>", unsafe_allow_html=True)

                # Calcular pontuação total
                grupos = analysis.get("grupos", [])
                pontuacao_total = 0
                pontuacao_obtida = 0
                
                for grupo in grupos:
                    for criterio in grupo.get("criterios", []):
                        percentual = criterio.get("percentual", 0)
                        pontuacao_total += percentual
                        if criterio.get("resposta", "").lower() == "sim":
                            pontuacao_obtida += percentual
                
                # Exibir pontuação total
                percentual_final = (pontuacao_obtida / pontuacao_total * 100) if pontuacao_total > 0 else 0
                st.subheader(f"📊 Pontuação Total: {percentual_final:.1f}%")
                st.progress(pontuacao_obtida / pontuacao_total if pontuacao_total > 0 else 0)
                st.write(f"**{pontuacao_obtida*100:.0f}** pontos de **{pontuacao_total*100:.0f}** possíveis")
                
                # Exibir avaliação por grupos
                st.subheader(f"✅ Avaliação Detalhada - {tipo_avaliacao}")
                
                for grupo in grupos:
                    nome_grupo = grupo.get("nome_grupo", "")
                    criterios = grupo.get("criterios", [])
                    
                    # Calcular pontuação do grupo
                    pontos_grupo = sum(c.get("percentual", 0) for c in criterios if c.get("resposta", "").lower() == "sim")
                    total_grupo = sum(c.get("percentual", 0) for c in criterios)
                    percentual_grupo = (pontos_grupo / total_grupo * 100) if total_grupo > 0 else 0
                    
                    with st.expander(f"{nome_grupo} - {percentual_grupo:.1f}%"):
                        for criterio in criterios:
                            resposta = criterio.get("resposta", "").lower()
                            percentual = criterio.get("percentual", 0) * 100
                            
                            if resposta == "sim":
                                classe = "criterio-sim"
                                icone = "✅"
                            else:
                                classe = "criterio-nao"
                                icone = "❌"
                            
                            st.markdown(f"""
                            <div class="{classe}">
                            {icone} <strong>{criterio.get('item')}. {criterio.get('criterio')}</strong> ({percentual:.0f}%)<br>
                            <em>{criterio.get('justificativa')}</em>
                            </div>
                            """, unsafe_allow_html=True)
                
                # Gerar PDF
                st.subheader("📄 Relatório em PDF")
                try:
                    pdf_bytes = create_pdf(analysis, transcript_text, tipo_avaliacao)
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    filename = f"MonitorAI_{tipo_avaliacao}_{timestamp}.pdf"
                    st.markdown(get_pdf_download_link(pdf_bytes, filename), unsafe_allow_html=True)
                except Exception as pdf_error:
                    st.error(f"Erro ao gerar PDF: {str(pdf_error)}")

            except Exception as e:
                st.error(f"❌ Erro ao processar a análise: {str(e)}")
                st.warning("💡 Possíveis causas: limite de tokens excedido, problema com a API da OpenAI, ou erro de conexão.")
                st.info("🔧 Sugestões: Tente novamente em alguns segundos ou verifique se a API Key está configurada corretamente.")
                try:
                    st.text_area("Resposta da IA (para debug):", value=response.choices[0].message.content.strip(), height=300)
                except:
                    st.warning("⚠️ Não foi possível recuperar a resposta da IA para debug.")
