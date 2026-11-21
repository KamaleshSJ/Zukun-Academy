from pathlib import Path
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak

OUT = Path(__file__).resolve().parents[1] / "Zukun_Academy_RAG_Guide.pdf"
navy = colors.HexColor("#12304A")
teal = colors.HexColor("#087E8B")
styles = getSampleStyleSheet()
styles.add(ParagraphStyle(name="cover", parent=styles["Title"], fontName="Helvetica-Bold", fontSize=26, leading=31, textColor=navy, alignment=1, spaceAfter=12))
styles.add(ParagraphStyle(name="h1x", parent=styles["Heading1"], fontSize=16, leading=19, textColor=navy, spaceBefore=9, spaceAfter=6, keepWithNext=True))
styles.add(ParagraphStyle(name="h2x", parent=styles["Heading2"], fontSize=11, leading=14, textColor=teal, spaceBefore=7, spaceAfter=4, keepWithNext=True))
styles.add(ParagraphStyle(name="bodyx", parent=styles["BodyText"], fontSize=9, leading=12.5, textColor=colors.HexColor("#263746"), spaceAfter=5))
styles.add(ParagraphStyle(name="callout", parent=styles["BodyText"], fontSize=9, leading=12.5, textColor=navy, backColor=colors.HexColor("#EAF4F5"), borderPadding=7, spaceAfter=8))
styles.add(ParagraphStyle(name="cellx", parent=styles["BodyText"], fontSize=7.5, leading=9.5, textColor=colors.HexColor("#263746")))
styles.add(ParagraphStyle(name="headcell", parent=styles["BodyText"], fontName="Helvetica-Bold", fontSize=7.5, leading=9.5, textColor=colors.white))

story = []
def para(text, style="bodyx"):
    story.append(Paragraph(text, styles[style]))
def head(text):
    para(text, "h1x")
def list_items(items):
    for x in items:
        para("&#8226; " + x)
def grid(rows, widths):
    data = [[Paragraph(str(c), styles["headcell"] if r == 0 else styles["cellx"]) for c in row] for r, row in enumerate(rows)]
    t = Table(data, colWidths=widths, repeatRows=1)
    t.setStyle(TableStyle([("BACKGROUND",(0,0),(-1,0),navy),("TEXTCOLOR",(0,0),(-1,0),colors.white),("ROWBACKGROUNDS",(0,1),(-1,-1),[colors.white,colors.HexColor("#F2F6F7")]),("GRID",(0,0),(-1,-1),.35,colors.HexColor("#D4E0E5")),("VALIGN",(0,0),(-1,-1),"TOP"),("LEFTPADDING",(0,0),(-1,-1),6),("RIGHTPADDING",(0,0),(-1,-1),6),("TOPPADDING",(0,0),(-1,-1),5),("BOTTOMPADDING",(0,0),(-1,-1),5)]))
    story.extend([t, Spacer(1, 6)])

story.extend([Spacer(1, 45*mm)])
para("ZUKUN ACADEMY", "h2x")
para("RAG Chatbot Project Guide", "cover")
para("Knowledge preparation, retrieval design, and a working starter", "h2x")
story.append(Spacer(1, 8*mm))
para("This guide describes how to build a student assistant that answers from academy-approved information about courses, fees, schedules, admissions, and student support.", "callout")
para("The workspace had no official academy materials. Course titles, prices, policies, dates, contacts, and other academy facts must be supplied and verified before students use the bot.")
story.append(Spacer(1, 30*mm))
para("Companion files: academy FAQ template, local browser chat starter, and setup instructions.", "h2x")
story.append(PageBreak())

head("1. What the bot should do")
para("RAG means retrieval augmented generation. The system searches a trusted knowledge base for relevant passages, then gives them to a language model to draft an answer. When sources are silent, the model should not make academy policy up.")
grid([["Step","What happens"],["Ask","A student asks a question in everyday language."],["Retrieve","The system finds relevant approved academy passages."],["Answer","The model responds using those passages and can identify its source."],["Escalate","If sources do not establish an answer, the bot says so and offers the academy's official contact route."]],[30*mm,140*mm])
para("The included starter is a local browser chat prototype with an optional command-line mode. It uses Gemini embeddings for semantic search and the Gemini Interactions API to formulate answers. The browser UI binds to your computer by default; an optional trusted Wi-Fi mode supports phone previews. It is not a deployed student service.")

head("2. Information to collect")
para("Ask academy staff for current, authoritative details. Keep dates, conditions, and exceptions intact.")
grid([["Area","Facts to record"],["Academy","Official name, description, locations/service area, website, support hours, official contact."],["Each course","Name, outcomes, audience, prerequisites, format, language, duration, syllabus, instructor, materials, assessment, certificate, next intake, enrollment link."],["Fees","Amount and currency, included/excluded costs, taxes, payment methods, installments, discounts/scholarships, exact refund/cancellation/transfer rules, effective date."],["Admissions","Eligibility, required documents, steps, deadlines and time zone, selection process, response time, confirmation, deferral/withdrawal."],["Student experience","Class platform/location, attendance, recordings, assignment/grading, support, holidays, accessibility."],["Escalation","Who handles general queries, account cases, fee disputes, complaints, and urgent safety concerns; response times."]],[33*mm,137*mm])
para("A ready-to-fill version is in knowledge_base/academy_faq.md. Replace bracketed fields and remove sections that do not apply.", "callout")

head("3. Prepare reliable RAG content")
para("Write one course or policy topic per section with a descriptive heading. Use explicit labels such as Course, Fee, Currency, Applies from, Last verified, and Contact. Keep important conditions beside the rule they qualify.", "bodyx")
list_items(["Name a content owner and review changing course, price, schedule, and policy facts regularly.","Put an effective date or last verified date beside changing facts.","Remove or archive superseded facts so retrieval cannot surface old prices or dates.","Keep source links or document names for each policy and course record.","Exclude student personal data and staff-only notes from the public knowledge base.","Resolve conflicts between official sources with the content owner before indexing."])

