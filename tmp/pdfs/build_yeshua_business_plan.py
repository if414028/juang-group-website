from pathlib import Path
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import (
    BaseDocTemplate, PageTemplate, Frame, Paragraph, Spacer, PageBreak,
    Table, TableStyle, Image, KeepTogether, HRFlowable
)
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "output/pdf/yeshua-cafe-business-proposal-english-updated.pdf"
OUT.parent.mkdir(parents=True, exist_ok=True)

PAGE_W, PAGE_H = A4
GREEN = colors.HexColor("#123D32")
GREEN_2 = colors.HexColor("#006B4F")
MINT = colors.HexColor("#DCECE6")
CREAM = colors.HexColor("#F2F0EB")
GOLD = colors.HexColor("#CBA258")
INK = colors.HexColor("#16201D")
SOFT = colors.HexColor("#5F6B67")
WHITE = colors.white
LINE = colors.HexColor("#D9DDD9")
RED = colors.HexColor("#B94B42")

FONT = "Helvetica"
FONT_B = "Helvetica-Bold"

styles = getSampleStyleSheet()
styles.add(ParagraphStyle(name="Eyebrow", fontName=FONT_B, fontSize=8, leading=10,
                          textColor=GREEN_2, spaceAfter=4, tracking=1.3, uppercase=True))
styles.add(ParagraphStyle(name="TitleBig", fontName=FONT_B, fontSize=30, leading=33,
                          textColor=GREEN, spaceAfter=10))
styles.add(ParagraphStyle(name="H1x", fontName=FONT_B, fontSize=22, leading=25,
                          textColor=GREEN, spaceAfter=10))
styles.add(ParagraphStyle(name="H2x", fontName=FONT_B, fontSize=14, leading=17,
                          textColor=GREEN, spaceBefore=6, spaceAfter=6))
styles.add(ParagraphStyle(name="Bodyx", fontName=FONT, fontSize=9.3, leading=14,
                          textColor=INK, spaceAfter=6))
styles.add(ParagraphStyle(name="Smallx", fontName=FONT, fontSize=7.7, leading=11,
                          textColor=SOFT, spaceAfter=4))
styles.add(ParagraphStyle(name="Captionx", fontName=FONT_B, fontSize=7.5, leading=10,
                          textColor=GREEN_2, spaceAfter=3))
styles.add(ParagraphStyle(name="Whitex", fontName=FONT, fontSize=10, leading=15,
                          textColor=WHITE, spaceAfter=6))
styles.add(ParagraphStyle(name="WhiteBig", fontName=FONT_B, fontSize=28, leading=31,
                          textColor=WHITE, spaceAfter=10))
styles.add(ParagraphStyle(name="Metric", fontName=FONT_B, fontSize=19, leading=21,
                          textColor=GREEN, alignment=TA_CENTER))
styles.add(ParagraphStyle(name="MetricLabel", fontName=FONT, fontSize=7.3, leading=10,
                          textColor=SOFT, alignment=TA_CENTER))
styles.add(ParagraphStyle(name="TableHead", fontName=FONT_B, fontSize=7.5, leading=9,
                          textColor=WHITE))
styles.add(ParagraphStyle(name="TableBody", fontName=FONT, fontSize=7.3, leading=9.5,
                          textColor=INK))


def P(text, style="Bodyx"):
    return Paragraph(text, styles[style])


def money(n):
    if abs(n) >= 1_000_000_000:
        return f"Rp {n/1_000_000_000:.2f} miliar"
    return f"Rp {n/1_000_000:.1f} juta"


def section_header(no, title, subtitle=None):
    out = [P(f"{no}  /  BUSINESS PLAN", "Eyebrow"), P(title, "H1x")]
    if subtitle:
        out.append(P(subtitle, "Bodyx"))
    out.append(HRFlowable(width="100%", thickness=0.6, color=LINE, spaceBefore=2, spaceAfter=10))
    return out


def bullet(text):
    return P(f"<font color='#006B4F'>&#9679;</font>&nbsp;&nbsp;{text}", "Bodyx")


def callout(title, body, color=GREEN):
    t = Table([[P(title, "Captionx"), P(body, "Bodyx")]], colWidths=[42*mm, 122*mm])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,-1), colors.HexColor("#EAF3EF")),
        ("BOX", (0,0), (-1,-1), 0.6, color),
        ("LINEBEFORE", (0,0), (0,-1), 3, color),
        ("VALIGN", (0,0), (-1,-1), "TOP"),
        ("LEFTPADDING", (0,0), (-1,-1), 8), ("RIGHTPADDING", (0,0), (-1,-1), 8),
        ("TOPPADDING", (0,0), (-1,-1), 8), ("BOTTOMPADDING", (0,0), (-1,-1), 7),
    ]))
    return t


def data_table(headers, rows, widths, header_bg=GREEN):
    data = [[P(h, "TableHead") for h in headers]]
    data += [[P(str(c), "TableBody") for c in row] for row in rows]
    t = Table(data, colWidths=widths, repeatRows=1)
    t.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,0), header_bg),
        ("TEXTCOLOR", (0,0), (-1,0), WHITE),
        ("GRID", (0,0), (-1,-1), 0.35, LINE),
        ("VALIGN", (0,0), (-1,-1), "TOP"),
        ("ROWBACKGROUNDS", (0,1), (-1,-1), [WHITE, colors.HexColor("#F7F8F6")]),
        ("LEFTPADDING", (0,0), (-1,-1), 6), ("RIGHTPADDING", (0,0), (-1,-1), 6),
        ("TOPPADDING", (0,0), (-1,-1), 6), ("BOTTOMPADDING", (0,0), (-1,-1), 6),
    ]))
    return t


def metric_row(items):
    cells = []
    for value, label in items:
        cells.append([P(value, "Metric"), P(label, "MetricLabel")])
    t = Table([cells], colWidths=[164*mm/len(items)]*len(items), rowHeights=[22*mm])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,-1), colors.HexColor("#F7F8F6")),
        ("BOX", (0,0), (-1,-1), 0.5, LINE),
        ("INNERGRID", (0,0), (-1,-1), 0.5, LINE),
        ("VALIGN", (0,0), (-1,-1), "MIDDLE"),
        ("ALIGN", (0,0), (-1,-1), "CENTER"),
        ("TOPPADDING", (0,0), (-1,-1), 6), ("BOTTOMPADDING", (0,0), (-1,-1), 5),
    ]))
    return t


