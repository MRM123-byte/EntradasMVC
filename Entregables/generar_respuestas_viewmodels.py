from io import BytesIO
from pathlib import Path

from PIL import Image
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    Image as ReportLabImage,
    KeepTogether,
    PageBreak,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
)


BASE_DIR = Path(__file__).resolve().parent
OUTPUT = BASE_DIR / "Respuestas_Cuestionario_ViewModels.pdf"
REFERENCE_COVER = Path(r"C:\Users\pc\AppData\Local\Temp\mvc_reference_render\cover-1.png")
ARIAL = Path(r"C:\Windows\Fonts\arial.ttf")
ARIAL_BOLD = Path(r"C:\Windows\Fonts\arialbd.ttf")


def add_page_number(canvas, document):
    if document.page > 1:
        canvas.saveState()
        canvas.setFont("Arial", 9)
        canvas.drawCentredString(letter[0] / 2, 0.42 * inch, str(document.page))
        canvas.restoreState()


def logo_from_reference():
    """Extract the logo area from the provided reference cover in memory."""
    image = Image.open(REFERENCE_COVER)
    logo = image.crop((270, 70, 960, 770))
    buffer = BytesIO()
    logo.save(buffer, format="PNG")
    buffer.seek(0)
    return buffer


pdfmetrics.registerFont(TTFont("Arial", str(ARIAL)))
pdfmetrics.registerFont(TTFont("Arial-Bold", str(ARIAL_BOLD)))

styles = getSampleStyleSheet()
cover_institution = ParagraphStyle(
    "CoverInstitution",
    parent=styles["Normal"],
    fontName="Arial",
    fontSize=13,
    leading=18,
    alignment=TA_CENTER,
)
cover_institution_bold = ParagraphStyle(
    "CoverInstitutionBold",
    parent=cover_institution,
    fontName="Arial-Bold",
)
cover_activity = ParagraphStyle(
    "CoverActivity",
    parent=styles["Normal"],
    fontName="Arial-Bold",
    fontSize=17,
    leading=22,
    alignment=TA_CENTER,
)
cover_title = ParagraphStyle(
    "CoverTitle",
    parent=cover_activity,
    fontSize=16,
)
cover_details = ParagraphStyle(
    "CoverDetails",
    parent=styles["Normal"],
    fontName="Arial",
    fontSize=12,
    leading=18,
    alignment=TA_CENTER,
)
heading = ParagraphStyle(
    "Heading",
    parent=styles["Heading1"],
    fontName="Arial-Bold",
    fontSize=16,
    leading=20,
    alignment=TA_CENTER,
    spaceAfter=16,
)
question = ParagraphStyle(
    "Question",
    parent=styles["Normal"],
    fontName="Arial-Bold",
    fontSize=12,
    leading=16,
    alignment=TA_LEFT,
)
answer = ParagraphStyle(
    "Answer",
    parent=styles["Normal"],
    fontName="Arial",
    fontSize=12,
    leading=16,
    alignment=TA_JUSTIFY,
    spaceAfter=10,
)

answers = [
    (
        "¿Cuál es la diferencia principal entre Model y ViewModel?",
        "El Model representa los datos y reglas del negocio. El ViewModel prepara solamente los datos que una vista necesita recibir o mostrar.",
    ),
    (
        "¿Cómo sabe una vista qué tipo de ViewModel recibe?",
        "Lo sabe por la línea @model que está al inicio de la vista. Por ejemplo, Index usa CotizacionInputViewModel y Resultado usa ResultadoCotizacionViewModel.",
    ),
    (
        "¿Qué función cumple Model Binding?",
        "Model Binding toma los datos que el usuario envía desde el formulario y crea un objeto ViewModel con esos valores para el controlador.",
    ),
    (
        "¿Puede un ViewModel recibir datos desde el navegador? Explique.",
        "Sí. En este proyecto CotizacionInputViewModel recibe el nombre, la cantidad y el tipo de entrada enviados desde el formulario.",
    ),
    (
        "¿Qué son las Data Annotations?",
        "Son atributos como [Required], [Range] y [StringLength]. Sirven para validar los datos y definir nombres que se muestran en el formulario.",
    ),
    (
        "¿Por qué Evento puede pertenecer al ViewModel de resultado y no necesariamente a Cotizacion?",
        "Porque Evento es información que necesita la pantalla de resultado, pero no es parte del cálculo de una cotización.",
    ),
    (
        "¿Dónde debe permanecer la regla del descuento y por qué?",
        "Debe permanecer en Cotizacion, porque es una regla de negocio y no una regla de la vista.",
    ),
    (
        "¿Un ViewModel representa obligatoriamente una tabla de la base de datos?",
        "No. Un ViewModel se crea para las necesidades de una vista y no tiene que representar una tabla.",
    ),
    (
        "Explique el recorrido completo desde que se pulsa Calcular hasta que aparece el resultado.",
        "El formulario envía los datos a Calcular. Model Binding crea el CotizacionInputViewModel y el controlador valida los datos. Si son correctos, crea una Cotizacion para calcular los importes. Después crea ResultadoCotizacionViewModel con la cotización, el evento, la fecha y el mensaje. Finalmente envía ese ViewModel a la vista Resultado.",
    ),
    (
        "¿Qué ventaja tiene utilizar un ViewModel de entrada en un formulario?",
        "Permite decidir exactamente qué datos puede enviar el formulario y colocar las validaciones correspondientes sin mezclar esas validaciones con las reglas de negocio.",
    ),
]

document = SimpleDocTemplate(
    str(OUTPUT),
    pagesize=letter,
    rightMargin=0.78 * inch,
    leftMargin=0.78 * inch,
    topMargin=0.68 * inch,
    bottomMargin=0.70 * inch,
)

story = []
logo = logo_from_reference()
story.append(Spacer(1, 0.25 * inch))
story.append(ReportLabImage(logo, width=3.45 * inch, height=3.45 * inch, hAlign="CENTER"))
story.append(Spacer(1, 0.20 * inch))
story.append(Paragraph("UNIVERSIDAD PRIVADA DEL VALLE", cover_institution_bold))
story.append(Paragraph("FACULTAD DE INFORMÁTICA Y ELECTRÓNICA", cover_institution))
story.append(Paragraph("CARRERA DE INGENIERÍA DE SISTEMAS INFORMÁTICOS", cover_institution))
story.append(Spacer(1, 0.46 * inch))
story.append(Paragraph("ACTIVIDAD ASÍNCRONA", cover_activity))
story.append(Paragraph("ViewModels en ASP.NET Core MVC", cover_title))
story.append(Spacer(1, 0.35 * inch))
story.append(Paragraph("Asignatura: Programación Web III", cover_details))
story.append(Paragraph("Unidad de aprendizaje: Unidad 2", cover_details))
story.append(Paragraph("Estudiante: Mauricio Rivero Mendez", cover_details))
story.append(Paragraph("Fecha de entrega: 01/10/2026", cover_details))
story.append(PageBreak())
story.append(Paragraph("RESPUESTAS CUESTIONARIO", heading))

for number, (prompt, response) in enumerate(answers, start=1):
    block = [
        Paragraph(f"{number}. &nbsp; {prompt}", question),
        Paragraph(response, answer),
    ]
    story.append(KeepTogether(block))

document.build(story, onFirstPage=add_page_number, onLaterPages=add_page_number)
print(OUTPUT)
