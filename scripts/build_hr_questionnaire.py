from docx import Document
from docx.enum.table import WD_CELL_VERTICAL_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Inches, Pt, RGBColor


OUT = "Zukun_Academy_Chatbot_HR_Information_Questionnaire.docx"
PURPLE = "5B16D6"
INK = "292334"
MUTED = "746B80"
PALE = "F3EEFA"
WHITE = "FFFFFF"


def shade(cell, fill):
    tc_pr = cell._tc.get_or_add_tcPr()
    shd = OxmlElement("w:shd")
    shd.set(qn("w:fill"), fill)
    tc_pr.append(shd)


def set_cell_text(cell, text, bold=False, color=INK, size=9):
    cell.text = ""
    p = cell.paragraphs[0]
    p.paragraph_format.space_after = Pt(0)
    run = p.add_run(text)
    run.bold = bold
    run.font.name = "Aptos"
    run.font.size = Pt(size)
    run.font.color.rgb = RGBColor.from_string(color)
    cell.vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.CENTER


def set_repeat_table_header(row):
    tr_pr = row._tr.get_or_add_trPr()
    repeat = OxmlElement("w:tblHeader")
    repeat.set(qn("w:val"), "true")
    tr_pr.append(repeat)


def add_questions(doc, questions):
    table = doc.add_table(rows=1, cols=2)
    table.autofit = False
    table.columns[0].width = Inches(3.05)
    table.columns[1].width = Inches(3.65)
    table.style = "Table Grid"
    header = table.rows[0]
    set_repeat_table_header(header)
    set_cell_text(header.cells[0], "Question for HR", True, WHITE, 9)
    set_cell_text(header.cells[1], "Approved student-facing answer", True, WHITE, 9)
    for cell in header.cells:
        shade(cell, PURPLE)
    for i, question in enumerate(questions):
        row = table.add_row()
        row.cells[0].width = Inches(3.05)
        row.cells[1].width = Inches(3.65)
        set_cell_text(row.cells[0], question, False, INK, 8.5)
        set_cell_text(row.cells[1], "Type answer here", False, MUTED, 8)
        if i % 2 == 1:
            shade(row.cells[0], "FAF8FC")
            shade(row.cells[1], "FAF8FC")
    doc.add_paragraph().paragraph_format.space_after = Pt(2)


def add_section(doc, title, questions, intro=None):
    doc.add_heading(title, level=1)
    if intro:
        p = doc.add_paragraph(intro)
        p.paragraph_format.space_after = Pt(6)
    add_questions(doc, questions)


def add_course_block(doc, course):
    doc.add_heading(course, level=2)
    add_questions(doc, [
        "What is the official course name? Are there alternate titles students may use?",
        "Who is this course designed for? What skills or goals suit it?",
        "What will students be able to do after completing it?",
        "What are all modules and topics, in the correct order?",
        "Which software, tools, languages, or versions are taught?",
        "Does the course include AI? If yes, which tools and modules exactly?",
        "What projects, labs, assignments, or portfolio work are included?",
        "What is the total duration and expected weekly commitment?",
        "What prerequisites are required or recommended?",
        "What teaching format, language, and class size are available?",
        "What is the current fee, what does it include, and what extra costs may apply?",
        "Are installment plans, discounts, scholarships, or refunds available? State conditions.",
        "How are attendance, assessments, and course completion measured?",
        "What certificate is awarded, and what must a student do to receive it?",
        "What career or placement support applies to this course? What does it not guarantee?",
        "When are the next batches, and how can a student confirm a seat?",
        "What common questions do students ask about this course? Add approved answers.",
    ])


doc = Document()
sec = doc.sections[0]
sec.top_margin = Inches(0.65)
sec.bottom_margin = Inches(0.65)
sec.left_margin = Inches(0.7)
sec.right_margin = Inches(0.7)

normal = doc.styles["Normal"]
normal.font.name = "Aptos"
normal.font.size = Pt(9)
normal.font.color.rgb = RGBColor.from_string(INK)
normal.paragraph_format.space_after = Pt(5)
for style_name, size, color in [("Title", 25, INK), ("Heading 1", 15, PURPLE), ("Heading 2", 11, INK)]:
    style = doc.styles[style_name]
    style.font.name = "Aptos Display"
    style.font.size = Pt(size)
    style.font.bold = True
    style.font.color.rgb = RGBColor.from_string(color)
    style.paragraph_format.space_before = Pt(12)
    style.paragraph_format.space_after = Pt(5)

p = doc.add_paragraph(style="Title")
p.add_run("Zukun Academy Chatbot Information Questionnaire")
p.paragraph_format.space_after = Pt(5)
p = doc.add_paragraph()
p.paragraph_format.space_after = Pt(10)
r = p.add_run("Questions for HR to complete with approved student-facing answers")
r.font.size = Pt(12)
r.font.color.rgb = RGBColor.from_string(MUTED)

doc.add_paragraph(
    "Please fill in the answer column with information the academy has approved for students. "
    "The chatbot will use these answers to respond to questions about Zukun Academy. If a detail "
    "is unknown, seasonal, or varies by batch, please say so and explain how students can get the current value."
)
doc.add_heading("How to complete this questionnaire", level=1)
for item in [
    "Use exact values, conditions, and dates where possible. Avoid phrases such as ‘contact us’ without giving the actual process or details.",
    "Mark information that changes often, and say who confirms the latest version and how often it should be updated.",
    "For claims about jobs, placements, salaries, or outcomes, include the exact limits and avoid guarantees unless formally approved.",
    "Do not include private employee details, passwords, API keys, or student personal information.",
    "Attach official brochures, policies, calendars, or course outlines that support your answers. Add source links when available.",
]:
    p = doc.add_paragraph(style="List Bullet")
    p.add_run(item)