def add_photo(path, width=164*mm, height=70*mm):
    img = Image(str(ROOT / path), width=width, height=height)
    img.hAlign = "CENTER"
    return img


class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        canvas.Canvas.__init__(self, *args, **kwargs)
        self._saved_page_states = []
    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()
    def save(self):
        total = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_number(total)
            canvas.Canvas.showPage(self)
        canvas.Canvas.save(self)
    def draw_page_number(self, total):
        if self._pageNumber == 1:
            return
        self.setFont(FONT, 7)
        self.setFillColor(SOFT)
        self.drawString(23*mm, 12*mm, "YESHUA CAFE  /  INVESTOR DISCUSSION DRAFT")
        self.drawRightString(PAGE_W-23*mm, 12*mm, f"{self._pageNumber} / {total}")


def cover_bg(c, doc):
    c.saveState()
    c.setFillColor(GREEN)
    c.rect(0, 0, PAGE_W, PAGE_H, fill=1, stroke=0)
    c.setFillColor(colors.HexColor("#194F41"))
    c.circle(PAGE_W*0.9, PAGE_H*0.15, 80*mm, fill=1, stroke=0)
    c.setFillColor(GOLD)
    c.rect(0, PAGE_H-8*mm, PAGE_W, 8*mm, fill=1, stroke=0)
    c.restoreState()


def standard_bg(c, doc):
    c.saveState()
    c.setFillColor(CREAM)
    c.rect(0, 0, PAGE_W, PAGE_H, fill=1, stroke=0)
    c.setFillColor(GREEN)
    c.rect(0, PAGE_H-5*mm, PAGE_W, 5*mm, fill=1, stroke=0)
    c.restoreState()


doc = BaseDocTemplate(str(OUT), pagesize=A4, leftMargin=23*mm, rightMargin=23*mm,
                      topMargin=20*mm, bottomMargin=20*mm, title="Yeshua Cafe Business Plan")
cover_frame = Frame(23*mm, 20*mm, 164*mm, 252*mm, id="cover", leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0)
body_frame = Frame(23*mm, 20*mm, 164*mm, 252*mm, id="body", leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0)
doc.addPageTemplates([
    PageTemplate(id="Cover", frames=cover_frame, onPage=cover_bg),
    PageTemplate(id="Body", frames=body_frame, onPage=standard_bg),
])

story = []

# 1 Cover
story += [Spacer(1, 27*mm)]
logo = Image(str(ROOT / "public/brand/official/yeshua-cafe-logo.png"), width=38*mm, height=38*mm)
logo.hAlign = "LEFT"
story += [logo, Spacer(1, 12*mm), P("INVESTOR DISCUSSION DRAFT", "Eyebrow"),
          P("Yeshua Cafe", "WhiteBig"),
          P("Inclusive hospitality, disciplined operations, and a cafe designed to create meaningful employment.", "Whitex"),
          Spacer(1, 70*mm),
          P("BUSINESS PLAN + MARKETING STRATEGY", "Whitex"),
          P("Flagship pilot candidates: Pejaten, South Jakarta and North Jakarta<br/>Long-term target: 20 Jakarta branches, followed by regional expansion", "Whitex"),
          Spacer(1, 8*mm), P("Prepared for Juang Group  |  Updated 3 August 2026", "Whitex"), PageBreak()]
doc.handle_nextPageTemplate("Body")

# 2 Document note & contents
story += section_header("00", "How to use this document", "A decision document for founder and investor discussions - not a guarantee of returns.")
story += [callout("STATUS", "This is a preliminary business plan based on current concept materials and explicit working assumptions. Lease quotations, floor plans, supplier quotations, staffing assessments, and founder funding terms must be validated before an investment agreement is signed."), Spacer(1, 8)]
story += [P("Document map", "H2x")]
toc = [
    ("01", "Executive summary"), ("02", "Investment thesis"), ("03", "Concept and customer promise"),
    ("04", "Market and location strategy"), ("05", "Inclusive employment model"), ("06", "Products and revenue model"),
    ("07", "Operations and technology"), ("08", "Marketing and sales strategy"), ("09", "Financial model"),
    ("10", "Funding requirement"), ("11", "Roadmap, governance, and risk"), ("12", "Due diligence checklist")
]
story += [data_table(["SECTION", "CONTENTS"], toc, [24*mm, 140*mm])]
story += [Spacer(1, 8), P("Brand note", "H2x"), P("The website's current cafe brand is Yeshua Cafe, operating under Juang Group. If the commercial name will instead be Juang Coffee, the legal name, trademark, signage, permits, social channels, and investor materials should be aligned before launch.", "Bodyx"), PageBreak()]

# 3 Executive summary
story += section_header("01", "Executive summary", "A large-format flagship pilot that proves the economics, operating system, and inclusive employment model before a 20-branch Jakarta rollout.")
story += [metric_row([("300-500", "Seats per flagship pilot"), ("Rp 10-15B", "Funding per flagship"), ("20", "Long-term Jakarta branches"), ("6-8 yrs", "Indicative rollout horizon")]), Spacer(1, 9)]
story += [P("The opportunity", "H2x"), P("Yeshua Cafe is positioned as an accessible, community-oriented cafe with a distinctive menu, digitally connected service, and structured employment opportunities for people with Down syndrome. The business is designed to compete first on hospitality, product quality, convenience, and operating consistency. Its social mission strengthens the brand, but it must never replace commercial discipline or fair employment practices.", "Bodyx")]
story += [P("Recommended strategy", "H2x"), bullet("Develop the first 300-500 seat flagship through a formal site competition between Pejaten and a selected North Jakarta micro-market."), bullet("Release Rp 10-15 billion per flagship in milestones, with Rp 12.5 billion used as the planning base case."), bullet("Treat the 20-branch Jakarta target as a stage-gated network plan rather than a commitment to sign 20 leases immediately."), bullet("Use supported roles, task design, job coaching, visual SOPs, and equal pay for equal responsibilities."), bullet("Build demand through destination events, neighborhood communities, offices, campuses, families, corporate catering, CRM, and delivery."), bullet("Require weekly operating dashboards and monthly investor reporting from day one.")]
story += [callout("INVESTMENT GATE", "Do not sign a second flagship lease until the first site records at least six consecutive months of positive store-level EBITDA, customer rating of at least 4.5/5, order accuracy above 98%, and staff retention above 85%. At Rp 10-15 billion per location, 20 equivalent branches imply Rp 200-300 billion of gross opening capital before inflation, central overhead, and regional expansion."), PageBreak()]

