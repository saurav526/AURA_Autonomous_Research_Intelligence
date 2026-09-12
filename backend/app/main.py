from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from fastapi.responses import StreamingResponse
from .ieee_pdf import build_ieee_pdf
from io import BytesIO
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER
from reportlab.lib import colors
from .config import FRONTEND_ORIGIN
from .models import ResearchRequest, ResearchResult
from .graph import run_research
app=FastAPI(title='AURA Research Intelligence API',version='2.0.0')
app.add_middleware(CORSMiddleware,allow_origins=[FRONTEND_ORIGIN,'http://localhost:3000'],allow_credentials=True,allow_methods=['*'],allow_headers=['*'])
@app.get('/api/health')
def health(): return {'status':'ok'}

@app.post('/api/research',response_model=ResearchResult)
async def research(req: ResearchRequest):
    try: return await run_research(req.query,req.max_sources)
    except Exception as exc: raise HTTPException(status_code=500,detail=str(exc))

@app.post('/api/report/pdf')
async def report_pdf(payload: dict):
    query=str(payload.get('query','AURA Research Report'))
    answer=str(payload.get('final_answer',''))
    confidence=float(payload.get('confidence',0))*100
    sources=payload.get('sources',[])
    buf=BytesIO()
    doc=SimpleDocTemplate(buf,pagesize=A4,rightMargin=45,leftMargin=45,topMargin=45,bottomMargin=45)
    styles=getSampleStyleSheet()
    title=ParagraphStyle('title',parent=styles['Title'],alignment=TA_CENTER,fontSize=22,spaceAfter=16,textColor=colors.HexColor('#123D2D'))
    heading=ParagraphStyle('heading',parent=styles['Heading2'],fontSize=14,spaceBefore=14,spaceAfter=8,textColor=colors.HexColor('#123D2D'))
    body=ParagraphStyle('body',parent=styles['BodyText'],fontSize=10,leading=15,spaceAfter=8)
    story=[Paragraph('AURA — Autonomous Research Intelligence',title),Paragraph('Research Query',heading),Paragraph(query.replace('&','&amp;'),body),Paragraph('Verification Confidence',heading),Paragraph(f'{round(confidence)}%',body),Paragraph('Final Intelligence Report',heading)]
    for line in answer.splitlines():
        line=line.strip()
        if not line: story.append(Spacer(1,6)); continue
        safe=line.replace('&','&amp;').replace('<','&lt;').replace('>','&gt;')
        if safe.startswith('#'): story.append(Paragraph(safe.lstrip('#').strip(),heading))
        else: story.append(Paragraph(safe,body))
    story += [PageBreak(),Paragraph('Sources',heading)]
    for i,s in enumerate(sources,1):
        t=str(s.get('title','Source')).replace('&','&amp;'); u=str(s.get('url','')).replace('&','&amp;')
        story.append(Paragraph(f'[{i}] {t}<br/>{u}',body))
    doc.build(story); buf.seek(0)
    return StreamingResponse(buf,media_type='application/pdf',headers={'Content-Disposition':'attachment; filename="AURA_Research_Report.pdf"'})


@app.post("/api/report/ieee-pdf")
async def generate_ieee_pdf(payload: dict):

    query = payload.get(
        "query",
        "Autonomous Research Intelligence"
    )

    final_answer = payload.get(
        "final_answer",
        ""
    )

    confidence = payload.get(
        "confidence",
        0
    )

    sources = payload.get(
        "sources",
        []
    )

    pdf = build_ieee_pdf(
        query=query,
        final_answer=final_answer,
        confidence=confidence,
        sources=sources,
        author="AURA Research Intelligence",
        affiliation="Artificial Intelligence and Analytics"
    )

    return StreamingResponse(
        pdf,
        media_type="application/pdf",
        headers={
            "Content-Disposition":
            'attachment; filename="AURA_IEEE_Research_Paper.pdf"'
        }
    )