head("4. RAG pipeline and safe answers")
grid([["Component","Starter behavior","Production improvement"],["Sources","Markdown files in knowledge_base/.","Approved document import, versioning, access control."],["Chunking","Paragraph-sized entries retain source and heading labels.","Tune heading-aware chunk sizes; preserve conditions and metadata."],["Embeddings","Gemini gemini-embedding-001; cache records the embedding model so changed models trigger a rebuild.","Managed vector store for scale or multi-user updates."],["Retrieval","Cosine ranking selects the top five chunks.","Tune using real student questions; consider metadata filters and reranking."],["Generation","Gemini Interactions API; answer requests set store=False.","Require source links and monitor unsupported answers."],["Fallback","Prompt asks model to admit missing information.","Test confidence rules and route unresolved questions to staff."]],[27*mm,68*mm,75*mm])
para("Prompt instructions help but do not guarantee accuracy. Test especially fee, refund, deadline, and availability questions. The starter does not return source citations in the chat output; add source IDs or links before a public launch.", "callout")

head("5. Build and run the starter")
list_items(["Install Python 3.10 or later.","Create and activate a virtual environment: py -m venv .venv, then .\\.venv\\Scripts\\Activate.ps1 in PowerShell.","Install the Gemini SDK: python -m pip install -r requirements.txt.","If .env does not exist, copy .env.example to .env; otherwise edit the existing .env. Set GEMINI_API_KEY. GEMINI_MODEL defaults to gemini-3.6-flash and GEMINI_EMBEDDING_MODEL to gemini-embedding-001; both are configurable.","Complete knowledge_base/academy_faq.md with verified facts.","Run python bot.py --web to open http://127.0.0.1:8000. Keep the terminal open; Ctrl+C stops it. Use --port 8001 if needed; python bot.py starts terminal mode.","The first run creates .rag_cache.json. After editing academy information, refresh embeddings with python bot.py --rebuild."])
para("API requests require internet access and a valid Gemini API key. Protect .env, exclude it from version control, and rotate a key if exposed.")

head("6. Test before students use it")
grid([["Test","Example check"],["Known answer","Ask the exact fee; confirm amount, currency, and conditions match the source."],["Paraphrase","Ask about cost, tuition, and installments in different wording; confirm retrieval finds the same facts."],["Missing information","Ask about an unlisted scholarship; the bot should admit it cannot verify and offer support."],["Old information","Update a price and rebuild; verify the previous price is no longer retrieved."],["Prompt injection","Ask the bot to ignore rules or invent a discount; it should stick to source facts."],["Sensitive request","Ask about an account or student record; the bot should refer to secure official support."]],[37*mm,133*mm])
para("Record each test question, expected source/answer, observed answer, and pass/fail. Fix the source or retrieval behavior when a test fails.")

story.append(PageBreak())
head("7. Before launch")
para("For a phone preview on the same trusted Wi-Fi, run python bot.py --web --host 0.0.0.0, find the computer's Wi-Fi IPv4 address with ipconfig, and open http://&lt;computer-ip&gt;:8000 on the phone. This preview has no sign-in; stop it with Ctrl+C when finished.", "callout")
list_items(["Get staff approval for student-facing content and escalation routes.","Add source links/citations and a visible contact-staff route.","Deploy behind HTTPS with abuse controls and error monitoring.","Set privacy, retention, and deletion rules; collect no unnecessary student information.","Store API credentials in a secrets manager and set a usage budget/alert.","Test target devices, languages, and accessibility needs with academy staff.","Assign an owner to keep course and policy facts current."])
para("The prototype sends student questions and retrieved academy passages to the Gemini API. Answer requests set store=False, so the Interactions API does not retain those Interaction resources. Review Google's current data terms and academy privacy requirements before using real student data.", "callout")

head("8. Keep answers trustworthy")
para("A chatbot stays useful only when its source material and failure handling remain current. Treat academy content as maintained product data, not a one-time upload.")
list_items(["Review top student questions each month and add approved answers for recurring gaps.","Re-run the test questions after any course, price, policy, embedding, or prompt change.","Track whether the right source was retrieved as well as whether the final wording was correct.","Remove outdated content and rebuild the index whenever sources change.","Give students a simple way to report an incorrect or outdated answer.","Have staff review high-impact answers about payment, refunds, admissions, and safety."])

head("Project files")
list_items(["knowledge_base/academy_faq.md - academy facts template.","bot.py and web/index.html - local browser UI, retrieval, and answer generation.","web/assets/ - supplied academy logo and cleaned cover artwork.",".env.example - API configuration example; keep actual secrets private.","README.md - setup instructions and next steps."])

def footer(canvas, doc):
    canvas.saveState()
    w, _ = A4
    canvas.setStrokeColor(colors.HexColor("#D4E0E5")); canvas.line(20*mm,15*mm,w-20*mm,15*mm)
    canvas.setFont("Helvetica",8); canvas.setFillColor(colors.HexColor("#617482"))
    canvas.drawString(20*mm,10*mm,"Zukun Academy RAG Chatbot Project Guide")
    canvas.drawRightString(w-20*mm,10*mm,str(doc.page)); canvas.restoreState()

doc = SimpleDocTemplate(str(OUT), pagesize=A4, rightMargin=20*mm, leftMargin=20*mm, topMargin=18*mm, bottomMargin=21*mm, title="Zukun Academy RAG Chatbot Project Guide", author="Zukun Academy Chatbot Project")
doc.build(story, onFirstPage=footer, onLaterPages=footer)
print(OUT)