# 4 Thesis
story += section_header("02", "Investment thesis", "Why this concept can become investable - and what still needs proof.")
thesis_rows = [
    ("Distinctive proposition", "Inclusive service and community programming create memorability beyond menu and interior design.", "Prove repeat visits and willingness to recommend."),
    ("Multi-daypart demand", "Coffee, meals, desserts, work sessions, gatherings, and events can spread demand across the day.", "Prove traffic by hour and category margin."),
    ("Digital control", "QR ordering and integrated cashier, kitchen, and inventory data support traceability and lower input error.", "Prove uptime, staff adoption, and clean inventory records."),
    ("Replicable operating model", "Visual SOPs, training modules, production zoning, and role-based workflows can support a 20-branch network.", "Prove the flagship before replication."),
    ("Measurable impact", "Employment, paid hours, training progression, retention, and family satisfaction can be reported.", "Use consent-based reporting and protect employee dignity."),
]
story += [data_table(["VALUE DRIVER", "WHY IT MATTERS", "EVIDENCE REQUIRED"], thesis_rows, [37*mm, 66*mm, 61*mm])]
story += [Spacer(1, 8), P("What investors are actually underwriting", "H2x"), P("Investors are not only funding a cafe fit-out. They are underwriting management capability, location quality, repeat customer behavior, unit economics, food safety, inclusive workforce execution, and the founder's ability to report transparently. The proposal therefore uses stage gates rather than optimistic branch-count promises.", "Bodyx"), PageBreak()]

# 5 Concept
story += section_header("03", "Concept and customer promise", "A welcoming cafe where quality, convenience, community, and meaningful work meet.")
story += [add_photo("public/images/juang-cafe/community-cafe.webp"), Spacer(1, 7)]
promise_rows = [
    ("Product", "Reliable coffee and beverages, signature rice dishes, meat pies, shawarmas, familiar comfort food, and desserts."),
    ("Place", "Warm, accessible seating for studying, work, informal meetings, families, and community gatherings."),
    ("People", "Hospitality delivered by a mixed team, including people with Down syndrome in roles matched to individual readiness and strengths."),
    ("Process", "QR ordering, cashier, kitchen, and stock data connected for speed, accuracy, and traceability."),
    ("Community", "Workshops, open mic events, family programs, creator collaborations, and inclusive employment education."),
]
story += [data_table(["PILLAR", "CUSTOMER PROMISE"], promise_rows, [35*mm, 129*mm])]
story += [Spacer(1, 7), callout("POSITIONING", "A modern neighborhood cafe with disciplined service and authentic social impact - approachable enough for frequent visits, distinctive enough to be remembered."), PageBreak()]

# 6 Customer & market
story += section_header("04", "Market and customer strategy", "Start with reachable customer groups and measurable occasions, not a broad claim that the cafe is for everyone.")
segments = [
    ("Students and young adults", "Study, affordable meals, Wi-Fi, group work", "Lunch bundles, study hours, campus ambassadors"),
    ("Professionals and remote workers", "Coffee, workspace, informal meetings", "Morning coffee, workday bundles, company partnerships"),
    ("Families", "Safe, welcoming outing and meaningful story", "Weekend programs, family bundles, accessible hospitality"),
    ("Communities and creators", "Gathering venue, workshops, open mic", "Event packages, co-created calendar, UGC"),
    ("Corporate and institutions", "Catering, CSR, employee engagement", "Catering, hosted sessions, partnership programs"),
]
story += [data_table(["SEGMENT", "CORE NEED", "OFFER"], segments, [43*mm, 58*mm, 63*mm])]
story += [Spacer(1, 8), P("Market evidence", "H2x"), P("BPS publishes annual demographic and economic profiles for both South Jakarta and North Jakarta, providing an official base for final catchment analysis. ILO reporting shows that access to formal employment remains materially lower for people with disabilities in Indonesia, reinforcing the relevance of a structured employment model. The final site memo must add primary fieldwork: pedestrian counts, competitor mapping, rent quotations, parking, delivery radius, and customer interviews.", "Bodyx")]
story += [callout("RESEARCH GAP", "The business case should not use city-wide population as a substitute for store demand. A 1-3 km catchment study and three-day footfall count are mandatory before lease signing."), PageBreak()]

# 7 Location comparison
story += section_header("04A", "Location strategy: Pejaten vs North Jakarta", "Both are flagship candidates. The first lease should go to the property with the strongest catchment, access, technical readiness, and occupancy economics.")
loc_rows = [
    ("Catchment clarity", "Strong: residential, education, offices, community access", "Varies widely by Kelapa Gading, PIK, Pluit, Koja, etc."),
    ("Flagship suitability", "Strong if a large site has parking, frontage, and event capacity", "Potentially strong, but dependent on the selected cluster and rent"),
    ("Brand fit", "Community flagship, study/work, family, events", "Lifestyle, destination, family, or mall flagship depending on site"),
    ("Delivery potential", "Dense mixed-use catchment", "Strong in selected clusters"),
    ("Key risk", "Congestion, parking, frontage, rent escalation", "Over-rent, destination dependence, unclear first catchment"),
    ("Recommendation", "Shortlist 3 large-format properties", "Select 2 micro-markets, then shortlist 3 properties"),
]
story += [data_table(["CRITERION", "PEJATEN", "NORTH JAKARTA"], loc_rows, [39*mm, 63*mm, 62*mm])]
story += [Spacer(1, 8), P("Lease decision scorecard", "H2x")]
score_rows = [
    ("Rent + service charge", "20%", "Occupancy cost target <= 12% of mature revenue"),
    ("Footfall and visibility", "20%", "Count by hour on weekday and weekend"),
    ("Access, parking, ride-hailing", "15%", "Safe pickup/drop-off and accessible entrance"),
    ("Catchment demand", "15%", "Offices, schools, residences, communities"),
    ("Kitchen and utilities", "10%", "Power, exhaust, water, grease trap, waste"),
    ("Competition and adjacency", "10%", "Healthy demand without direct price war"),
    ("Lease flexibility", "10%", "Fit-out period, break clause, escalation cap"),
]
story += [data_table(["FACTOR", "WEIGHT", "PASS CONDITION"], score_rows, [58*mm, 22*mm, 84*mm]), PageBreak()]

