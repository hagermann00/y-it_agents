"""
WYATT MACHINE 2 (Y-IT Machine 2) [SIMULATION]
KDP PDF Assembler - Pagify + KDP-ify

Converts Markdown manuscripts with [IMAGE: ...] tags into 6x9 KDP-ready PDFs.
Images are simulated as gray placeholder boxes.
"""

import os
import re
from reportlab.lib.pagesizes import inch
from reportlab.lib.units import inch as INCH
from reportlab.pdfgen import canvas
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Image as RLImage
from reportlab.platypus.flowables import Flowable
from reportlab.lib.colors import gray, black

# KDP 6x9 SPECIFICATIONS
PAGE_WIDTH = 6 * INCH
PAGE_HEIGHT = 9 * INCH
MARGIN_TOP = 0.75 * INCH
MARGIN_BOTTOM = 0.75 * INCH
MARGIN_OUTSIDE = 0.5 * INCH
MARGIN_GUTTER = 0.75 * INCH

INPUT_FILE = r"c:\iiwii_db\y-it_agents\00_TURBO_PRODUCTION_RUN\dummy_manuscript.md"
OUTPUT_FILE = r"c:\iiwii_db\y-it_agents\00_TURBO_PRODUCTION_RUN\OUTPUT_SIMULATION.pdf"


class ImagePlaceholder(Flowable):
    """Gray box placeholder for [IMAGE: ...] tags."""
    def __init__(self, width, height, label=""):
        Flowable.__init__(self)
        self.width = width
        self.height = height
        self.label = label

    def draw(self):
        self.canv.setFillColor(gray)
        self.canv.rect(0, 0, self.width, self.height, fill=1, stroke=1)
        self.canv.setFillColor(black)
        self.canv.setFont("Helvetica", 8)
        self.canv.drawCentredString(self.width / 2, self.height / 2, self.label[:50])


def parse_markdown(md_content):
    """Parse markdown into flowable elements."""
    styles = getSampleStyleSheet()
    
    # Custom styles
    styles.add(ParagraphStyle(
        name='ChapterTitle',
        fontName='Helvetica-Bold',
        fontSize=18,
        spaceAfter=20,
        spaceBefore=40,
        leading=22
    ))
    styles.add(ParagraphStyle(
        name='SectionHeader',
        fontName='Helvetica-Bold',
        fontSize=14,
        spaceAfter=12,
        spaceBefore=20,
        leading=18
    ))
    styles.add(ParagraphStyle(
        name='YitBodyText',
        fontName='Times-Roman',
        fontSize=11,
        spaceAfter=8,
        leading=14,
        firstLineIndent=0
    ))
    styles.add(ParagraphStyle(
        name='YitBulletText',
        fontName='Times-Roman',
        fontSize=11,
        spaceAfter=4,
        leading=14,
        leftIndent=20,
        bulletIndent=10
    ))

    elements = []
    lines = md_content.split('\n')
    
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        
        # Skip empty lines
        if not line:
            i += 1
            continue
        
        # Chapter title (# )
        if line.startswith('# '):
            if elements:  # Page break before new chapter (except first)
                elements.append(PageBreak())
            title = line[2:].strip()
            elements.append(Paragraph(title, styles['ChapterTitle']))
            i += 1
            continue
        
        # Section header (## )
        if line.startswith('## '):
            header = line[3:].strip()
            elements.append(Paragraph(header, styles['SectionHeader']))
            i += 1
            continue
        
        # Image placeholder
        image_match = re.match(r'\[IMAGE:\s*(.+?)\]', line)
        if image_match:
            label = image_match.group(1)
            # 3.5" wide, 2" tall placeholder
            elements.append(Spacer(1, 10))
            elements.append(ImagePlaceholder(3.5 * INCH, 2 * INCH, f"[{label}]"))
            elements.append(Spacer(1, 10))
            i += 1
            continue
        
        # Bullet points
        if line.startswith('- '):
            bullet_text = line[2:].strip()
            # Handle bold markdown
            bullet_text = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', bullet_text)
            elements.append(Paragraph(f"• {bullet_text}", styles['YitBulletText']))
            i += 1
            continue
        
        # Horizontal rule
        if line.startswith('---'):
            elements.append(Spacer(1, 20))
            i += 1
            continue
        
        # Italic/emphasis line
        if line.startswith('*') and line.endswith('*') and not line.startswith('**'):
            text = line.strip('*')
            elements.append(Spacer(1, 10))
            elements.append(Paragraph(f"<i>{text}</i>", styles['YitBodyText']))
            i += 1
            continue
        
        # Regular paragraph - handle bold
        text = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', line)
        elements.append(Paragraph(text, styles['YitBodyText']))
        i += 1
    
    return elements


def build_pdf():
    """Build the KDP PDF from markdown."""
    print(f"[WYATT MACHINE 2] Starting PDF generation...")
    print(f"[WYATT MACHINE 2] Input: {INPUT_FILE}")
    print(f"[WYATT MACHINE 2] Output: {OUTPUT_FILE}")
    
    # Read markdown
    with open(INPUT_FILE, 'r', encoding='utf-8') as f:
        md_content = f.read()
    
    print(f"[WYATT MACHINE 2] Read {len(md_content)} characters from manuscript.")
    
    # Create document
    doc = SimpleDocTemplate(
        OUTPUT_FILE,
        pagesize=(PAGE_WIDTH, PAGE_HEIGHT),
        leftMargin=MARGIN_GUTTER,
        rightMargin=MARGIN_OUTSIDE,
        topMargin=MARGIN_TOP,
        bottomMargin=MARGIN_BOTTOM
    )
    
    # Parse and build
    elements = parse_markdown(md_content)
    print(f"[WYATT MACHINE 2] Generated {len(elements)} flowable elements.")
    
    doc.build(elements)
    
    # Verify output
    if os.path.exists(OUTPUT_FILE):
        size = os.path.getsize(OUTPUT_FILE)
        print(f"[WYATT MACHINE 2] SUCCESS! PDF created: {size} bytes")
        return True
    else:
        print(f"[WYATT MACHINE 2] FAILED! PDF not created.")
        return False


if __name__ == "__main__":
    build_pdf()