add_questions(doc, [
    "HR contact name or team for reviewing this document",
    "Date completed and date approved for student use",
    "Who owns updates to these answers?",
    "How often should the chatbot information be reviewed?",
])

add_section(doc, "Academy information", [
    "What is the academy's full official name and short description?",
    "What is the official website and which pages should students use?",
    "What are the public email address, phone/WhatsApp number, and office address?",
    "What are office hours, working days, and holiday closures?",
    "Which languages can students use to contact the academy?",
    "Is the academy currently offering in-person, online, or hybrid classes?",
    "Who may enroll (age, location, education level, or other requirements)?",
    "What should the chatbot say about the academy that is important to every student?",
])

add_section(doc, "Course catalogue and course details", [
    "Is this the complete current course list? Give the approved names and any aliases.",
    "Which courses are currently open for enrollment, paused, or discontinued?",
    "Do the course names supplied below match the official website titles? Explain differences.",
    "Are any courses combined, renamed, or offered as separate modules?",
    "Which course pages, brochures, or syllabi are the approved sources of truth?",
])
for course in [
    "Data Science with AI", "Data Analyst with AI", "Python Full Stack Developer",
    "Java Full Stack Developer", "Digital Marketing",
]:
    add_course_block(doc, course)

doc.add_page_break()
doc.add_heading("Additional courses", level=1)
doc.add_paragraph(
    "Please list every other course the academy currently offers, including courses that are "
    "temporarily not accepting enrollments. For each course, copy the question table below and "
    "complete a separate copy so the chatbot can answer course-specific questions accurately."
)
add_course_block(doc, "Additional course name")

add_section(doc, "Fees and payment", [
    "What is the current fee for each course and how long is that price valid?",
    "What is included in the fee (materials, software, exams, certificate, support)?",
    "Are there registration, exam, certificate, or other extra charges?",
    "What payment methods are accepted and where should students pay safely?",
    "Are installments available? State amounts, timing, eligibility, and late-payment rules.",
    "Are discounts, scholarships, referral offers, or group rates available? State conditions and end dates.",
    "What is the cancellation, refund, transfer, and deferral policy? Include deadlines and exceptions.",
    "Can fees change between batches? How should the chatbot explain this?",
])

add_section(doc, "Admissions and enrollment", [
    "What are the exact steps to apply, enroll, and confirm a seat?",
    "What documents or information must an applicant provide?",
    "Is there an entrance test, interview, counseling call, or skill check?",
    "How does a student choose a course if they are unsure?",
    "When does enrollment close, and how are seats confirmed?",
    "Can students join after a batch has started or transfer to another batch?",
    "What confirmation or receipt should a student receive after payment?",
    "What should a student do if they cannot access the application or payment process?",
])

add_section(doc, "Batches and learning format", [
    "What upcoming batch start dates and enrollment deadlines are confirmed?",
    "What are the class days, times, time zone, and total weekly hours for each course?",
    "Are weekday, weekend, morning, or evening batches offered?",
    "How do live online classes work, and what platform/device/internet are needed?",
    "Where are in-person classes held, and how can students find the classroom?",
    "Are recordings or make-up classes available? State access and limits.",
    "What is the attendance requirement and what happens after missed classes?",
    "Can students change format or batch after joining? What rules apply?",
])

add_section(doc, "Learning, assessment, and completion", [
    "What support can a student get from instructors or mentors during the course?",
    "How and when can students ask academic questions outside class?",
    "Are projects, assignments, exams, or practical assessments required?",
    "What are the pass, attendance, or completion requirements?",
    "What happens if a student falls behind or does not pass an assessment?",
    "Are learning materials included, and how long can students access them?",
    "What accessibility accommodations or learning support can be requested?",
    "Can a student pause, defer, repeat, or withdraw? Explain the process and costs.",
])

add_section(doc, "Certificates and career support", [
    "What certificate is issued, by whom, and when? Is it accredited or industry-recognized?",
    "What exact conditions must be met before a certificate is issued?",
    "What career services are available (resume, interview, portfolio, counseling)?",
    "What does placement assistance include, and what is outside its scope?",
    "Does the academy guarantee a job, salary, internship, or interview? State approved wording.",
    "Are outcome or placement statistics published? Provide definitions, dates, and source.",
    "Can alumni receive ongoing support? What are the terms and contact route?",
])

add_section(doc, "Student support and policies", [
    "What is the official route for academic support, admissions, payments, and complaints?",
    "What response times should students expect, and during which hours?",
    "What is the process for reporting a payment issue or suspected fraud?",
    "What student code of conduct, privacy, recording, or classroom rules apply?",
    "How does a student request a receipt, certificate reissue, or enrollment record correction?",
    "What personal data does the academy collect and how can students ask about it?",
    "What should the chatbot do if it receives a complaint, emergency, or sensitive personal information?",
])

add_section(doc, "Approved answers for other common questions", [
    "What are the 10 most frequent questions students ask that are not covered above? Add approved answers.",
    "What misunderstandings about courses, fees, certificates, or placements should the chatbot correct?",
    "What details must the chatbot never promise or disclose?",
    "When should the chatbot hand a conversation to a staff member, and how should it do that?",
    "What exact wording should the chatbot use when a fact is genuinely unknown or changing?",
])

add_section(doc, "Sources and approval", [
    "List the official documents or URLs that support the answers in this questionnaire.",
    "Who has reviewed and approved the answers for student-facing chatbot use?",
    "Are any answers restricted, confidential, or not approved for public display? Identify them.",
    "What is the next review date, and who will provide changes to the chatbot knowledge base?",
])

doc.save(OUT)
print(OUT)
