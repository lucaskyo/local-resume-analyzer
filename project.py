import ollama
import pdfplumber
from fpdf import FPDF
from pathlib import Path

def main():
    pdf_file = file_select()
    text = extract_text(pdf_file)
    job_file = job_file_select()
    job_description = extract_text(job_file)
    write_response(response = run_prompt(text, job_description=job_description))

def file_select():
    root_folder = Path(__file__).parent
    pdf_files = sorted(root_folder.glob("*.pdf"))
    if not pdf_files:
        raise FileNotFoundError("No resume PDF files found in the project folder.")

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

def job_file_select():
    jobs_folder = Path(__file__).parent / "positions"
    job_files = sorted(jobs_folder.glob("*.pdf"))
    if not job_files:
        raise FileNotFoundError("No PDF files for the position found in the 'positions' folder.")

    print("Job PDF files found:")
    for idx, job_file in enumerate(job_files, start=1):
        print(f"[{idx}] {job_file.name}")

    while True:
        try:
            escolha = int(input("Enter the number of the desired job: "))
            if 1 <= escolha <= len(job_files):
                selected_file = job_files[escolha - 1]
                print(f"Selected job: {selected_file.name}")
                return selected_file
            print("Invalid option. Please enter a number from the list.")
        except ValueError:
            print("Invalid input. Please enter numbers only.")

def extract_text(file):
    with pdfplumber.open(file) as pdf:
        pages_text = []
        for page in pdf.pages:
            page_text = page.extract_text(
                    x_tolerance=3,
                    y_tolerance=5,
                    layout=False
                )
            if page_text:
                pages_text.append(page_text)
    return "\n\n".join(pages_text)

def run_prompt(
    pdf_text: str,
    model: str = "qwen2.5:3b",
    job_description: str = ""
) -> str:
    print("AI analysis started.")
    response = ollama.chat(
        model=model,
        messages=[
            {"role": "system", "content": "Você é um recrutador sênior com vasta experiência em seleção de talentos, análise estratégica de perfis e dinâmicas de recrutamento do mercado de trabalho. Sua função é comparar o currículo com a vaga fornecida e entregar uma avaliação crítica, objetiva e acionável da compatibilidade entre ambos. Instruções obrigatórias de comportamento e tom: 1. Comunique-se diretamente com a pessoa que enviou o currículo. Use a segunda pessoa ('você', 'seu', 'sua'). É PROIBIDO usar a terceira pessoa (não use termos como 'o candidato', 'ele', 'o profissional' ou 'o currículo do usuário'). 2. NÃO faça nenhuma pergunta ao usuário. Sua resposta deve conter apenas análises, diagnósticos e recomendações diretas, sem interrogações ou solicitações de esclarecimentos adicionais. 3. NÃO reescreva o currículo nem recrie seções inteiras dele. 4. Compare explicitamente os requisitos e responsabilidades da vaga com as experiências, competências e resultados apresentados no currículo. Diferencie requisitos atendidos, parcialmente atendidos e não evidenciados, sem inventar informações. Estruture sua resposta estritamente no seguinte formato: 1. Compatibilidade com a Vaga: Apresente um percentual estimado de compatibilidade, os requisitos atendidos, parcialmente atendidos e não evidenciados, sempre com base no currículo. 2. Impressão Geral e Posicionamento: Avalie como seu perfil é percebido para esta vaga nos primeiros segundos de leitura. 3. Pontos Fortes para esta Vaga: Apresente as experiências, conquistas, competências e palavras-chave que jogam a seu favor. 4. Oportunidades de Melhoria: Aponte falhas, lacunas, termos genéricos, falta de métricas ou inconsistências que reduzam sua compatibilidade. 5. Recomendações Práticas de Ajuste: Forneça orientações diretas sobre o que você deve alterar, remover ou enfatizar para aumentar suas chances de ser chamado para esta vaga."},
            {"role": "user", "content": f"Descrição da vaga específica:\n{job_description}\n\nCurrículo:\n{pdf_text}\n"}
        ]
    )
    print("AI analysis completed.")
    return response["message"]["content"]

def write_response(text):
    pdf = FPDF()
    pdf.set_margins(left=20, top=20, right=20)
    pdf.set_auto_page_break(auto=True, margin=20)
    pdf.add_page()
    pdf.set_font("Helvetica", size=8)
    pdf.multi_cell(w=0, h=5, text=text.encode("latin-1", "replace").decode("latin-1"))
    pdf.output("output.pdf")
    print("Output PDF generated successfully.")

if __name__ == "__main__":
    main()