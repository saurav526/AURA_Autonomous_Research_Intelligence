from io import BytesIO
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import (
    BaseDocTemplate,
    PageTemplate,
    Frame,
    Paragraph,
    Spacer,
    PageBreak,
    KeepTogether
)

PAGE_WIDTH, PAGE_HEIGHT = A4

LEFT = 0.55 * inch
RIGHT = 0.55 * inch
TOP = 0.55 * inch
BOTTOM = 0.55 * inch

GAP = 0.20 * inch

COLUMN_WIDTH = (
    PAGE_WIDTH - LEFT - RIGHT - GAP
) / 2


def clean_text(text):
    if not text:
        return ""

    text = str(text)

    replacements = {
        "**": "",
        "__": "",
        "###": "",
        "##": "",
        "#": "",
        "---": "",
        "`": "",
    }

    for old, new in replacements.items():
        text = text.replace(old, new)

    return text.strip()


def escape_html(text):
    return (
        str(text)
        .replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
    )


def extract_sections(text):
    sections = {}

    current = "Introduction"
    sections[current] = []

    for raw_line in str(text).splitlines():

        line = raw_line.strip()

        if not line:
            continue

        clean = clean_text(line)

        lower = clean.lower()

        if "executive summary" in lower:
            current = "Introduction"
            sections.setdefault(current, [])
            continue

        if "key findings" in lower:
            current = "Results and Discussion"
            sections.setdefault(current, [])
            continue

        if "methodology" in lower:
            current = "Methodology"
            sections.setdefault(current, [])
            continue

        if "system architecture" in lower:
            current = "System Architecture"
            sections.setdefault(current, [])
            continue

        if "analysis" in lower:
            current = "Analysis"
            sections.setdefault(current, [])
            continue

        if "results" in lower:
            current = "Results and Discussion"
            sections.setdefault(current, [])
            continue

        if "risks" in lower or "uncertainty" in lower:
            current = "Risks and Uncertainty"
            sections.setdefault(current, [])
            continue

        if "limitations" in lower:
            current = "Limitations"
            sections.setdefault(current, [])
            continue

        if "conclusion" in lower:
            current = "Conclusion"
            sections.setdefault(current, [])
            continue

        if "recommendation" in lower:
            current = "Recommendations"
            sections.setdefault(current, [])
            continue

        if line.startswith("|"):
            sections[current].append(clean)
        else:
            sections[current].append(clean)

    return sections


