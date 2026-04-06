"""
Generate the MNC Logistics Report Technical Guide as a PDF using ReportLab.
Run with: python3 generate_technical_guide.py
Output: mnc_logistics_report_technical_guide.pdf
"""

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    HRFlowable, PageBreak,
)
from datetime import date

OUTPUT_FILE = "mnc_logistics_report_technical_guide.pdf"

# ── Colour palette ─────────────────────────────────────────────────────────────
GREEN_DARK  = colors.HexColor("#115631")
GREEN_MID   = colors.HexColor("#2d6a4f")
AMBER       = colors.HexColor("#e7a553")
SLATE       = colors.HexColor("#3d3d3d")
LIGHT_GREY  = colors.HexColor("#f5f5f5")
MID_GREY    = colors.HexColor("#cccccc")
WHITE       = colors.white

# ── Styles ─────────────────────────────────────────────────────────────────────
styles = getSampleStyleSheet()

def _style(name, parent="Normal", **kw):
    s = ParagraphStyle(name, parent=styles[parent], **kw)
    styles.add(s)
    return s

TITLE    = _style("DocTitle",    fontSize=26, leading=32, textColor=GREEN_DARK,
                  spaceAfter=6,  alignment=TA_CENTER, fontName="Helvetica-Bold")
SUBTITLE = _style("DocSubtitle", fontSize=13, leading=18, textColor=SLATE,
                  spaceAfter=4,  alignment=TA_CENTER)
META     = _style("Meta",        fontSize=9,  leading=13, textColor=colors.grey,
                  alignment=TA_CENTER, spaceAfter=2)
H1       = _style("H1", fontSize=15, leading=20, textColor=GREEN_DARK,
                  spaceBefore=18, spaceAfter=6, fontName="Helvetica-Bold")
H2       = _style("H2", fontSize=12, leading=16, textColor=GREEN_MID,
                  spaceBefore=12, spaceAfter=4, fontName="Helvetica-Bold")
H3       = _style("H3", fontSize=10, leading=14, textColor=SLATE,
                  spaceBefore=8,  spaceAfter=3, fontName="Helvetica-Bold")
BODY     = _style("Body", fontSize=9, leading=14, textColor=SLATE,
                  spaceAfter=6, alignment=TA_JUSTIFY)
BULLET   = _style("BulletItem", fontSize=9, leading=14, textColor=SLATE,
                  spaceAfter=3, leftIndent=14, firstLineIndent=-10, bulletIndent=4)
CODE     = _style("InlineCode", fontSize=8, leading=12, fontName="Courier",
                  backColor=LIGHT_GREY, textColor=colors.HexColor("#c0392b"),
                  spaceAfter=4, leftIndent=10, rightIndent=10, borderPad=3)
NOTE     = _style("Note", fontSize=8.5, leading=13,
                  textColor=colors.HexColor("#555555"),
                  backColor=colors.HexColor("#fff8e1"),
                  leftIndent=10, rightIndent=10, spaceAfter=6, borderPad=4)


def hr():                return HRFlowable(width="100%", thickness=1, color=MID_GREY, spaceAfter=6)
def p(text, style=BODY): return Paragraph(text, style)
def h1(text):            return Paragraph(text, H1)
def h2(text):            return Paragraph(text, H2)
def h3(text):            return Paragraph(text, H3)
def sp(n=6):             return Spacer(1, n)
def bullet(text):        return Paragraph(f"• {text}", BULLET)
def note(text):          return Paragraph(f"<b>Note:</b> {text}", NOTE)

def c(text):
    return Paragraph(str(text), BODY)

