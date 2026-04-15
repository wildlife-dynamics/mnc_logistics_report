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
    p("Balloon landings, airstrip operations, airstrip maintenance, and airline complaints reporting", SUBTITLE),
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
    p("The <b>mnc_logistics_report</b> workflow fetches events from "
      "EarthRanger for a specified time window — specifically "
      "<b>balloon_landing</b>, <b>airstrip_operations</b>, "
      "<b>airstrip_maintenance</b>, and <b>airline_complaint</b> event types — "
      "and routes them into four independent logistics reporting branches. "
      "Each branch processes and flattens event details, cleans and renames "
      "fields, and persists its data as a CSV table."),
    sp(4),
    p("The workflow delivers:"),
    bullet("<b>balloon_landing_summary_table.csv</b> — passenger records per "
           "balloon company and lodge"),
    bullet("<b>airstrip_operations_summary_table.csv</b> — total client counts "
           "pivoted by camp/lodge and direction (arrival / departure)"),
    bullet("<b>airstrip_maintenance_summary_table.csv</b> — dated log of airstrip "
           "maintenance activity types"),
    sp(6),
    h2("Output summary"),
    make_table(
        [
            ["Output file", "Source event type", "Description"],
            ["balloon_landing_summary_table.csv",
             "balloon_landing",
             "Passenger records: date, balloon company, lodge, number of passengers"],
            ["airstrip_operations_summary_table.csv",
             "airstrip_operations",
             "Pivoted summary: camp/lodge × arrival/departure, total clients"],
            ["airstrip_maintenance_summary_table.csv",
             "airstrip_maintenance",
             "Dated activity log: date, maintenance type"],
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
            ["ecoscope-workflows-core",        "0.22.18.*", "ecoscope-workflows"],
            ["ecoscope-workflows-ext-ecoscope","0.22.18.*", "ecoscope-workflows"],
            ["ecoscope-workflows-ext-custom",  "0.0.43.*",  "ecoscope-workflows-custom"],
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
             "Fetch event records (balloon_landing, airstrip_operations, "
             "airstrip_maintenance, airline_complaint) for the analysis time range. "
             "The client is also passed to each process_events_details call to "
             "resolve display titles for event detail fields."],
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
    p("All four reporting branches share a common ingestion pipeline that "
      "fetches, date-stamps, and temporally indexes events before branching."),
    sp(6),
    h2("3.1  Event retrieval"),
    make_table(
        [
            ["Parameter", "Value"],
            ["Task",             "get_events"],
            ["event_types",      "balloon_landing, airstrip_operations, "
                                 "airstrip_maintenance, airline_complaint"],
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
    note("Only the four event types required by this workflow are fetched at "
         "retrieval time. Downstream filter_df steps then isolate each type "
         "into its own branch."),
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
             "four branches."],
        ],
        [1.2*cm, 4.5*cm, W - 5.7*cm],
    ),
    sp(6),
    h2("3.3  Common branch pattern"),
    p("Every branch follows the same four-step normalisation pattern before "
      "any branch-specific transformations:"),
    make_table(
        [
            ["Step", "Task", "Detail"],
            ["1", "filter_df",
             "Filter events_temporal by event_type (op: equal, reset_index: false)."],
            ["2", "process_events_details",
             "Resolve event detail field IDs to their display titles "
             "(map_to_titles: true, ordered: true). "
             "Requires the EarthRanger client to look up schema definitions."],
            ["3", "normalize_json_column",
             "Flatten the <b>event_details</b> JSON column into individual columns "
             "(skip_if_not_exists: true, sort_columns: true)."],
            ["4", "drop_column_prefix",
             "Remove the <b>event_details__</b> prefix from all flattened columns "
             "(duplicate_strategy: keep_original)."],
        ],
        [1.2*cm, 4.5*cm, W - 5.7*cm],
    ),
    note("Because map_to_titles is true, flattened column names reflect "
         "human-readable field titles (e.g. 'Balloon Company', 'Camp/Lodge') "
         "rather than raw field keys. map_columns steps reference these titles "
         "directly."),
    PageBreak(),
]