def build_ieee_pdf(
    query,
    final_answer,
    confidence=0,
    sources=None,
    author="AURA Research Intelligence",
    affiliation="Artificial Intelligence and Analytics"
):

    sources = sources or []

    buffer = BytesIO()

    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        "IEEE_TITLE",
        parent=styles["Title"],
        fontName="Helvetica-Bold",
        fontSize=15,
        leading=18,
        alignment=TA_CENTER,
        spaceAfter=10,
    )

    author_style = ParagraphStyle(
        "IEEE_AUTHOR",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=9,
        leading=12,
        alignment=TA_CENTER,
        spaceAfter=2,
    )

    abstract_heading = ParagraphStyle(
        "IEEE_ABSTRACT_HEADING",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=9,
        leading=11,
        alignment=TA_CENTER,
        spaceAfter=3,
    )

    abstract_style = ParagraphStyle(
        "IEEE_ABSTRACT",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=8.5,
        leading=11,
        alignment=0,
        spaceAfter=6,
    )

    keywords_style = ParagraphStyle(
        "IEEE_KEYWORDS",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=8,
        leading=10,
        spaceAfter=10,
    )

    heading_style = ParagraphStyle(
        "IEEE_HEADING",
        parent=styles["Heading2"],
        fontName="Helvetica-Bold",
        fontSize=9.5,
        leading=11,
        spaceBefore=7,
        spaceAfter=4,
    )

    body_style = ParagraphStyle(
        "IEEE_BODY",
        parent=styles["BodyText"],
        fontName="Helvetica",
        fontSize=8.2,
        leading=10.2,
        alignment=0,
        spaceAfter=4,
    )

    reference_style = ParagraphStyle(
        "IEEE_REFERENCE",
        parent=styles["BodyText"],
        fontName="Helvetica",
        fontSize=7.5,
        leading=9,
        leftIndent=0,
        firstLineIndent=0,
        spaceAfter=3,
    )

    first_frame = Frame(
        LEFT,
        BOTTOM,
        PAGE_WIDTH - LEFT - RIGHT,
        PAGE_HEIGHT - TOP - BOTTOM,
        id="first_frame",
        leftPadding=0,
        rightPadding=0,
        topPadding=0,
        bottomPadding=0,
    )

    left_frame = Frame(
        LEFT,
        BOTTOM,
        COLUMN_WIDTH,
        PAGE_HEIGHT - TOP - BOTTOM,
        id="left",
        leftPadding=0,
        rightPadding=0,
        topPadding=0,
        bottomPadding=0,
    )

    right_frame = Frame(
        LEFT + COLUMN_WIDTH + GAP,
        BOTTOM,
        COLUMN_WIDTH,
        PAGE_HEIGHT - TOP - BOTTOM,
        id="right",
        leftPadding=0,
        rightPadding=0,
        topPadding=0,
        bottomPadding=0,
    )

    def first_page(canvas, doc):
        canvas.saveState()

        canvas.setFont("Helvetica", 7)
        canvas.drawCentredString(
            PAGE_WIDTH / 2,
            0.30 * inch,
            f"AURA Autonomous Research Intelligence — Page {doc.page}"
        )

        canvas.restoreState()

    def later_pages(canvas, doc):
        canvas.saveState()

        canvas.setFont("Helvetica", 7)
        canvas.drawCentredString(
            PAGE_WIDTH / 2,
            0.30 * inch,
            f"AURA Autonomous Research Intelligence — Page {doc.page}"
        )

        canvas.restoreState()

    doc = BaseDocTemplate(
        buffer,
        pagesize=A4,
        leftMargin=LEFT,
        rightMargin=RIGHT,
        topMargin=TOP,
        bottomMargin=BOTTOM,
        title="AURA IEEE Research Paper",
        author=author,
    )

    doc.addPageTemplates([
        PageTemplate(
            id="FirstPage",
            frames=[first_frame],
            onPage=first_page,
        ),
        PageTemplate(
            id="TwoColumn",
            frames=[left_frame, right_frame],
            onPage=later_pages,
        ),
    ])

    story = []

    title = clean_text(query)

    if not title:
        title = "Autonomous Research Intelligence Report"

    story.append(
        Paragraph(
            escape_html(title.upper()),
            title_style
        )
    )

    story.append(
        Paragraph(
            escape_html(author),
            author_style
        )
    )

    story.append(
        Paragraph(
            escape_html(affiliation),
            author_style
        )
    )

    story.append(Spacer(1, 8))

    abstract_text = clean_text(final_answer)

    if len(abstract_text) > 1200:
        abstract_text = abstract_text[:1200] + "..."

    story.append(
        Paragraph(
            "Abstract—",
            abstract_heading
        )
    )

    story.append(
        Paragraph(
            escape_html(abstract_text),
            abstract_style
        )
    )

    story.append(
        Paragraph(
            "<b>Keywords—</b> Generative AI, Agentic AI, "
            "Large Language Models, Multi-Agent Systems, "
            "LangGraph, Groq, Autonomous Research",
            keywords_style
        )
    )

    story.append(PageBreak())

    sections = extract_sections(final_answer)

    section_order = [
        ("I.", "Introduction"),
        ("II.", "Methodology"),
        ("III.", "System Architecture"),
        ("IV.", "Analysis"),
        ("V.", "Results and Discussion"),
        ("VI.", "Risks and Uncertainty"),
        ("VII.", "Limitations"),
        ("VIII.", "Recommendations"),
        ("IX.", "Conclusion"),
    ]

    used = set()

    for number, section_name in section_order:

        content = sections.get(section_name, [])

        if not content:
            continue

        used.add(section_name)

        story.append(
            Paragraph(
                f"{number} {section_name.upper()}",
                heading_style
            )
        )

        for item in content:

            item = clean_text(item)

            if not item:
                continue

            if item.startswith("|"):
                item = item.replace("|", "  |  ")

            story.append(
                Paragraph(
                    escape_html(item),
                    body_style
                )
            )

    for name, content in sections.items():

        if name in used:
            continue

        if not content:
            continue

        story.append(
            Paragraph(
                name.upper(),
                heading_style
            )
        )

        for item in content:

            item = clean_text(item)

            if not item:
                continue

            story.append(
                Paragraph(
                    escape_html(item),
                    body_style
                )
            )

    story.append(
        Paragraph(
            "VERIFICATION CONFIDENCE",
            heading_style
        )
    )

    try:
        confidence_value = float(confidence)
        if confidence_value <= 1:
            confidence_value *= 100
    except Exception:
        confidence_value = 0

    story.append(
        Paragraph(
            f"The research pipeline assigned an overall "
            f"verification confidence of {confidence_value:.1f}%.",
            body_style
        )
    )

    story.append(
        Paragraph(
            "REFERENCES",
            heading_style
        )
    )

    if sources:

        for index, source in enumerate(sources, 1):

            if isinstance(source, dict):

                source_title = source.get(
                    "title",
                    f"Research Source {index}"
                )

                source_url = source.get(
                    "url",
                    ""
                )

                reference = (
                    f"[{index}] {source_title}. "
                    f"{source_url}"
                )

            else:

                reference = f"[{index}] {source}"

            story.append(
                Paragraph(
                    escape_html(reference),
                    reference_style
                )
            )

    else:

        story.append(
            Paragraph(
                "[1] Sources were not explicitly returned "
                "by the research pipeline.",
                reference_style
            )
        )

    doc.handle_nextPageTemplate("TwoColumn")

    doc.build(story)

    buffer.seek(0)

    return buffer