def make_table(data, col_widths, header_row=True):
    wrapped = [[c(cell) if isinstance(cell, str) else cell for cell in row]
               for row in data]
    t = Table(wrapped, colWidths=col_widths, repeatRows=1 if header_row else 0)
    t.setStyle(TableStyle([
        ("BACKGROUND",    (0, 0), (-1, 0 if header_row else -1), GREEN_DARK),
        ("TEXTCOLOR",     (0, 0), (-1, 0 if header_row else -1), WHITE),
        ("FONTNAME",      (0, 0), (-1, 0 if header_row else -1), "Helvetica-Bold"),
        ("FONTSIZE",      (0, 0), (-1, -1), 8),
        ("ROWBACKGROUNDS",(0, 1), (-1, -1), [WHITE, LIGHT_GREY]),
        ("GRID",          (0, 0), (-1, -1), 0.4, MID_GREY),
        ("VALIGN",        (0, 0), (-1, -1), "TOP"),
        ("TOPPADDING",    (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ("LEFTPADDING",   (0, 0), (-1, -1), 5),
        ("RIGHTPADDING",  (0, 0), (-1, -1), 5),
    ]))
    return t


def on_page(canvas, doc):
    canvas.saveState()
    canvas.setFont("Helvetica", 8)
    canvas.setFillColor(colors.grey)
    canvas.drawCentredString(A4[0] / 2, 1.5 * cm,
                             f"MNC Logistics Report — Technical Guide  |  Page {doc.page}")
    canvas.restoreState()


# ── Document ───────────────────────────────────────────────────────────────────
doc = SimpleDocTemplate(
    OUTPUT_FILE,
    pagesize=A4,
    leftMargin=2*cm, rightMargin=2*cm,
    topMargin=2.5*cm, bottomMargin=2.5*cm,
)

W = A4[0] - 4*cm   # usable width

story = []

# ══════════════════════════════════════════════════════════════════════════════
# COVER
# ══════════════════════════════════════════════════════════════════════════════
story += [
    sp(60),
    p("MNC Logistics Report", TITLE),
    p("Technical Guide", SUBTITLE),
    sp(4),
    p("Balloon landings, airstrip operations, and airstrip maintenance reporting", SUBTITLE),
    sp(4),
    p(f"Generated {date.today().strftime('%B %d, %Y')}", META),
    p("Workflow id: <b>mnc_logistics_report</b>", META),
    PageBreak(),
]

# ══════════════════════════════════════════════════════════════════════════════
# 1. OVERVIEW
# ══════════════════════════════════════════════════════════════════════════════
story += [
    h1("1. Overview"),
    hr(),
    p("The <b>mnc_logistics_report</b> workflow fetches all events from "
      "EarthRanger for a specified time window and routes them into three "
      "independent logistics reporting branches: balloon landings, airstrip "
      "operations (arrivals and departures), and airstrip maintenance. "
      "Each branch cleans, transforms, summarises, and persists its data "
      "as a CSV table."),
    sp(4),
    p("The workflow delivers:"),
    bullet("<b>balloon_landing_by_date.csv</b> — daily passenger counts per "
           "balloon company and lodge"),
    bullet("<b>airstrip_arrivals_and_departure.csv</b> — total client counts "
           "pivoted by camp/lodge and direction (arrival / departure)"),
    bullet("<b>airstrip_maintenance_table.csv</b> — dated log of airstrip "
           "maintenance activities"),
    sp(6),
    h2("Output summary"),
    make_table(
        [
            ["Output file", "Source event type", "Description"],
            ["balloon_landing_by_date.csv",
             "balloon_landing",
             "Daily summary: date, balloon company, lodge, total passengers"],
            ["airstrip_arrivals_and_departure.csv",
             "airstrip_operations",
             "Pivoted summary: camp/lodge × arrival/departure, total clients"],
            ["airstrip_maintenance_table.csv",
             "airstrip_maintenance",
             "Dated activity log: date, maintenance activity type"],
        ],
        [5.5*cm, 4*cm, W - 9.5*cm],
    ),
    PageBreak(),
]

# ══════════════════════════════════════════════════════════════════════════════
# 2. DEPENDENCIES
# ══════════════════════════════════════════════════════════════════════════════
story += [
    h1("2. Dependencies"),
    hr(),
    h2("2.1  Python packages"),
    make_table(
        [
            ["Package", "Version", "Channel"],
            ["ecoscope-workflows-core",        "0.22.17.*", "ecoscope-workflows"],
            ["ecoscope-workflows-ext-ecoscope","0.22.17.*", "ecoscope-workflows"],
            ["ecoscope-workflows-ext-custom",  "0.0.39.*",  "ecoscope-workflows-custom"],
            ["ecoscope-workflows-ext-ste",     "0.0.18.*",  "ecoscope-workflows-custom"],
            ["ecoscope-workflows-ext-mnc",     "0.0.8.*",   "ecoscope-workflows-custom"],
        ],
        [6.5*cm, 3*cm, W - 9.5*cm],
    ),
    sp(6),
    h2("2.2  Connection"),
    make_table(
        [
            ["Connection", "Task", "Purpose"],
            ["EarthRanger", "set_er_connection",
             "Fetch all event records (balloon_landing, airstrip_operations, "
             "airstrip_maintenance) for the analysis time range"],
        ],
        [3.5*cm, 4*cm, W - 7.5*cm],
    ),
    note("This workflow does not require Google Earth Engine or any "
         "Dropbox file downloads."),
    sp(6),
    h2("2.3  Grouper"),
    p("The workflow uses an <b>empty grouper list</b> (groupers: []). "
      "All event records are processed as a single undivided dataset — "
      "no fan-out or per-group branching is applied to the data. "
      "The grouper is passed through to the dashboard only."),
    PageBreak(),
]

# ══════════════════════════════════════════════════════════════════════════════
# 3. EVENT INGESTION PIPELINE
# ══════════════════════════════════════════════════════════════════════════════
story += [
    h1("3. Event Ingestion Pipeline"),
    hr(),
    p("All three reporting branches share a common ingestion pipeline that "
      "fetches, date-stamps, and temporally indexes events before branching."),
    sp(6),
    h2("3.1  Event retrieval"),
    make_table(
        [
            ["Parameter", "Value"],
            ["Task",             "get_events"],
            ["event_types",      "[] — fetches all event types (no filter at retrieval)"],
            ["Columns retained", "id, time, event_type, event_category, reported_by, "
                                 "serial_number, geometry, created_at, event_details, patrols"],
            ["include_details",  "true"],
            ["raise_on_empty",   "true"],
            ["include_null_geometry",   "false"],
            ["include_updates",         "false"],
            ["include_related_events",  "false"],
            ["include_display_values",  "false"],
        ],
        [5*cm, W - 5*cm],
    ),
    note("Fetching all event types and filtering downstream (rather than "
         "specifying event_types at retrieval) allows a single API call to "
         "serve all three reporting branches."),
    sp(6),
    h2("3.2  Date extraction and temporal indexing"),
    make_table(
        [
            ["Step", "Task", "Detail"],
            ["1", "extract_column_as_type",
             "Extract the <b>time</b> column as <b>output_type: date</b> "
             "into a new column named <b>date</b>. This strips the time "
             "component for daily grouping downstream."],
            ["2", "add_temporal_index",
             "Add temporal index using <b>time_col: date</b>, "
             "groupers: [], cast_to_datetime: true, format: mixed. "
             "Produces the shared events_temporal DataFrame used by all "
             "three branches."],
        ],
        [1.2*cm, 4.5*cm, W - 5.7*cm],
    ),
    PageBreak(),
]

# ══════════════════════════════════════════════════════════════════════════════
# 4. BRANCH 1 — BALLOON LANDINGS
# ══════════════════════════════════════════════════════════════════════════════
story += [
    h1("4. Branch 1 — Balloon Landings"),
    hr(),
    p("Filters <b>balloon_landing</b> events and produces a daily passenger "
      "count summary grouped by balloon company and lodge."),
    sp(6),
    h2("4.1  Filtering and normalisation"),
    make_table(
        [
            ["Step", "Task", "Detail"],
            ["1", "filter_df",
             "Filter events_temporal to rows where <b>event_type == "
             "'balloon_landing'</b> (op: equal, reset_index: false)."],
            ["2", "normalize_json_column",
             "Flatten the <b>event_details</b> JSON column "
             "(skip_if_not_exists: true, sort_columns: true)."],
        ],
        [1.2*cm, 4.5*cm, W - 5.7*cm],
    ),
    sp(6),
    h2("4.2  Column renaming"),
    p("Task: <b>transform_columns</b>. The following fields are renamed "
      "(skip_missing_rename: true). The task requires these source columns "
      "to be present:"),
    make_table(
        [
            ["Source column (event_details__*)", "Renamed to"],
            ["event_details__of_passengers",           "no_of_passengers"],
            ["event_details__balloon_company",          "balloon_company"],
            ["event_details__where_are_clients_staying","lodge"],
            ["date",                                    "date (required, not renamed)"],
        ],
        [7*cm, W - 7*cm],
    ),
    sp(6),
    h2("4.3  Cleaning"),
    make_table(
        [
            ["Step", "Task", "Detail"],
            ["1", "remove_brackets_from_column",
             "Strip bracket characters from <b>lodge</b> and "
             "<b>balloon_company</b> columns."],
            ["2", "replace_missing_with_label",
             "Replace null values in <b>lodge</b> with the label <b>'other'</b>."],
            ["3", "convert_to_int",
             "Cast <b>no_of_passengers</b> to integer "
             "(errors: coerce, fill_value: 0, inplace: false)."],
        ],
        [1.2*cm, 4.5*cm, W - 5.7*cm],
    ),
    sp(6),
    h2("4.4  Summary and persistence"),
    make_table(
        [
            ["Step", "Task", "Detail"],
            ["1", "summarize_df",
             "Group by <b>[date, balloon_company, lodge]</b> and compute "
             "<b>sum(no_of_passengers)</b>. reset_index: true."],
            ["2", "capitalize_text",
             "Capitalise the <b>balloon_company</b> column (sentence case)."],
            ["3", "capitalize_text",
             "Capitalise the <b>lodge</b> column (sentence case)."],
            ["4", "persist_df",
             "Save as <b>balloon_landing_by_date.csv</b> "
             "(filetype: csv)."],
        ],
        [1.2*cm, 4.5*cm, W - 5.7*cm],
    ),
    PageBreak(),
]

# ══════════════════════════════════════════════════════════════════════════════
# 5. BRANCH 2 — AIRSTRIP OPERATIONS
# ══════════════════════════════════════════════════════════════════════════════
story += [
    h1("5. Branch 2 — Airstrip Operations"),
    hr(),
    p("Filters <b>airstrip_operations</b> events and produces a pivoted "
      "summary of total client counts by camp/lodge and direction "
      "(arrival or departure)."),
    sp(6),
    h2("5.1  Filtering and normalisation"),
    make_table(
        [
            ["Step", "Task", "Detail"],
            ["1", "filter_df",
             "Filter events_temporal to rows where <b>event_type == "
             "'airstrip_operations'</b> (op: equal, reset_index: false)."],
            ["2", "normalize_json_column",
             "Flatten the <b>event_details</b> JSON column "
             "(skip_if_not_exists: true, sort_columns: true)."],
        ],
        [1.2*cm, 4.5*cm, W - 5.7*cm],
    ),
    sp(6),
    h2("5.2  Column renaming"),
    p("Task: <b>map_columns</b> (raise_if_not_found: true). "
      "Seven fields are renamed:"),
    make_table(
        [
            ["Source column (event_details__*)", "Renamed to"],
            ["event_details__guide",              "guide"],
            ["event_details__airline",            "airline"],
            ["event_details__attendant",          "attendant"],
            ["event_details__camplodge",          "camp_lodge"],
            ["event_details__flight_number",      "flight_number"],
            ["event_details__number_of_clients",  "number_of_clients"],
            ["event_details__arrival_or_departure","arrival_or_departure"],
        ],
        [7*cm, W - 7*cm],
    ),
    sp(6),
    h2("5.3  Cleaning"),
    make_table(
        [
            ["Step", "Task", "Detail"],
            ["1", "remove_brackets_from_column",
             "Strip bracket characters from <b>airline</b>, <b>attendant</b>, "
             "<b>camp_lodge</b>, and <b>arrival_or_departure</b>."],
            ["2", "replace_missing_with_label",
             "Replace null values in <b>camp_lodge</b> with the label <b>'other'</b>."],
            ["3", "convert_to_int",
             "Cast <b>number_of_clients</b> to integer "
             "(errors: coerce, fill_value: 0, inplace: false)."],
            ["4", "capitalize_text",
             "Capitalise the <b>camp_lodge</b> column (sentence case)."],
        ],
        [1.2*cm, 4.5*cm, W - 5.7*cm],
    ),
    sp(6),
    h2("5.4  Summary, pivot, and persistence"),
    make_table(
        [
            ["Step", "Task", "Detail"],
            ["1", "summarize_df",
             "Group by <b>[camp_lodge, arrival_or_departure]</b> and compute "
             "<b>sum(number_of_clients)</b> displayed as <b>no_of_passengers</b> "
             "(decimal_places: 0). reset_index: true."],
            ["2", "pivot_df",
             "Pivot the summary table: index_col: <b>camp_lodge</b>, "
             "columns_col: <b>arrival_or_departure</b>, "
             "values_col: <b>no_of_passengers</b>. reset_idx: true. "
             "Produces one column per direction value "
             "(e.g. Arrival, Departure)."],
            ["3", "persist_df",
             "Save as <b>airstrip_arrivals_and_departure.csv</b> (filetype: csv)."],
        ],
        [1.2*cm, 4.5*cm, W - 5.7*cm],
    ),
    PageBreak(),
]

# ══════════════════════════════════════════════════════════════════════════════
# 6. BRANCH 3 — AIRSTRIP MAINTENANCE
# ══════════════════════════════════════════════════════════════════════════════
story += [
    h1("6. Branch 3 — Airstrip Maintenance"),
    hr(),
    p("Filters <b>airstrip_maintenance</b> events and produces a dated log "
      "of maintenance activities, retaining only the date and activity columns."),
    sp(6),
    h2("6.1  Filtering and normalisation"),
    make_table(
        [
            ["Step", "Task", "Detail"],
            ["1", "filter_df",
             "Filter events_temporal to rows where <b>event_type == "
             "'airstrip_maintenance'</b> (op: equal, reset_index: false)."],
            ["2", "normalize_json_column",
             "Flatten the <b>event_details</b> JSON column "
             "(skip_if_not_exists: true, sort_columns: true)."],
        ],
        [1.2*cm, 4.5*cm, W - 5.7*cm],
    ),
    sp(6),
    h2("6.2  Column renaming and filtering"),
    make_table(
        [
            ["Step", "Task", "Detail"],
            ["1", "transform_columns",
             "Rename <b>event_details__maintenance_type → activity</b> "
             "(skip_missing_rename: true, required_columns: "
             "[event_details__maintenance_type])."],
            ["2", "filter_columns",
             "Retain only two columns: <b>date</b> and <b>activity</b>. "
             "All other fields are discarded."],
        ],
        [1.2*cm, 4.5*cm, W - 5.7*cm],
    ),
    sp(6),
    h2("6.3  Capitalisation and persistence"),
    make_table(
        [
            ["Step", "Task", "Detail"],
            ["1", "capitalize_text",
             "Capitalise the <b>activity</b> column (sentence case)."],
            ["2", "persist_df",
             "Save as <b>airstrip_maintenance_table.csv</b> (filetype: csv)."],
        ],
        [1.2*cm, 4.5*cm, W - 5.7*cm],
    ),
    PageBreak(),
]

# ══════════════════════════════════════════════════════════════════════════════
# 7. OUTPUT FILES
# ══════════════════════════════════════════════════════════════════════════════
story += [
    h1("7. Output Files"),
    hr(),
    p("All outputs are written to <b>ECOSCOPE_WORKFLOWS_RESULTS</b>."),
    make_table(
        [
            ["File", "Branch", "Columns", "Description"],
            ["balloon_landing_by_date.csv",
             "Balloon landings",
             "date, balloon_company, lodge, no_of_passengers",
             "Daily passenger total per balloon company and lodge"],
            ["airstrip_arrivals_and_departure.csv",
             "Airstrip operations",
             "camp_lodge, Arrival, Departure (pivoted)",
             "Total clients per camp/lodge pivoted by direction"],
            ["airstrip_maintenance_table.csv",
             "Airstrip maintenance",
             "date, activity",
             "Dated log of airstrip maintenance activity types"],
        ],
        [5*cm, 3.5*cm, 4*cm, W - 12.5*cm],
    ),
    PageBreak(),
]

# ══════════════════════════════════════════════════════════════════════════════
# 8. WORKFLOW EXECUTION LOGIC
# ══════════════════════════════════════════════════════════════════════════════
story += [
    h1("8. Workflow Execution Logic"),
    hr(),
    h2("8.1  Per-task skip conditions"),
    p("This workflow does <b>not</b> use a global <b>task-instance-defaults</b> "
      "block. Instead, every task from event retrieval onwards carries its own "
      "explicit skipif block:"),
    make_table(
        [
            ["Condition", "Behaviour"],
            ["any_is_empty_df",        "Skip this task if any input DataFrame is empty"],
            ["any_dependency_skipped", "Skip this task if any upstream dependency was skipped"],
        ],
        [5*cm, W - 5*cm],
    ),
    note("Because skip conditions are per-task rather than global, each of "
         "the three branches propagates skips independently. If balloon_landing "
         "events are absent, only that branch is skipped; the airstrip branches "
         "continue normally."),
    sp(6),
    h2("8.2  Three independent branches"),
    p("After the shared ingestion pipeline produces <b>events_temporal</b>, "
      "the workflow splits into three fully independent branches. Each branch "
      "reads from events_temporal and produces its own CSV output with no "
      "cross-branch dependencies:"),
    make_table(
        [
            ["Branch", "Filter value", "Output"],
            ["Balloon landings",   "balloon_landing",    "balloon_landing_by_date.csv"],
            ["Airstrip operations","airstrip_operations","airstrip_arrivals_and_departure.csv"],
            ["Airstrip maintenance","airstrip_maintenance","airstrip_maintenance_table.csv"],
        ],
        [4*cm, 4*cm, W - 8*cm],
    ),
    sp(6),
    h2("8.3  No mapvalues or fan-out"),
    p("This workflow processes all records as a single batch. There is no "
      "<b>mapvalues</b>, <b>split_groups</b>, or <b>zip_groupbykey</b> — "
      "every task runs exactly once."),
    sp(6),
    h2("8.4  No chart or map generation"),
    p("This is a pure data-extraction and tabulation workflow. It produces "
      "no charts, maps, or HTML outputs — only CSV tables. "
      "There are no html_to_png conversions, draw_map calls, "
      "or Likert/pie/bar chart tasks."),
    sp(6),
    h2("8.5  Dashboard"),
    p("The workflow concludes with <b>gather_dashboard</b> which packages "
      "workflow details, time range, and groupers. The <b>widgets</b> list "
      "is empty — no single-value or map widgets are configured."),
    PageBreak(),
]

# ══════════════════════════════════════════════════════════════════════════════
# 9. SOFTWARE VERSIONS
# ══════════════════════════════════════════════════════════════════════════════
story += [
    h1("9. Software Versions"),
    hr(),
    make_table(
        [
            ["Package", "Version pinned in spec.yaml"],
            ["ecoscope-workflows-core",        "0.22.17.*"],
            ["ecoscope-workflows-ext-ecoscope","0.22.17.*"],
            ["ecoscope-workflows-ext-custom",  "0.0.39.*"],
            ["ecoscope-workflows-ext-ste",     "0.0.18.*"],
            ["ecoscope-workflows-ext-mnc",     "0.0.8.*"],
        ],
        [7*cm, W - 7*cm],
    ),
]

# ══════════════════════════════════════════════════════════════════════════════
# BUILD
# ══════════════════════════════════════════════════════════════════════════════
doc.build(story, onFirstPage=on_page, onLaterPages=on_page)
print(f"PDF written → {OUTPUT_FILE}")