# ══════════════════════════════════════════════════════════════════════════════
# 4. BRANCH 1 — BALLOON LANDINGS
# ══════════════════════════════════════════════════════════════════════════════
story += [
    h1("4. Branch 1 — Balloon Landings"),
    hr(),
    p("Filters <b>balloon_landing</b> events and produces a passenger "
      "summary table grouped by balloon company and lodge."),
    sp(6),
    h2("4.1  Normalisation"),
    p("Steps 1–4 follow the common branch pattern described in Section 3.3."),
    sp(6),
    h2("4.2  Column selection and renaming"),
    p("Task: <b>map_columns</b> (raise_if_not_found: false). "
      "Only the following columns are retained after prefix removal:"),
    make_table(
        [
            ["Source column (title after prefix drop)", "Renamed to"],
            ["date",                        "date (retained, not renamed)"],
            ["Balloon Company",             "balloon_company"],
            ["Where are clients staying?",  "where_are_clients_staying"],
            ["# of passengers",             "no_of_passengers"],
        ],
        [7*cm, W - 7*cm],
    ),
    note("All other columns are discarded at this step. "
         "raise_if_not_found: false means the task skips gracefully if any "
         "of the named columns are absent."),
    sp(6),
    h2("4.3  Cleaning and persistence"),
    make_table(
        [
            ["Step", "Task", "Detail"],
            ["1", "remove_brackets_from_column",
             "Strip bracket characters from <b>balloon_company</b> and "
             "<b>where_are_clients_staying</b> columns."],
            ["2", "persist_df",
             "Save as <b>balloon_landing_summary_table.csv</b> (filetype: csv)."],
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
    h2("5.1  Normalisation"),
    p("Steps 1–4 follow the common branch pattern described in Section 3.3."),
    sp(6),
    h2("5.2  Column renaming"),
    p("Task: <b>map_columns</b> (raise_if_not_found: false, retain_columns: []). "
      "No columns are dropped; all are retained with the following renames:"),
    make_table(
        [
            ["Source column (title after prefix drop)", "Renamed to"],
            ["Airline",             "airline"],
            ["Arrival or departure","arrival_departure"],
            ["Attendant",           "attendant"],
            ["Camp/Lodge",          "camp_lodge"],
            ["Number of clients",   "no_of_clients"],
        ],
        [7*cm, W - 7*cm],
    ),
    sp(6),
    h2("5.3  Cleaning"),
    make_table(
        [
            ["Step", "Task", "Detail"],
            ["1", "remove_brackets_from_column",
             "Strip bracket characters from <b>airline</b>, <b>arrival_departure</b>, "
             "<b>attendant</b>, and <b>camp_lodge</b>."],
            ["2", "replace_missing_with_label",
             "Replace null values in <b>camp_lodge</b> with the label <b>'other'</b>."],
            ["3", "convert_to_int",
             "Cast <b>no_of_clients</b> to integer "
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
             "Group by <b>[camp_lodge, arrival_departure]</b> and compute "
             "<b>sum(no_of_clients)</b> (display_name: no_of_clients, "
             "decimal_places: 0). reset_index: true."],
            ["2", "pivot_df",
             "Pivot the summary table: index_col: <b>camp_lodge</b>, "
             "columns_col: <b>arrival_departure</b>, "
             "values_col: <b>no_of_clients</b>. reset_idx: true. "
             "Produces one column per direction value (arrival, departure)."],
            ["3", "convert_to_int",
             "Cast pivot columns <b>arrival</b> and <b>departure</b> to integer "
             "(errors: coerce, fill_value: 0, inplace: false)."],
            ["4", "persist_df",
             "Save as <b>airstrip_operations_summary_table.csv</b> (filetype: csv)."],
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
      "of maintenance activity types."),
    sp(6),
    h2("6.1  Normalisation"),
    p("Steps 1–4 follow the common branch pattern described in Section 3.3."),
    sp(6),
    h2("6.2  Column selection and renaming"),
    p("Task: <b>map_columns</b> (raise_if_not_found: false). "
      "Only the following columns are retained:"),
    make_table(
        [
            ["Source column (title after prefix drop)", "Renamed to"],
            ["date",             "date (retained, not renamed)"],
            ["Maintenance type", "maintenance_type"],
        ],
        [7*cm, W - 7*cm],
    ),
    note("All other event detail columns are discarded at this step."),
    sp(6),
    h2("6.3  Persistence"),
    make_table(
        [
            ["Step", "Task", "Detail"],
            ["1", "persist_df",
             "Save as <b>airstrip_maintenance_summary_table.csv</b> (filetype: csv)."],
        ],
        [1.2*cm, 4.5*cm, W - 5.7*cm],
    ),
    PageBreak(),
]

# ══════════════════════════════════════════════════════════════════════════════
# 7. BRANCH 4 — AIRLINE COMPLAINTS
# ══════════════════════════════════════════════════════════════════════════════
story += [
    h1("7. Branch 4 — Airline Complaints"),
    hr(),
    p("Filters <b>airline_complaint</b> events and normalises their event "
      "details using the same four-step common branch pattern."),
    sp(6),
    h2("7.1  Normalisation"),
    make_table(
        [
            ["Step", "Task", "Detail"],
            ["1", "filter_df",
             "Filter events_temporal to rows where <b>event_type == "
             "'airline_complaint'</b> (op: equal, reset_index: false)."],
            ["2", "process_events_details",
             "Resolve event detail field IDs to display titles "
             "(map_to_titles: true, ordered: true)."],
            ["3", "normalize_json_column",
             "Flatten the <b>event_details</b> JSON column "
             "(skip_if_not_exists: true, sort_columns: true)."],
            ["4", "drop_column_prefix",
             "Remove the <b>event_details__</b> prefix "
             "(duplicate_strategy: keep_original). "
             "This is the terminal step in the current spec for this branch."],
        ],
        [1.2*cm, 4.5*cm, W - 5.7*cm],
    ),
    note("The airline complaint branch currently ends at the drop_column_prefix "
         "step. Column selection, renaming, and persistence steps are not yet "
         "defined in the spec. All four steps in this branch carry explicit "
         "skipif conditions (any_is_empty_df, any_dependency_skipped), "
         "consistent with the rest of the workflow."),
    PageBreak(),
]

# ══════════════════════════════════════════════════════════════════════════════
# 8. OUTPUT FILES
# ══════════════════════════════════════════════════════════════════════════════
story += [
    h1("8. Output Files"),
    hr(),
    p("All outputs are written to <b>ECOSCOPE_WORKFLOWS_RESULTS</b>."),
    make_table(
        [
            ["File", "Branch", "Columns", "Description"],
            ["balloon_landing_summary_table.csv",
             "Balloon landings",
             "date, balloon_company, where_are_clients_staying, no_of_passengers",
             "Passenger records by balloon company and lodge"],
            ["airstrip_operations_summary_table.csv",
             "Airstrip operations",
             "camp_lodge, arrival, departure (pivoted)",
             "Total clients per camp/lodge pivoted by direction"],
            ["airstrip_maintenance_summary_table.csv",
             "Airstrip maintenance",
             "date, maintenance_type",
             "Dated log of airstrip maintenance activity types"],
        ],
        [5*cm, 3.5*cm, 4*cm, W - 12.5*cm],
    ),
    PageBreak(),
]

# ══════════════════════════════════════════════════════════════════════════════
# 9. WORKFLOW EXECUTION LOGIC
# ══════════════════════════════════════════════════════════════════════════════
story += [
    h1("9. Workflow Execution Logic"),
    hr(),
    h2("9.1  Per-task skip conditions"),
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
         "the four branches propagates skips independently. If balloon_landing "
         "events are absent, only that branch is skipped; the other branches "
         "continue normally."),
    sp(6),
    h2("9.2  Four independent branches"),
    p("After the shared ingestion pipeline produces <b>events_temporal</b>, "
      "the workflow splits into four fully independent branches. Each branch "
      "reads from events_temporal and produces its own output with no "
      "cross-branch dependencies:"),
    make_table(
        [
            ["Branch", "Filter value", "Output"],
            ["Balloon landings",    "balloon_landing",    "balloon_landing_summary_table.csv"],
            ["Airstrip operations", "airstrip_operations","airstrip_operations_summary_table.csv"],
            ["Airstrip maintenance","airstrip_maintenance","airstrip_maintenance_summary_table.csv"],
            ["Airline complaints",  "airline_complaint",  "(normalised; no persist step yet)"],
        ],
        [4*cm, 4*cm, W - 8*cm],
    ),
    sp(6),
    h2("9.3  No mapvalues or fan-out"),
    p("This workflow processes all records as a single batch. There is no "
      "<b>mapvalues</b>, <b>split_groups</b>, or <b>zip_groupbykey</b> — "
      "every task runs exactly once."),
    sp(6),
    h2("9.4  No chart or map generation"),
    p("This is a pure data-extraction and tabulation workflow. It produces "
      "no charts, maps, or HTML outputs — only CSV tables. "
      "There are no html_to_png conversions, draw_map calls, "
      "or Likert/pie/bar chart tasks."),
    sp(6),
    h2("9.5  Dashboard"),
    p("The workflow concludes with <b>gather_dashboard</b> which packages "
      "workflow details, time range, and groupers. The <b>widgets</b> list "
      "is empty — no single-value or map widgets are configured."),
    PageBreak(),
]

# ══════════════════════════════════════════════════════════════════════════════
# 10. SOFTWARE VERSIONS
# ══════════════════════════════════════════════════════════════════════════════
story += [
    h1("10. Software Versions"),
    hr(),
    make_table(
        [
            ["Package", "Version pinned in spec.yaml"],
            ["ecoscope-workflows-core",        "0.22.18.*"],
            ["ecoscope-workflows-ext-ecoscope","0.22.18.*"],
            ["ecoscope-workflows-ext-custom",  "0.0.43.*"],
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
