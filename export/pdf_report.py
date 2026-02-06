from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
)
from reportlab.lib.pagesizes import LETTER
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER
from reportlab.lib import colors
from reportlab.lib.units import inch


def generate_pdf_report(analysis_data, output_path):
    """
    Generates a professional, readable PDF report for contract risk analysis.
    """

    doc = SimpleDocTemplate(
        output_path,
        pagesize=LETTER,
        rightMargin=50,
        leftMargin=50,
        topMargin=60,
        bottomMargin=50
    )

    styles = getSampleStyleSheet()
    story = []

    # -------------------------------------------------
    # CUSTOM STYLES
    # -------------------------------------------------
    title_style = ParagraphStyle(
        "TitleStyle",
        parent=styles["Title"],
        alignment=TA_CENTER,
        fontSize=20,
        spaceAfter=20
    )

    subtitle_style = ParagraphStyle(
        "SubtitleStyle",
        parent=styles["Normal"],
        alignment=TA_CENTER,
        fontSize=11,
        textColor=colors.grey,
        spaceAfter=30
    )

    section_style = ParagraphStyle(
        "SectionStyle",
        parent=styles["Heading2"],
        fontSize=14,
        spaceBefore=20,
        spaceAfter=10
    )

    normal_style = ParagraphStyle(
        "NormalStyle",
        parent=styles["Normal"],
        fontSize=10,
        leading=14,
        spaceAfter=8
    )

    risk_high = ParagraphStyle(
        "RiskHigh",
        parent=normal_style,
        textColor=colors.red
    )

    risk_medium = ParagraphStyle(
        "RiskMedium",
        parent=normal_style,
        textColor=colors.orange
    )

    # -------------------------------------------------
    # TITLE
    # -------------------------------------------------
    story.append(Paragraph("CARA-Bot Contract Analysis Report", title_style))
    story.append(Paragraph(
        "AI-assisted risk assessment for small and medium businesses",
        subtitle_style
    ))

    # -------------------------------------------------
    # CONTRACT SUMMARY
    # -------------------------------------------------
    story.append(Paragraph("Contract Overview", section_style))

    overview_table = Table([
        ["Contract Type", analysis_data.get("contract_type", "Unknown")],
        ["Confidence Score", f"{analysis_data.get('confidence', 0.0) * 100:.1f}%"],
        ["Total Risks Found", str(len(analysis_data.get("risks", [])))]
    ], colWidths=[2.5 * inch, 3.5 * inch])

    overview_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.whitesmoke),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
        ("FONT", (0, 0), (-1, -1), "Helvetica", 10),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
        ("TOPPADDING", (0, 0), (-1, -1), 8)
    ]))

    story.append(overview_table)

    # -------------------------------------------------
    # RISKS SECTION
    # -------------------------------------------------
    story.append(Spacer(1, 20))
    story.append(Paragraph("Identified Risks", section_style))

    risks = analysis_data.get("risks", [])

    if not risks:
        story.append(Paragraph(
            "No high or medium risks were identified in this contract.",
            normal_style
        ))
    else:
        for idx, risk in enumerate(risks, start=1):

            severity = risk.get("severity", "Medium")
            style = risk_high if severity in ["High", "Critical"] else risk_medium

            story.append(Paragraph(
                f"<b>{idx}. {risk.get('risk_id', 'Risk')}</b> "
                f"({severity} Risk)",
                style
            ))

            story.append(Paragraph(
                f"<b>Reason:</b> {risk.get('reason', 'N/A')}",
                normal_style
            ))

            story.append(Paragraph(
                f"<b>Clause Context:</b><br/>{risk.get('clause_text', '')}",
                normal_style
            ))

            # Add LLM Explanation if available
            explanation = risk.get('explanation')
            if explanation:
                story.append(Spacer(1, 6))
                story.append(Paragraph("<b>AI Explanation:</b>", normal_style))
                story.append(Paragraph(
                    f"<i>{explanation.get('plain_explanation', '')}</i>", 
                    normal_style
                ))
                story.append(Spacer(1, 4))
                story.append(Paragraph(
                    f"<b>Suggestion:</b> {explanation.get('suggested_alternative', '')}", 
                    normal_style
                ))

            story.append(Spacer(1, 12))

    # -------------------------------------------------
    # FOOTER NOTE
    # -------------------------------------------------
    story.append(PageBreak())
    story.append(Paragraph("Disclaimer", section_style))
    story.append(Paragraph(
        "This report is generated by CARA-Bot using automated analysis. "
        "It is intended to assist business understanding and does not "
        "constitute legal advice. Please consult a qualified legal "
        "professional before making contractual decisions.",
        normal_style
    ))

    doc.build(story)
