import json
import ollama
from ollama import ResponseError
import pdfplumber
from fpdf import FPDF
from pathlib import Path

REPORT_SCHEMA = {
    "type": "object",
    "properties": {
        "requirements_met": {"type": "array", "items": {"type": "string"}},
        "requirements_partial": {"type": "array", "items": {"type": "string"}},
        "requirements_not_evidenced": {"type": "array", "items": {"type": "string"}},
        "general_impression": {"type": "string"},
        "positioning": {"type": "string"},
        "strengths": {"type": "array", "items": {"type": "string"}},
        "interview_questions": {"type": "array", "minItems": 3, "items": {"type": "string"}},
    },
    "required": [
        "requirements_met",
        "requirements_partial",
        "requirements_not_evidenced",
        "general_impression",
        "positioning",
        "strengths",
        "interview_questions",
    ],
    "additionalProperties": False,
}

def main():
    try:
        pdf_file = file_select()
        text = extract_text(pdf_file)
        job_file = job_file_select()
        job_description = extract_text(job_file)
        write_response(report=run_prompt(text, job_description=job_description))
    except RuntimeError as error:
        print(f"\nError: {error}")

def file_select():
    resumes_folder = Path(__file__).parent / "resumes"
    pdf_files = sorted(resumes_folder.glob("*.pdf"))
    if not pdf_files:
        raise FileNotFoundError("No resume PDF files found in the 'resumes' folder.")

    print("PDF files found:\n")
    for idx, pdf in enumerate(pdf_files, start=1):
        print(f"[{idx}] {pdf.name}")
    while True:
        try:
            escolha = int(input("\nEnter the number of the desired file: "))
            if 1 <= escolha <= len(pdf_files):
                selected_file = pdf_files[escolha - 1]
                print(f"\nSelected file: {selected_file.name} \n")
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

    print("Job PDF files found: \n")
    for idx, job_file in enumerate(job_files, start=1):
        print(f"[{idx}] {job_file.name}")

    while True:
        try:
            escolha = int(input("\nEnter the number of the desired job: "))
            if 1 <= escolha <= len(job_files):
                selected_file = job_files[escolha - 1]
                print(f"\nSelected job: {selected_file.name} \n")
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
) -> dict:
    try:
        print("AI analysis started.")
        response = ollama.chat(
            model=model,
            format=REPORT_SCHEMA,
            messages=[
                {"role": "system", "content": "Você é um recrutador sênior com vasta experiência em seleção de talentos, análise estratégica de perfis e dinâmicas de recrutamento do mercado de trabalho. Sua função é comparar o currículo com a vaga fornecida e entregar uma avaliação crítica, objetiva e acionável da compatibilidade entre ambos. Instruções obrigatórias de comportamento e tom: 1. NÃO reescreva o currículo nem recrie seções inteiras dele. 2. Compare explicitamente os requisitos e responsabilidades da vaga com as experiências, competências e resultados apresentados no currículo. Diferencie requisitos atendidos, parcialmente atendidos e não evidenciados, sem inventar informações."},
                {"role": "user", "content": f"Descrição da vaga específica:\n{job_description}\n\nCurrículo:\n{pdf_text}\n\nRetorne somente um objeto JSON válido que siga exatamente o schema fornecido. Não inclua Markdown, títulos, numeração, comentários ou texto fora do JSON. Escreva as análises em português. Não calcule nem estime uma porcentagem de compatibilidade: essa decisão será preenchida manualmente pelo profissional de RH no PDF. Use listas de strings para os requisitos, pontos fortes e perguntas para a entrevista. As perguntas são conteúdo para o entrevistador usar durante a entrevista, não perguntas de esclarecimento para a pessoa que enviou o currículo. Gere exatamente pelo menos três perguntas relevantes, baseadas nos requisitos, lacunas ou experiências identificadas. Baseie tudo exclusivamente nas informações do currículo e da vaga."}
            ]
        )
    except ResponseError as error:
        if error.status_code == 404:
            raise RuntimeError(
                f"The model '{model}' was not found. "
                f"Run: ollama pull {model}"
            ) from error

        raise RuntimeError(
            f"Ollama returned an error: {error}"
        ) from error

    except ConnectionError as error:
        raise RuntimeError(
            "Could not connect to Ollama. "
            "Make sure the application is running."
        ) from error

    except Exception as error:
        raise RuntimeError(
            "Could not complete the analysis with Ollama. "
            f"Details: {error}"
        ) from error

    print("AI analysis completed. \n")
    try:
        report = json.loads(response["message"]["content"])
    except (KeyError, TypeError, json.JSONDecodeError) as error:
        raise RuntimeError("Ollama returned an invalid JSON report.") from error

    return validate_report(report)