# 8 Inclusive employment
story += section_header("05", "Inclusive employment operating model", "Employment must be structured, paid, safe, and based on each person's abilities - not used as promotional decoration.")
story += [add_photo("public/images/juang-cafe/inclusive-employment.webp"), Spacer(1, 7)]
roles = [
    ("Guest welcome", "Greeting, menu guidance, table numbers", "Script cards, buddy support, calm escalation"),
    ("Table support", "Delivering items, clearing, resetting", "Color/number system, route practice"),
    ("Packaging", "Labels, cutlery, takeaway checks", "Picture checklist, two-step verification"),
    ("Beverage prep support", "Measured non-hazardous tasks", "Pre-portioned ingredients, visual sequence"),
    ("Stock and cleaning support", "Counting, arranging, scheduled cleaning", "Task boards, PPE, supervisor sign-off"),
]
story += [data_table(["ROLE FAMILY", "TASK EXAMPLES", "ACCOMMODATION"], roles, [35*mm, 64*mm, 65*mm])]
story += [Spacer(1, 7), P("Employment principles", "H2x"), bullet("Individual assessment and voluntary participation; never assume identical capabilities."), bullet("Equal pay for the same role and responsibility, consistent with Law No. 8/2016."), bullet("Accessible facilities, reasonable accommodation, feedback mechanism, and safeguarding."), bullet("Job coach or trained shift mentor, visual SOPs, predictable schedules, and progressive certification."), bullet("Consent-based storytelling: employees may decline photos or public narratives without employment consequences."), PageBreak()]

# 9 workforce journey
story += section_header("05A", "Workforce journey and impact measurement", "A repeatable pathway from recruitment to independent task ownership.")
journey = [
    ("1. Partner", "Engage foundations, schools, families, disability employment services, and professionals."),
    ("2. Assess", "Map preferences, communication needs, transport, sensory considerations, and task readiness."),
    ("3. Prepare", "Two-week paid training lab using visual SOPs and simulated service."),
    ("4. Place", "Assign supported roles with a buddy and documented accommodations."),
    ("5. Progress", "Review weekly during probation, then monthly; certify skills by task."),
    ("6. Sustain", "Offer fair scheduling, feedback, career steps, family communication with consent, and grievance channels."),
]
story += [data_table(["STAGE", "OPERATING REQUIREMENT"], journey, [36*mm, 128*mm])]
story += [Spacer(1, 8), P("Impact dashboard", "H2x")]
impact = [
    ("Employment", "Number of employees with Down syndrome; paid hours; retention"),
    ("Capability", "Tasks certified; training hours; independent task completion"),
    ("Quality", "Order accuracy; service recovery; customer rating"),
    ("Well-being", "Employee feedback; family feedback with consent; reported incidents"),
    ("Fairness", "Pay parity by role; schedule stability; promotion opportunities"),
]
story += [data_table(["DIMENSION", "MEASURES"], impact, [38*mm, 126*mm])]
story += [Spacer(1, 7), callout("YEAR-1 IMPACT TARGET", "Illustrative target: 4-6 employees with Down syndrome, at least 80 paid training hours per participant, 85% retention, and at least three certified task families per participant. Final targets require partner and candidate assessment."), PageBreak()]

# 10 Menu
story += section_header("06", "Products and revenue model", "A focused launch menu should protect speed, quality, margin, and training simplicity.")
story += [add_photo("public/images/juang-cafe/menu-concept-real-menu.webp"), Spacer(1, 7)]
rev = [
    ("Dine-in food and beverage", "70-75%", "Core traffic; bundles and add-ons lift average order value"),
    ("Delivery and takeaway", "12-15%", "Incremental reach; manage platform commission and packaging"),
    ("Events and community packages", "5-8%", "Space rental, food packages, workshops, open mic"),
    ("Catering and corporate orders", "5-8%", "Pre-order trays, meetings, CSR and institutional programs"),
    ("Retail / future products", "0-5%", "Coffee, chocolate, packaged items after operations stabilize"),
]
story += [data_table(["REVENUE STREAM", "MATURE MIX", "COMMERCIAL LOGIC"], rev, [49*mm, 25*mm, 90*mm])]
story += [Spacer(1, 7), P("Menu engineering rules", "H2x"), bullet("Launch with no more than 25-30 core SKUs plus limited seasonal items."), bullet("Every SKU requires recipe card, portion, allergens, cost, prep time, target margin, and photo standard."), bullet("Target blended COGS of 33-35%; review low-volume and low-margin items monthly."), bullet("Use signature items for distinction, while familiar products reduce trial friction."), PageBreak()]

# 11 Operations tech
story += section_header("07", "Operations and connected technology", "Every order and stock movement should create a traceable record.")
story += [add_photo("public/images/juang-cafe/connected-operations.webp"), Spacer(1, 7)]
flow = [
    ("1. Table QR", "Customer scans, views menu, notes allergies/preferences, and submits order."),
    ("2. POS and payment", "Order enters cashier system with table, items, discounts, payment, and audit trail."),
    ("3. Kitchen display", "Food and beverage stations receive timed tickets; status is visible."),
    ("4. Service", "Runner receives ready notification and delivers to numbered table."),
    ("5. Inventory", "Recipe quantities decrement stock; wastage, voids, and transfers require reason codes."),
    ("6. Management", "Founder and investors receive role-based dashboards, not unrestricted raw-system access."),
]
story += [data_table(["FLOW", "CONTROL"], flow, [38*mm, 126*mm])]
story += [Spacer(1, 7), P("Required dashboards", "H2x"), bullet("Daily sales, transaction count, AOV, category mix, discounts, voids, and refunds."), bullet("Ticket time, order accuracy, item availability, wastage, and stock variance."), bullet("Labor hours, sales per labor hour, attendance, training, and safety incidents."), bullet("Cash reconciliation, payable calendar, runway, and investor reporting pack."), PageBreak()]

