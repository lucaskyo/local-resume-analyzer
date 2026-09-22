import ollama
import pdfplumber
from fpdf import FPDF
from pathlib import Path

def main():
    pdf_file = file_select()
    text = extract_text(pdf_file)
    response = run_prompt(text)
    write_response(response)

def file_select():
    root_folder = Path(__file__).parent
    pdf_files = sorted(root_folder.glob("*.pdf"))
    if not pdf_files:
        print("No PDF files found in the folder.")
    else:
        print("PDF files found:")
        for idx, pdf in enumerate(pdf_files, start=1):
            print(f"[{idx}] {pdf.name}")
        while True:
            try:
                escolha = int(input("Enter the number of the desired file: "))
                if 1 <= escolha <= len(pdf_files):
                    selected_file = pdf_files[escolha - 1]
                    print(f"Selected file: {selected_file.name}")
                    break
                else:
                    print("Invalid option. Please enter a number from the list.")
            except ValueError:
                print("Invalid input. Please enter numbers only.")
    return selected_file

def extract_text(file):
    with pdfplumber.open(file) as pdf:
        page = pdf.pages[0]
        text = page.extract_text(
                x_tolerance=3, 
                y_tolerance=5, 
                layout=False
            )
    return text

def run_prompt(pdf_text: str, model: str = "qwen2.5:3b") -> str:
    print("AI analysis started.")
    response = ollama.chat(
        model=model,
        messages=[
            {"role": "system", "content": "Você é um recrutador sênior com vasta experiência em seleção de talentos, análise estratégica de perfis e dinâmicas de recrutamento do mercado de trabalho. Sua função é analisar o currículo fornecido e entregar uma avaliação crítica, objetiva e acionável. Instruções obrigatórias de comportamento e tom: 1. Comunique-se diretamente com a pessoa que enviou o currículo. Use a segunda pessoa ('você', 'seu', 'sua'). É PROIBIDO usar a terceira pessoa (não use termos como 'o candidato', 'ele', 'o profissional' ou 'o currículo do usuário'). 2. NÃO faça nenhuma pergunta ao usuário. Sua resposta deve conter apenas análises, diagnósticos e recomendações diretas, sem interrogações ou solicitações de esclarecimentos adicionais. 3. NÃO reescreva o currículo nem recrie seções inteiras dele. Sua tarefa é avaliar e criticar o conteúdo existente, e não redigir uma nova versão da experiência da pessoa. Estruture sua resposta estritamente no seguinte formato: 1. Impressão Geral e Posicionamento: Avalie como seu perfil é percebido nos primeiros segundos de leitura, destacando a clareza dos seus objetivos e o impacto visual da estrutura. 2. Pontos Fortes: Apresente os aspectos que jogam a seu favor (ex.: conquistas relevantes, coerência de trajetória, boas palavras-chave ou clareza em resultados). 3. Oportunidades de Melhoria: Aponta falhas, lacunas de informação, termos genéricos, falta de métricas/resultados ou inconsistências na organização das informações. 4. Recomendações Práticas de Ajuste: Forneça orientações diretas sobre o que você deve alterar, remover ou enfatizar para aumentar suas chances de ser chamado para entrevistas."},
            {"role": "user", "content": f"Currículo:\n{pdf_text}\n"}
        ]
    )
    print("AI analysis completed.")
    return response["message"]["content"]

def write_response(text):
    response_text = text
    pdf = FPDF()
    pdf.set_margins(left=20, top=20, right=20)
    pdf.set_auto_page_break(auto=True, margin=20)
    pdf.add_page()
    pdf.set_font("Helvetica", size=8)
    pdf.multi_cell(w=0, h=5, text=response_text)
    pdf.output("output.pdf")
    print("Output PDF generated successfully.")

if __name__ == "__main__":
    main()