def validate_report(report: dict) -> dict:
    required_fields = set(REPORT_SCHEMA["required"])
    if not isinstance(report, dict) or set(report) != required_fields:
        raise RuntimeError("The report does not match the expected structure.")

    list_fields = (
        "requirements_met",
        "requirements_partial",
        "requirements_not_evidenced",
        "strengths",
        "interview_questions",
    )
    for field in list_fields:
        values = report[field]
        if not isinstance(values, list) or not all(isinstance(value, str) for value in values):
            raise RuntimeError(f"The report field '{field}' must be a list of strings.")
        if field == "interview_questions" and len(values) < 3:
            raise RuntimeError("The report must contain at least three interview questions.")

    text_fields = ("general_impression", "positioning")
    if not all(isinstance(report[field], str) for field in text_fields):
        raise RuntimeError("The report text fields must be strings.")

    return report

def write_response(report: dict):
    output_folder = Path(__file__).parent / "output"
    output_folder.mkdir(exist_ok=True)

    output_file = output_folder / "output.pdf"
    file_number = 1
    while output_file.exists():
        output_file = output_folder / f"output_{file_number}.pdf"
        file_number += 1

    font_folder = Path("C:/Windows/Fonts")
    regular_font = font_folder / "arial.ttf"
    bold_font = font_folder / "arialbd.ttf"
    if not regular_font.exists() or not bold_font.exists():
        raise RuntimeError("Arial Unicode font files were not found in C:/Windows/Fonts.")

    pdf = FPDF()
    pdf.set_margins(left=20, top=20, right=20)
    pdf.set_auto_page_break(auto=True, margin=20)
    pdf.add_page()
    pdf.add_font("Arial", style="", fname=str(regular_font))
    pdf.add_font("Arial", style="B", fname=str(bold_font))

    pdf.set_font("Arial", style="B", size=14)
    pdf.set_x(pdf.l_margin)
    pdf.cell(w=0, h=10, text="Avaliação de Compatibilidade", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(4)

    render_section_title(pdf, "1. Compatibilidade com a Vaga")
    pdf.set_font("Arial", size=10)
    pdf.set_x(pdf.l_margin)
    pdf.multi_cell(w=0, h=6, text="Compatibilidade: _%")
    render_list(pdf, "Requisitos atendidos", report["requirements_met"])
    render_list(pdf, "Requisitos parcialmente atendidos", report["requirements_partial"])
    render_list(pdf, "Requisitos não evidenciados", report["requirements_not_evidenced"])

    render_section_title(pdf, "2. Impressão Geral e Posicionamento")
    render_paragraph(pdf, report["general_impression"])
    render_paragraph(pdf, report["positioning"])

    render_section_title(pdf, "3. Pontos Fortes para esta Vaga")
    render_list(pdf, "Pontos fortes", report["strengths"])

    render_section_title(pdf, "4. Perguntas para a Entrevista")
    render_numbered_list(pdf, report["interview_questions"])

    pdf.output(str(output_file))
    print(f"Output PDF generated successfully: {output_file}")

def render_section_title(pdf: FPDF, title: str):
    pdf.ln(5)
    pdf.set_font("Arial", style="B", size=11)
    pdf.set_x(pdf.l_margin)
    pdf.multi_cell(w=0, h=7, text=title)

def render_paragraph(pdf: FPDF, text: str):
    pdf.set_font("Arial", size=10)
    pdf.set_x(pdf.l_margin)
    pdf.multi_cell(w=0, h=6, text=text)
    pdf.ln(2)

def render_list(pdf: FPDF, title: str, items: list[str]):
    pdf.set_font("Arial", style="B", size=10)
    pdf.set_x(pdf.l_margin)
    pdf.multi_cell(w=0, h=6, text=title)
    pdf.set_font("Arial", size=10)
    for item in items:
        pdf.set_x(pdf.l_margin)
        pdf.multi_cell(w=0, h=6, text=f"- {item}")
    pdf.ln(2)

def render_numbered_list(pdf: FPDF, items: list[str]):
    pdf.set_font("Arial", size=10)
    for index, item in enumerate(items, start=1):
        pdf.set_x(pdf.l_margin)
        pdf.multi_cell(w=0, h=6, text=f"{index}. {item}")
    pdf.ln(2)

if __name__ == "__main__":
    main()