# 12 SOP
story += section_header("07A", "Store operating model", "Controls that protect guest experience, food safety, and financial transparency.")
sop = [
    ("Opening", "Cash float, hygiene checklist, equipment check, stock count, briefing, role board"),
    ("Service", "Greeting, QR support, ticket monitoring, table delivery, feedback, recovery"),
    ("Food safety", "Receiving, temperature log, FIFO/FEFO, allergen control, cleaning schedule"),
    ("Cash and discounts", "Role permissions, manager approval, end-shift reconciliation, exception report"),
    ("Inventory", "Recipe-level usage, daily critical count, weekly cycle count, monthly full count"),
    ("Inclusive supervision", "Visual instructions, buddy coverage, break planning, calm escalation, incident notes"),
    ("Closing", "Waste record, cash close, stock alerts, cleaning verification, maintenance log"),
]
story += [data_table(["PROCESS", "MINIMUM STANDARD"], sop, [39*mm, 125*mm])]
story += [Spacer(1, 8), P("Suggested flagship organization", "H2x")]
org = [
    ("General / Store Manager", "1", "P&L, people, compliance, reporting"),
    ("Department and Shift Leaders", "5-7", "Front of house, kitchen, bar, events, coaching, quality"),
    ("Bar / kitchen / service crew", "24-34", "High-volume production, service, and events"),
    ("Inclusive service associates", "10-20", "Supported service roles; mix of full/part time"),
    ("Job coaches / partner support", "2-3 / retainer", "Assessment, training, accommodation support"),
]
story += [data_table(["ROLE", "HEADCOUNT", "ACCOUNTABILITY"], org, [51*mm, 28*mm, 85*mm]), PageBreak()]

# 13 Marketing strategy
story += section_header("08", "Marketing strategy", "Community before campaign: build a repeatable local demand engine instead of depending on launch hype.")
story += [add_photo("public/images/juang-cafe/marketing-ecosystem.webp"), Spacer(1, 7)]
channels = [
    ("Owned", "Website, Google Business Profile, Instagram, TikTok, WhatsApp CRM", "Discovery, proof, retention"),
    ("Local", "Residential groups, schools, offices, churches, communities", "Trust and recurring visits"),
    ("Partnership", "Universities, foundations, companies, creators, event organizers", "Shared audiences and programs"),
    ("Paid", "Radius ads, search, maps, retargeting", "Capture high-intent demand"),
    ("Earned", "PR, founder story, inclusive employment education", "Credibility - with employee consent"),
]
story += [data_table(["ENGINE", "TACTICS", "ROLE"], channels, [29*mm, 82*mm, 53*mm])]
story += [Spacer(1, 7), callout("MESSAGE HIERARCHY", "Lead with quality and hospitality. Support with convenience and community. Explain inclusion through dignified, factual stories about paid work, skills, and opportunity - never pity-based messaging."), PageBreak()]

# 14 Funnel
story += section_header("08A", "Customer acquisition and retention funnel", "A measurable path from nearby awareness to repeat visits and advocacy.")
funnel = [
    ("Awareness", "Maps SEO, local PR, creator previews, partner audiences", "Reach, map views, branded searches"),
    ("Consideration", "Menu, pricing, location, reviews, employee story", "Website visits, direction requests, saves"),
    ("First visit", "Opening offer, bundles, events, sampling", "New customers, acquisition cost"),
    ("Second visit", "Receipt QR, WhatsApp opt-in, return offer", "30-day repeat rate"),
    ("Habit", "Daypart programs, loyalty, pre-order, community calendar", "Visits/customer, AOV, retention"),
    ("Advocacy", "Reviews, UGC, referral, partner stories", "NPS, rating, referrals"),
]
story += [data_table(["STAGE", "ACTIVATION", "PRIMARY KPI"], funnel, [31*mm, 85*mm, 48*mm])]
story += [Spacer(1, 8), P("First 90 days campaign", "H2x")]
plan90 = [
    ("T-60 to T-30", "Build", "Recruit partners, publish build story, collect waitlist, seed Google profile"),
    ("T-30 to T-7", "Preview", "Community tastings, staff stories with consent, creator and neighbor previews"),
    ("Launch week", "Experience", "Controlled reservations, daily service review, no uncontrolled discount crowd"),
    ("Days 8-30", "Correct", "Fix menu, ticket time, stockouts, review response, targeted radius ads"),
    ("Days 31-90", "Retain", "CRM, workday offers, events, catering outreach, referral program"),
]
story += [data_table(["PERIOD", "OBJECTIVE", "ACTION"], plan90, [30*mm, 30*mm, 104*mm]), PageBreak()]

# 15 content calendar budget
story += section_header("08B", "Marketing operating plan and budget", "The marketing function must produce demand, customer data, and learning - not only content output.")
story += [P("Illustrative monthly marketing budget", "H2x")]
budget = [
    ("Content production", "Rp 15 million", "Photo/video, employee consent workflow, menu assets"),
    ("Paid media", "Rp 20 million", "Maps/search, city targeting, and radius campaigns"),
    ("Community and events", "Rp 15 million", "Hosts, equipment, sampling, partnership materials"),
    ("CRM and loyalty", "Rp 5 million", "WhatsApp tools, offers, database hygiene"),
    ("PR / creators", "Rp 10 million", "Selective previews, media relations, and creator partnerships"),
    ("Testing reserve", "Rp 10 million", "New offers, channels, and branch launch tests"),
]
story += [data_table(["LINE", "MONTHLY", "PURPOSE"], budget, [47*mm, 29*mm, 88*mm])]
story += [Spacer(1, 8), P("Weekly content rhythm", "H2x"), bullet("2 product-led posts: menu, craftsmanship, value, and usage occasion."), bullet("1 people-and-process story: skills, teamwork, training, or service - consent required."), bullet("1 community post: events, partner, customer story, or neighborhood guide."), bullet("Daily utility: opening hours, availability, event reminders, directions, and customer replies."), bullet("Monthly proof: impact metrics, customer feedback, operational improvement, and partner outcomes."), PageBreak()]

# 16 Financial assumptions
story += section_header("09", "Financial model: key assumptions", "All figures are indicative, pre-tax, and must be replaced with quotations and a signed lease model.")
assumptions = [
    ("Flagship format", "Approximately 900-1,300 sqm, 300-500 seats, one initial flagship"),
    ("Trading days", "30 days per month"),
    ("Mature transactions", "700 per day in the planning base case"),
    ("Average order value", "Rp 95,000"),
    ("Ancillary revenue", "Rp 255 million/month from events, catering, venue packages, and retail"),
    ("Blended COGS", "34% of revenue"),
    ("Mature fixed/semi-fixed opex", "Rp 1.05 billion/month"),
    ("Occupancy target", "Rent + service charge <= 12% of mature revenue"),
    ("Ramp", "9-15 months to mature flagship run-rate"),
]
story += [data_table(["ASSUMPTION", "WORKING VALUE"], assumptions, [63*mm, 101*mm])]
story += [Spacer(1, 8), callout("FINANCIAL DISCIPLINE", "The most sensitive drivers are transactions/day, AOV, seat utilization, COGS, rent, payroll, and event income. A large venue has a materially higher fixed-cost base: downside testing is mandatory. The investment committee should review a spreadsheet model with editable assumptions before approval."), PageBreak()]

# 17 Capex
story += section_header("09A", "Indicative flagship startup funding", "Client target: Rp 10-15 billion per 300-500 seat flagship. The model uses Rp 12.5 billion as a midpoint and excludes land purchase, financing costs, and the full multi-year lease commitment.")
capex = [
    ("Large-format renovation and MEP", 4_000_000_000), ("Kitchen, coffee, and production equipment", 2_000_000_000),
    ("Furniture, signage, event equipment, smallwares", 1_100_000_000), ("POS, QR, KDS, network, CCTV, access control", 350_000_000),
    ("Permits, design, professional fees, pre-opening", 350_000_000), ("Recruitment and inclusive training", 450_000_000),
    ("Lease deposit / initial advance", 1_800_000_000), ("Opening inventory", 250_000_000),
    ("Working capital reserve", 1_450_000_000), ("Contingency", 750_000_000),
]
total_capex = sum(v for _,v in capex)
cap_rows = [(k, money(v), f"{v/total_capex*100:.1f}%") for k,v in capex] + [("TOTAL", money(total_capex), "100.0%")]
story += [data_table(["USE OF FUNDS", "AMOUNT", "SHARE"], cap_rows, [86*mm, 48*mm, 30*mm])]
story += [Spacer(1, 7), P("Funding release gates", "H2x"), bullet("Gate 1: flagship concept validation, property shortlist, partner MoUs, and preliminary quotations."), bullet("Gate 2: signed lease subject to technical due diligence, traffic study, occupancy-cost test, and permit pathway."), bullet("Gate 3: design approval, fit-out milestones, and equipment acceptance."), bullet("Gate 4: high-volume operating simulation, hiring, inclusive training, soft opening, and operating reserve."), PageBreak()]

# 18 Unit economics
story += section_header("09B", "Mature monthly unit economics", "Illustrative base case after the store reaches stable operations.")
sales = 700*95_000*30 + 255_000_000
cogs = sales*.34
gross = sales-cogs
opex = 1_050_000_000
ebitda = gross-opex
econ = [
    ("Core dine-in/takeaway revenue", money(700*95_000*30), "88.7%"),
    ("Events, catering, venue, and retail revenue", money(255_000_000), "11.3%"),
    ("Total revenue", money(sales), "100.0%"),
    ("COGS", money(-cogs), "34.0%"),
    ("Gross profit", money(gross), "66.0%"),
    ("Operating expenses", money(-opex), "46.7%"),
    ("Store EBITDA", money(ebitda), f"{ebitda/sales*100:.1f}%"),
]
story += [data_table(["LINE", "MONTHLY", "% REVENUE"], econ, [85*mm, 48*mm, 31*mm])]
story += [Spacer(1, 9), metric_row([("Rp 2.25B", "Mature monthly revenue"), ("Rp 435M", "Store EBITDA"), ("19.3%", "EBITDA margin"), ("~29 mo", "Simple payback at Rp 12.5B")])]
story += [Spacer(1, 8), P("Break-even", "H2x"), P("At a 66% contribution margin and Rp 1.05 billion monthly fixed/semi-fixed operating cost, the indicative revenue break-even is approximately Rp 1.59 billion per month. At an AOV of Rp 95,000 and Rp 150 million ancillary revenue, this implies roughly 506 transactions per day.", "Bodyx"), PageBreak()]

# 19 Scenarios
story += section_header("09C", "Scenario analysis", "The investment decision should be based on downside survivability, not only the base case.")
scenarios = [
    ("Conservative", "420", "Rp 85k", "Rp 1.20B", "37%", "Rp 900M", "-Rp 144M", "Negative"),
    ("Base", "700", "Rp 95k", "Rp 2.25B", "34%", "Rp 1.05B", "Rp 435M", "19.3%"),
    ("Upside", "950", "Rp 105k", "Rp 3.35B", "32%", "Rp 1.30B", "Rp 978M", "29.2%"),
]
story += [data_table(["CASE", "TX/DAY", "AOV", "REVENUE", "COGS", "OPEX", "EBITDA", "MARGIN"], scenarios,
                     [26*mm, 18*mm, 19*mm, 24*mm, 18*mm, 22*mm, 23*mm, 14*mm])]
story += [Spacer(1, 9), P("Three-year indicative ramp", "H2x")]
years = [
    ("Year 1", "Rp 13.5B", "Rp 0.2B", "1.5%", "Opening and large-format ramp; protect cash"),
    ("Year 2", "Rp 24.0B", "Rp 3.6B", "15.0%", "Full-year flagship optimization"),
    ("Year 3", "Rp 28.0B", "Rp 5.2B", "18.6%", "Mature flagship; controlled rollout"),
]
story += [data_table(["YEAR", "REVENUE", "EBITDA", "MARGIN", "COMMENT"], years, [23*mm, 31*mm, 28*mm, 21*mm, 61*mm])]
story += [Spacer(1, 8), callout("CAUTION", "These are planning figures, not audited forecasts. Taxes, depreciation, financing, owner compensation, platform commissions, and corporate overhead require confirmation in the full spreadsheet model."), PageBreak()]

# 20 Funding proposal
story += section_header("10", "Investment structure and use of funds", "Funding should be milestone-based with clear governance, information rights, and downside protection.")
story += [P("Illustrative funding ask", "H2x"), P("Rp 10-15 billion for one 300-500 seat flagship, released by milestones. The working financial model uses Rp 12.5 billion. The final amount must be reset after receiving at least three large-format fit-out quotations, two equipment quotations, a negotiated lease term sheet, event and parking capacity studies, and an 18-month payroll and working-capital plan.", "Bodyx")]
deal = [
    ("Equity", "Investor owns shares in operating company", "Alignment and long-term upside", "Valuation and dilution must be negotiated"),
    ("Convertible instrument", "Debt converts under agreed trigger", "Defers valuation discussion", "Needs legal drafting and clear cap/discount"),
    ("Revenue/profit share", "Return linked to store performance", "Simple commercial logic", "Can strain cash and create accounting disputes"),
    ("Project SPV", "Pilot store ring-fenced in an entity", "Clear store economics and governance", "More administration and intercompany agreements"),
]
story += [data_table(["OPTION", "MECHANISM", "ADVANTAGE", "CAUTION"], deal, [30*mm, 50*mm, 42*mm, 42*mm])]
story += [Spacer(1, 8), P("Recommended investor protections", "H2x"), bullet("Board or reserved-matter approval for new debt, second lease, related-party transactions, and major capex."), bullet("Monthly management accounts and quarterly impact report."), bullet("Bank dual-control above an agreed threshold and documented procurement."), bullet("Founder vesting/commitment, IP ownership, and related-party disclosure."), bullet("Pre-agreed policy for dividends versus reinvestment."), PageBreak()]

# 21 Roadmap
story += section_header("11", "Roadmap and decision gates", "Scale only after evidence, systems, and people are ready.")
road = [
    ("0-3 months", "Validate", "Flagship brief, site competition, demand study, partner MoUs, quotations", "Investment committee approval"),
    ("3-6 months", "Secure", "Lease, design, permits, vendors, technology, high-volume recruitment", "Technical and legal due diligence"),
    ("6-12 months", "Build", "Large-format fit-out, SOPs, menu testing, hiring, inclusive training", "Pre-opening readiness audit"),
    ("12-15 months", "Launch", "Soft opening, controlled capacity, events, daily corrections", "90-day stabilization review"),
    ("15-24 months", "Optimize", "Menu engineering, CRM, catering, venue utilization, impact reporting", "Six months positive KPI trend"),
    ("Years 2-3", "Prove cluster", "Open branches 2-4 only after flagship evidence", "Cluster economics and management bench"),
    ("Years 3-5", "Scale Jakarta", "Grow toward 8-12 branches with central systems", "Portfolio cash flow and governance"),
    ("Years 5-8", "Complete & expand", "Target 20 Jakarta branches, then selected regions", "Regional go / no-go"),
]
story += [data_table(["TIMING", "PHASE", "WORK", "GATE"], road, [24*mm, 26*mm, 72*mm, 42*mm])]
story += [Spacer(1, 9), P("Expansion KPI gate", "H2x")]
story += [metric_row([(">=15%", "Store EBITDA margin"), (">=98%", "Order accuracy"), (">=4.5", "Customer rating"), (">=85%", "Staff retention")])]
story += [Spacer(1, 7), P("In addition: positive operating cash flow, stock variance below 2%, occupancy cost below 12%, documented management bench, central procurement readiness, and a clean six-month reporting record. A 20-branch network will require format standardization, regional managers, a training academy, central quality assurance, and significantly more capital than the first flagship.", "Bodyx"), PageBreak()]

# 22 Governance / risk
story += section_header("11A", "Risk register and mitigation", "The strongest plan names its failure modes before investors do.")
risks = [
    ("Traffic below plan", "High", "Field counts, conservative lease, pre-opening partnerships, weekly funnel tracking"),
    ("Rent pressure", "High", "Occupancy cap, escalation ceiling, fit-out period, break/renewal protections"),
    ("Service inconsistency", "High", "Soft opening, visual SOPs, shift coaching, limited launch menu"),
    ("Tokenistic inclusion or safeguarding failure", "High", "Partner oversight, consent, grievance process, trained mentors, incident protocol"),
    ("Food safety", "High", "HACCP-inspired controls, logs, supplier approval, training, audits"),
    ("Cash leakage / stock loss", "Medium-High", "POS permissions, CCTV, cycle counts, variance reports, dual approval"),
    ("Founder dependency", "Medium-High", "Delegation, management roles, SOPs, board reporting, succession plan"),
    ("Technology outage", "Medium", "Offline procedure, backups, support SLA, access controls"),
    ("Reputation backlash", "Medium", "Dignified messaging, transparent corrections, employee privacy"),
    ("Regulatory delay", "Medium", "Permit checklist, professional review, halal pathway, lease condition precedent"),
]
story += [data_table(["RISK", "LEVEL", "MITIGATION"], risks, [47*mm, 24*mm, 93*mm])]
story += [Spacer(1, 7), P("Governance cadence", "H2x"), P("Daily store huddle; weekly operations review; monthly management accounts and impact dashboard; quarterly board/investor review; annual strategy and compensation review.", "Bodyx"), PageBreak()]

# 23 Compliance
story += section_header("11B", "Legal and compliance workstream", "Obtain professional legal, tax, employment, accessibility, and food-safety advice before commitments.")
compliance = [
    ("Entity and governance", "Operating company, shareholders agreement, tax registrations, beneficial ownership"),
    ("Business licensing", "NIB and applicable KBLI through OSS; location and building requirements"),
    ("Food and beverage", "Food safety, sanitation, labeling/allergens, supplier records, halal certification pathway"),
    ("Employment", "Contracts, wages, BPJS, hours, leave, equal treatment, accommodation, grievance mechanism"),
    ("Accessibility", "Entrance, circulation, toilet, signage, emergency procedures, reasonable accommodation"),
    ("Data and technology", "Customer consent, CRM data, access control, backups, vendor agreements"),
    ("IP and brand", "Trademark search/registration, logo ownership, domain/social handles, recipe confidentiality"),
    ("Lease", "Use clause, signage, fit-out, utilities, restoration, escalation, break/renewal, assignment"),
]
story += [data_table(["AREA", "MINIMUM REVIEW"], compliance, [46*mm, 118*mm])]
story += [Spacer(1, 8), callout("TIME-SENSITIVE", "BPJPH states that the halal-certification phase for food and beverage products expands in October 2026. The founder should confirm the applicable category and timeline with BPJPH or an accredited adviser before launch."), PageBreak()]

# 24 DD checklist
story += section_header("12", "Investor due diligence checklist", "Information required to convert this discussion draft into a bankable plan.")
dd = [
    ("Founder and entity", "Founder CV, company documents, cap table, liabilities, related parties"),
    ("Funding", "Amount sought, founder contribution, instrument, valuation/return expectation, use of funds"),
    ("Property", "Exact address, 900-1,300 sqm feasibility, floor plan, rent, service charge, deposit, term, parking, event egress, utilities"),
    ("Market", "Catchment map, footfall counts, competitor price/menu audit, customer interviews"),
    ("Menu", "Final SKUs, selling prices, recipe costs, supplier quotations, prep time, allergens"),
    ("People", "35-55+ person flagship org chart, salary plan, inclusive employment partners, assessment and coaching cost"),
    ("Operations", "Hours, capacity, equipment list, SOP index, food safety and incident plan"),
    ("Technology", "Vendor, implementation cost, monthly fee, integrations, support SLA, access rights"),
    ("Financial", "Editable 36-60 month model, working capital, tax, depreciation, sensitivity analysis"),
    ("Impact", "Targets, consent policy, data collection, safeguarding, employee feedback"),
]
story += [data_table(["WORKSTREAM", "DOCUMENTS / ANSWERS REQUIRED"], dd, [43*mm, 121*mm])]
story += [Spacer(1, 8), P("Immediate next meeting agenda", "H2x"), bullet("Confirm commercial brand: Yeshua Cafe or Juang Coffee."), bullet("Confirm that Rp 10-15 billion is per flagship location, not the total program budget."), bullet("Confirm whether Pejaten and North Jakarta are sequential candidates or two simultaneous flagship openings."), bullet("Approve the 300-500 seat design brief, rollout horizon, and 20-branch stage gates."), bullet("Confirm founder capital contribution and investor instrument."), bullet("Commission large-site, menu-costing, workforce, and editable financial-model workstreams."), PageBreak()]

# 25 Sources & assumptions
story += section_header("APPENDIX", "Sources, definitions, and limitations", "Prepared from official public sources and current Juang Group concept materials.")
sources = [
    ("BPS Jakarta Selatan", "Kota Jakarta Selatan Dalam Angka 2025", "https://jakselkota.bps.go.id/id/publication/2025/02/28/c51f32498dcf950a81b7b394/kota-jakarta-selatan-dalam-angka-2025.html"),
    ("BPS Jakarta Utara", "Kota Jakarta Utara Dalam Angka 2025", "https://jakutkota.bps.go.id/id/publication/2025/02/28/0fe91e929bc66c17b6417dcf/jakarta-utara-municipality-in-figures-2025.html"),
    ("Government of Indonesia", "Law No. 8/2016 on Persons with Disabilities", "https://peraturan.bpk.go.id/Details/37251/uu-no-8-tahun-2016"),
    ("ILO", "Indonesia paves the way for inclusive employment services", "https://www.ilo.org/resource/news/indonesia-paves-way-inclusive-employment-services"),
    ("ILO", "Business as unusual: Making workplaces inclusive", "https://www.ilo.org/publications/business-unusual-making-workplaces-inclusive-people-disabilities"),
    ("OSS", "KBLI - Cafe and food service activity references", "https://oss.go.id/id/kbli"),
    ("BPJPH", "Mandatory halal certification information", "https://bpjph.halal.go.id/detail/tak-hanya-makanan-minuman-ini-jenis-produk-yang-wajib-bersertifikat-halal-mulai-18-oktober-2026/"),
]
story += [data_table(["SOURCE", "REFERENCE", "URL"], sources, [34*mm, 54*mm, 76*mm])]
story += [Spacer(1, 8), P("Limitations", "H2x"), P("The client has provided a target of 20 Jakarta branches, regional expansion, 300-500 seats per flagship pilot, and Rp 10-15 billion. This draft interprets Rp 10-15 billion as the startup range per flagship; that interpretation requires written confirmation. No site visits, lease quotations, customer interviews, supplier quotations, audited financial statements, tax review, legal review, disability professional assessment, or founder funding terms were available. Financial values are planning assumptions in Indonesian rupiah and should not be presented as guaranteed returns.", "Bodyx")]
story += [Spacer(1, 8), callout("NEXT DELIVERABLE", "After the due diligence inputs are collected, convert this plan into: (1) an editable 5-year financial model, (2) a 12-15 slide investor pitch deck, (3) a one-page investment teaser, and (4) a final business plan with signed-off assumptions."), PageBreak()]

# 26 Back cover
story += [Spacer(1, 45*mm), P("FROM A VISION,<br/>BUILT WITH DISCIPLINE.", "TitleBig"), Spacer(1, 8*mm),
          P("Yeshua Cafe is designed to create a commercially sustainable hospitality business and meaningful employment. The next step is not a bigger promise - it is better evidence.", "Bodyx"),
          Spacer(1, 55*mm), HRFlowable(width="100%", thickness=2, color=GOLD), Spacer(1, 6*mm),
          P("Prepared for Juang Group", "H2x"), P("Investor discussion draft  |  August 2026", "Smallx")]

doc.build(story, canvasmaker=NumberedCanvas)
print(OUT)
