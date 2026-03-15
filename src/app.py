from shiny import App, ui, render, reactive
from shiny.ui import Chat, chat_ui
from shinywidgets import output_widget, render_altair, reactive_read
import pandas as pd
import altair as alt
from datetime import date
from faicons import icon_svg
from dotenv import load_dotenv
import os
import sys
from pathlib import Path
import pathlib
import ibis
from ai_query_engine import SupplyChainAIEngine

# Add src directory to Python path
_project_root = Path(__file__).resolve().parent.parent
if str(_project_root) not in sys.path:
    sys.path.insert(0, str(_project_root))

from compare import compare

# Load environment variables
load_dotenv()

# Setup DuckDB connection via ibis
_app_dir = pathlib.Path(__file__).parent.parent
_parquet_path = str(_app_dir / "data" / "processed" / "supply_chain_data.parquet")
con = ibis.duckdb.connect()
supply_chain_table = con.read_parquet(_parquet_path, table_name="supply_chain")

# Load full data for baseline calculations and AI engine
df = supply_chain_table.to_pandas()

# Colorblind-friendly palette (Okabe-Ito)
# Blue, Orange, Green, Pink, Yellow, Light Blue, Light Orange
CP = ["#0072B2", "#D55E00", "#009E73", "#CC79A7", "#F0E442", "#56B4E9", "#E69F00"]
BASELINE = {
    "cost": df["Manufacturing costs"].mean(),
    "pass_rate": (df["Inspection results"] == "Pass").mean() * 100,
}


def kpi_showcase(cmp):
    """FA icon sized for the value-box showcase panel — inherits theme colour."""
    # fill defaults to currentColor, so the icon matches the box's text colour
    # fill_opacity softens it slightly so it doesn't overpower the value
    return icon_svg(cmp["icon"], height="1.5em", fill_opacity="0.85")


def kpi_caption(cmp):
    """Delta badge + five-state label rendered below the value."""
    return ui.tags.div(
        # bold first line: absolute + relative delta, e.g. "+5.6 (+24.3%) vs overall avg"
        ui.HTML(f'<strong style="opacity:0.9">{cmp["badge"]}</strong>'),
        # dimmer second line: human-readable state, e.g. "significantly above avg"
        ui.div(
            cmp.get("label", ""), style="opacity:0.7;font-size:0.8rem;margin-top:2px"
        ),
    )


app_ui = ui.page_fluid(
    # Custom CSS stylesheet
    ui.head_content(
        ui.tags.link(rel="stylesheet", href="apple-style.css"),
        ui.tags.style(
            """
            /* Force the page to fit the viewport with no scroll */
            html, body { height: 100vh; overflow: hidden; margin: 0; padding: 0; }
            .container-fluid { height: 100vh; overflow: hidden; padding: 0 12px; }

            /* Tighten card padding so charts get more room */
            .card-body { padding: 4px !important; }
            .card-header { padding: 4px 8px !important; font-size: 0.8rem; }

            /* Remove excess margin from value boxes */
            .value-box { min-height: 0 !important; }
            .value-box .value-box-grid { padding: 6px 10px !important; }

            /* Sidebar: tighter overall padding */
            .sidebar { padding: 10px 14px !important; font-size: 0.85rem; overflow: hidden !important; }
            .sidebar h5 { margin-bottom: 8px !important; font-size: 0.9rem; }

            /* All inputs: tighter gap between them */
            .sidebar .shiny-input-container { margin-bottom: 8px !important; }

            /* Labels: less bottom breathing room */
            label { font-size: 0.8rem !important; margin-bottom: 4px !important; }

            /* Checkbox group: kill the extra space after the last item */
            .shiny-input-checkboxgroup { margin-bottom: 0 !important; }
            .shiny-input-checkboxgroup .shiny-options-group { margin-bottom: 0 !important; }
            .shiny-input-checkboxgroup > label { margin-bottom: 18px !important; }

            /* HR: tight margins */
            .sidebar hr { margin: 6px 0 !important; border-color: rgba(0,0,0,0.15); border-top-width: 1px; opacity: 0.6; }

            /* Nav pills row */
            .nav-pills { margin-bottom: 4px !important; }
            .tab-content { overflow: hidden; }

            /* Layout sidebar — fix height so it doesn't overflow */
            .bslib-sidebar-layout {
                height: calc(100vh - 90px) !important;
                overflow: hidden;
            }
            .bslib-sidebar-layout > .main {
                overflow: hidden;
            }
            /* Sidebar section headings - bold + slightly larger */
            .sidebar h5,
            .sidebar label.control-label,
            .sidebar .shiny-input-container > label:first-child {
                font-weight: 700 !important;
                color: rgba(0,0,0,0.75) !important;
            }
            /* Remove the default padding at the top of the sidebar content */
            .bslib-sidebar-layout .sidebar-content {
                padding-top: 0 !important;
                display: flex;
                flex-direction: column;
            }
            """
        ),
        ui.HTML(
            """
            <div class="aurora-orb aurora-orb-1"></div>
            <div class="aurora-orb aurora-orb-2"></div>
            <div class="aurora-orb aurora-orb-3"></div>
        """
        ),
    ),
    ui.div(
        ui.panel_title("✨ Supply Chain Dashboard"),
        style="margin: 6px 0; line-height: 1;",
    ),
    ui.navset_pill(
        ui.nav_panel(
            "📊 Dashboard",
            ui.layout_sidebar(
                ui.sidebar(
                    ui.h5("🎛️ Global Filters"),
                    ui.input_select(
                        "input_product_type",
                        "Product Category",
                        ["All"] + sorted(df["Product type"].unique().tolist()),
                    ),
                    ui.input_checkbox_group(
                        "input_transport_mode",
                        "Transportation Mode",
                        sorted(df["Transportation modes"].unique().tolist()),
                        selected=df["Transportation modes"].unique().tolist(),
                    ),
                    ui.input_select(
                        "input_supplier",
                        "Supplier",
                        ["All"] + sorted(df["Supplier name"].unique().tolist()),
                    ),
                    ui.input_action_button(
                        "clear_all", "Reset Filters", class_="btn-primary btn-sm"
                    ),
                    ui.hr(),
                    ui.div(
                        ui.div(
                            "KPI LEGEND",
                            style="font-size:0.65rem; font-weight:700; letter-spacing:0.06em; color:rgba(0,0,0,0.5); margin-bottom:6px; text-transform:uppercase;",
                        ),
                        # Column headers
                        ui.div(
                            ui.div(
                                "slight (<5%)",
                                style="font-size:0.6rem; text-align:center; color:rgba(0,0,0,0.45);",
                            ),
                            ui.div(
                                "significant (≥5%)",
                                style="font-size:0.6rem; text-align:center; color:rgba(0,0,0,0.45);",
                            ),
                            style="display:grid; grid-template-columns:1fr 1fr; gap:4px; margin-bottom:2px;",
                        ),
                        # 2×2 grid
                        ui.div(
                            # Good + slight → teal
                            ui.div(
                                ui.HTML(
                                    '<svg width="11" height="11" viewBox="0 0 12 12"><path d="M2 9L6 3L10 9" fill="none" stroke="#003d29" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/></svg>'
                                ),
                                ui.span("Good, slight"),
                                style="display:flex; align-items:center; gap:5px; font-size:0.68rem; font-weight:500; padding:4px 6px; border-radius:5px; background:#02bf7f; color:#003d29;",
                            ),
                            # Good + significant → success
                            ui.div(
                                ui.HTML(
                                    '<svg width="11" height="11" viewBox="0 0 12 12"><path d="M2 9L6 3L10 9" fill="none" stroke="#e6f5e9" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/></svg>'
                                ),
                                ui.span("Good, signif."),
                                style="display:flex; align-items:center; gap:5px; font-size:0.68rem; font-weight:500; padding:4px 6px; border-radius:5px; background:#008919; color:#e6f5e9;",
                            ),
                            # Poor + slight → warning
                            ui.div(
                                ui.HTML(
                                    '<svg width="11" height="11" viewBox="0 0 12 12"><path d="M2 3L6 9L10 3" fill="none" stroke="#4a3300" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/></svg>'
                                ),
                                ui.span("Poor, slight"),
                                style="display:flex; align-items:center; gap:5px; font-size:0.68rem; font-weight:500; padding:4px 6px; border-radius:5px; background:#f9b927; color:#4a3300;",
                            ),
                            # Poor + significant → danger
                            ui.div(
                                ui.HTML(
                                    '<svg width="11" height="11" viewBox="0 0 12 12"><path d="M2 3L6 9L10 3" fill="none" stroke="#ffe8e8" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/></svg>'
                                ),
                                ui.span("Poor, signif."),
                                style="display:flex; align-items:center; gap:5px; font-size:0.68rem; font-weight:500; padding:4px 6px; border-radius:5px; background:#c10000; color:#ffe8e8;",
                            ),
                            style="display:grid; grid-template-columns:1fr 1fr; gap:4px; margin-bottom:6px;",
                        ),
                        # Divider
                        ui.hr(
                            style="margin:4px 0 !important; border-color:rgba(0,0,0,0.12);"
                        ),
                        # Stable row
                        ui.div(
                            ui.HTML(
                                '<svg width="11" height="11" viewBox="0 0 12 12"><path d="M2 6H10" stroke="#383d41" stroke-width="1.8" stroke-linecap="round"/></svg>'
                            ),
                            ui.span("Stable (<1% deviation)"),
                            style="display:flex; align-items:center; justify-content:center; gap:5px; font-size:0.68rem; font-weight:500; padding:4px 6px; border-radius:5px; background:#404040; color:#f0f0f0;",
                        ),
                        style="padding:6px 8px; background:rgba(255,255,255,0.4); border-radius:8px; border:0.5px solid rgba(0,0,0,0.1); margin:4px 0;",
                    ),
                    ui.hr(),
                    ui.div(
                        ui.markdown(
                            f"**✨ Supply Chain Dashboard** • Managing costs, demographics, and quality control\n\n"
                            f"👨‍💻 **Team:** Rocco Lee • Gaurang Ahuja • Junli Liu • Amanpreet Binepal\n\n"
                            f"🔗 [View on GitHub](https://github.com/UBC-MDS/DSCI-532_2026_27_Supply_Chain_Dashboard) • "
                            f"**Last Updated:** {date.today()}"
                        ),
                        style="text-align: center; opacity: 0.8; font-size: 12px;",
                    ),
                    open="desktop",
                    width=300,
                ),
                ui.layout_columns(
                    # LEFT COLUMN
                    ui.layout_columns(
                        # KPI row
                        ui.layout_columns(
                            ui.output_ui("value_cost_unit"),
                            ui.output_ui("value_pass_rate"),
                            col_widths=[6, 6],
                            style="height:70px;",
                        ),
                        # Defect scatter
                        ui.card(
                            ui.card_header("🔍 Defect Rates by SKU"),
                            output_widget("plot_defect_sku"),
                            full_screen=True,
                            style="height:270px;",
                        ),
                        # Customer demo + Availability
                        ui.layout_columns(
                            ui.card(
                                ui.card_header("👥 Customer Demographics"),
                                output_widget("plot_customer_demo"),
                                full_screen=True,
                                style="height:150px;",
                            ),
                            ui.card(
                                ui.card_header("📦 Stock Availability"),
                                output_widget("plot_availability"),
                                full_screen=True,
                                style="height:150px;",
                            ),
                            col_widths=[6, 6],
                        ),
                        col_widths=[12, 12, 12],
                    ),
                    # RIGHT COLUMN
                    ui.layout_columns(
                        ui.card(
                            ui.card_header("🌡️ Shipping Cost Matrix (Route vs. Mode)"),
                            output_widget("plot_route_heatmap"),
                            full_screen=True,
                            style="height:250px;",
                        ),
                        ui.card(
                            ui.card_header("⚖️ Cost vs. Time Tradeoff by Mode"),
                            output_widget("plot_cost_time_faceted"),
                            full_screen=True,
                            style="height:320px;",
                        ),
                        col_widths=[12, 12],
                    ),
                    col_widths=[6, 6],
                ),
            ),
        ),
        ui.nav_panel(
            "📋 Data",
            ui.layout_columns(
                ui.input_switch("filters", "Show filters", True),
                ui.download_button(
                    "download_all", "⬇ All Data", class_="btn-secondary"
                ),
                ui.download_button(
                    "download_view", "⬇ Filtered View", class_="btn-primary"
                ),
                col_widths=[3, 3, 3],
            ),
            ui.output_data_frame("table"),
        ),
        ui.nav_panel(
            "🤖 AI Explorer",
            ui.layout_sidebar(
                ui.sidebar(
                    ui.h5("💬 AI Assistant"),
                    ui.markdown(
                        "**✨ Ask questions in natural language!**\n\n"
                        "💡 Click a suggestion below to get started:"
                    ),
                    ui.hr(),
                    ui.markdown("**📊 Session Statistics**"),
                    ui.output_text_verbatim("query_stats"),
                    open="closed",
                    width=350,
                ),
                ui.layout_columns(
                    # Left column: AI Assistant
                    ui.card(
                        ui.card_header("💬 AI Assistant"),
                        chat_ui(id="ai_chat"),
                        ui.div(
                            ui.div(
                                ui.span("💡 Quick:", style="font-weight: 600; margin-right: 8px;"),
                                ui.input_action_button(
                                    "prompt_expensive",
                                    "Top 10 most expensive",
                                    class_="btn-sm btn-outline-primary",
                                    style="margin: 2px;",
                                ),
                                ui.input_action_button(
                                    "prompt_defects",
                                    "Defect rate > 3%",
                                    class_="btn-sm btn-outline-primary",
                                    style="margin: 2px;",
                                ),
                                ui.input_action_button(
                                    "prompt_routes",
                                    "Top 10 cheapest routes",
                                    class_="btn-sm btn-outline-primary",
                                    style="margin: 2px;",
                                ),
                                ui.input_action_button(
                                    "prompt_quality",
                                    "Low defect rate < 2%",
                                    class_="btn-sm btn-outline-primary",
                                    style="margin: 2px;",
                                ),
                                ui.input_action_button(
                                    "prompt_cost_filter",
                                    "Cost over $50",
                                    class_="btn-sm btn-outline-primary",
                                    style="margin: 2px;",
                                ),
                                ui.input_action_button(
                                    "prompt_skincare",
                                    "Skincare products",
                                    class_="btn-sm btn-outline-primary",
                                    style="margin: 2px;",
                                ),
                                style="display: flex; flex-wrap: wrap; gap: 2px; align-items: center;",
                            ),
                            style="padding: 6px 8px; background-color: #f8f9fa; border-radius: 5px; margin-bottom: 6px;",
                        ),
                        full_screen=True,
                        style="height:calc(100vh - 150px);",
                    ),
                    # Right column: stacked cards
                    ui.layout_columns(
                        ui.card(
                            ui.card_header("📋 Filtered Results"),
                            ui.output_data_frame("ai_filtered_table"),
                            full_screen=True,
                            style="height:calc((100vh - 150px) / 2 - 10px);",
                        ),
                        ui.layout_columns(
                            ui.card(
                                ui.card_header("📊 Defect Rate by Supplier"),
                                output_widget("ai_plot_defects"),
                                full_screen=True,
                                style="height:calc((100vh - 150px) / 2 - 10px);",
                            ),
                            ui.card(
                                ui.card_header("💰 Shipping Cost Distribution"),
                                output_widget("ai_plot_costs"),
                                full_screen=True,
                                style="height:calc((100vh - 150px) / 2 - 10px);",
                            ),
                            col_widths=[6, 6],
                        ),
                        col_widths=[12, 12],
                    ),
                    col_widths=[6, 6],
                ),
                ui.layout_columns(
                    ui.div(
                        ui.download_button(
                            "download_ai_filtered",
                            "⬇ Download Filtered Data (CSV)",
                            class_="btn-success btn-lg",
                            width="100%",
                        ),
                        style="text-align: center; padding-bottom: 20px;",
                    ),
                    col_widths=[12],
                ),
            ),
        ),
    ),
)


def server(input, output, session):

    # Initialize AI engine
    ai_engine = SupplyChainAIEngine()

    # Store for AI-filtered data
    ai_filtered_data_store = reactive.Value(df.copy())

    # Store pending SQL query awaiting confirmation
    pending_sql = reactive.Value(None)

    # Initialize Chat instance
    chat = Chat(id="ai_chat")

    # Add welcome message
    @reactive.effect
    async def _():
        await chat.append_message(
            "👋 Ask me to filter and analyze data. I'll generate SQL queries for your review first!"
        )

    @reactive.calc
    def filtered_data():
        query = supply_chain_table

        if input.input_product_type() != "All":
            query = query.filter(query["Product type"] == input.input_product_type())

        if input.input_supplier() != "All":
            query = query.filter(query["Supplier name"] == input.input_supplier())

        if input.input_transport_mode():
            query = query.filter(
                query["Transportation modes"].isin(input.input_transport_mode())
            )

        return query.to_pandas()

    @render.download(filename="supply_chain_all.csv")
    def download_all():
        yield df.to_csv(index=False)

    @render.download(filename="supply_chain_filtered.csv")
    def download_view():
        yield filtered_data().to_csv(index=False)

    @render.data_frame
    def table():
        return render.DataTable(
            filtered_data(),
            filters=input.filters(),
            height="400px",
            width="100%",
        )

    # Heatmap
    @render_altair
    def plot_route_heatmap():
        return (
            alt.Chart(filtered_data())
            .mark_rect()
            .encode(
                x=alt.X(
                    "Routes:N", title="Shipping Route", axis=alt.Axis(labelAngle=0)
                ),
                y=alt.Y("Transportation modes:N", title="Mode"),
                color=alt.Color(
                    "mean(Shipping costs):Q",
                    scale=alt.Scale(scheme="viridis"),
                    title="Avg Cost",
                ),
                tooltip=[
                    "Routes",
                    "Transportation modes",
                    alt.Tooltip("mean(Shipping costs):Q", format="$.2f"),
                ],
            )
            .properties(width="container")
        )

    # Faceted Bars
    @render_altair
    def plot_cost_time_faceted():
        summary = (
            filtered_data()
            .groupby("Transportation modes")[["Shipping costs", "Shipping times"]]
            .mean()
            .reset_index()
        )
        long_data = summary.melt(
            id_vars="Transportation modes", var_name="Metric", value_name="Value"
        )

        long_data["Metric"] = long_data["Metric"].replace(
            {"Shipping costs": "Avg Cost ($)", "Shipping times": "Avg Time (Days)"}
        )

        return (
            alt.Chart(long_data)
            .mark_bar()
            .encode(
                x=alt.X(
                    "Transportation modes:N", title=None, axis=alt.Axis(labelAngle=0)
                ),
                y=alt.Y("Value:Q", title=None),
                color=alt.Color(
                    "Metric:N", scale=alt.Scale(range=[CP[0], CP[1]]), legend=None
                ),
                row=alt.Row(
                    "Metric:N",
                    title=None,
                    header=alt.Header(labelFontSize=11, labelFontWeight="bold"),
                ),
                tooltip=[
                    "Transportation modes",
                    alt.Tooltip("Value:Q", format=".2f", title="Avg Value"),
                ],
            )
            .properties(width=600, height=170, padding={"bottom": 10})
            .resolve_scale(y="independent")
        )

    # Sub-quadrant charts
    @render_altair
    def plot_customer_demo():
        return (
            alt.Chart(filtered_data())
            .mark_bar()
            .encode(
                x=alt.X("count():Q", title="Total Customers"),
                y=alt.Y("Customer demographics:N", sort="-x", title=None),
                color=alt.value(CP[5]),
                tooltip=["Customer demographics", "count()"],
            )
            .properties(width="container")
        )

    @render_altair
    def plot_availability():
        return (
            alt.Chart(filtered_data())
            .mark_bar()
            .encode(
                x=alt.X("sum(Availability):Q", title="Units in Stock"),
                y=alt.Y("Product type:N", sort="-x", title=None),
                color=alt.value(CP[2]),
                tooltip=[
                    "Product type",
                    alt.Tooltip("sum(Availability):Q", title="Stock"),
                ],
            )
            .properties(width="container")
        )

    # KPI
    @render.ui
    def value_cost_unit():
        val = filtered_data()["Manufacturing costs"].mean()
        cmp = compare(val, BASELINE["cost"], higher_is_better=False)
        return ui.value_box(
            "Avg. Cost per Unit",
            f"${val:.2f}",
            kpi_caption(cmp),
            showcase=kpi_showcase(cmp),
            showcase_layout="left center",
            theme=cmp["theme"],
        )

    @render.ui
    def value_pass_rate():
        val = (filtered_data()["Inspection results"] == "Pass").mean() * 100
        cmp = compare(val, BASELINE["pass_rate"], higher_is_better=True)
        return ui.value_box(
            "Inspection Pass Rate",
            f"{val:.1f}%",
            kpi_caption(cmp),
            showcase=kpi_showcase(cmp),
            showcase_layout="left center",
            theme=cmp["theme"],
        )

    # Defect Rate Scatter plot
    @render_altair
    def plot_defect_sku():
        selection = alt.selection_point(
            name="point",
            fields=["Supplier name"],
            on="click",
            toggle=True,
            clear="dblclick",
        )
        return (
            alt.Chart(filtered_data())
            .mark_point(size=80, filled=True)
            .encode(
                x=alt.X("SKU:N", axis=alt.Axis(labels=False), title="SKUs"),
                y=alt.Y("Defect rates:Q", title="Defect Rate (%)"),
                color=alt.Color(
                    "Supplier name:N", scale=alt.Scale(range=CP), title="Supplier"
                ),
                shape=alt.Shape("Supplier name:N", title="Supplier"),
                opacity=alt.condition(selection, alt.value(1.0), alt.value(0.10)),
                tooltip=[
                    "SKU",
                    "Supplier name",
                    alt.Tooltip("Defect rates:Q", format=".2f"),
                ],
            )
            .add_params(selection)
            .properties(width="container", height=300)
        )

    @reactive.effect
    def update_supplier():
        pt = reactive_read(plot_defect_sku.widget.selections, "point")
        if pt and pt.value:
            ui.update_select("input_supplier", selected=pt.value[0]["Supplier name"])

    @reactive.effect
    def reset_button():
        input.clear_all()
        ui.update_select("input_supplier", selected="All")
        ui.update_select("input_product_type", selected="All")
        ui.update_checkbox_group(
            "input_transport_mode",
            selected=df["Transportation modes"].unique().tolist(),
        )

    # ==================== AI Explorer ====================

    suggested_prompts = {
        "prompt_expensive": "Show top 10 most expensive items by manufacturing cost",
        "prompt_defects": "Show products with defect rate greater than 3%",
        "prompt_routes": "Show top 10 cheapest shipping routes",
        "prompt_quality": "Show products with defect rate less than 2%",
        "prompt_cost_filter": "Show products with manufacturing cost over $50",
        "prompt_skincare": "Show all skincare products",
    }

    @reactive.effect
    @reactive.event(input.prompt_expensive)
    def handle_prompt_expensive():
        chat.update_user_input(value=suggested_prompts["prompt_expensive"])

    @reactive.effect
    @reactive.event(input.prompt_defects)
    def handle_prompt_defects():
        chat.update_user_input(value=suggested_prompts["prompt_defects"])

    @reactive.effect
    @reactive.event(input.prompt_routes)
    def handle_prompt_routes():
        chat.update_user_input(value=suggested_prompts["prompt_routes"])

    @reactive.effect
    @reactive.event(input.prompt_quality)
    def handle_prompt_quality():
        chat.update_user_input(value=suggested_prompts["prompt_quality"])

    @reactive.effect
    @reactive.event(input.prompt_cost_filter)
    def handle_prompt_cost_filter():
        chat.update_user_input(value=suggested_prompts["prompt_cost_filter"])

    @reactive.effect
    @reactive.event(input.prompt_skincare)
    def handle_prompt_skincare():
        chat.update_user_input(value=suggested_prompts["prompt_skincare"])

    @chat.on_user_submit
    async def handle_chat_input():
        """Handle user chat input with SQL confirmation flow"""
        user_messages = chat.messages()
        if not user_messages:
            return

        user_query = user_messages[-1]["content"]
        user_query_lower = user_query.strip().lower()

        # Check if user is confirming execution
        if user_query_lower in ['yes', 'confirm', 'execute', 'y', 'ok']:
            sql = pending_sql.get()
            if sql:
                try:
                    filtered = ai_engine.execute_sql(con, sql)
                    ai_filtered_data_store.set(filtered)

                    await chat.append_message(
                        f"✅ **SQL executed successfully!**\n\n"
                        f"📊 Found **{len(filtered)}** matching records (out of {len(df)} total)\n\n"
                        f"Data table and charts have been updated - check the results below!"
                    )

                    pending_sql.set(None)
                except Exception as e:
                    await chat.append_message(
                        f"❌ **SQL execution failed:**\n\n"
                        f"```\n{str(e)}\n```\n\n"
                        f"Please try a different query."
                    )
                    pending_sql.set(None)
            else:
                await chat.append_message(
                    "💡 No pending SQL query to execute. Please send a new query first."
                )
            return

        # Check if user is canceling
        if user_query_lower in ['no', 'cancel', 'abort', 'n']:
            if pending_sql.get():
                pending_sql.set(None)
                await chat.append_message(
                    "🚫 SQL query cancelled. You can send a new query anytime."
                )
            else:
                await chat.append_message(
                    "💡 No pending SQL query to cancel."
                )
            return

        # Generate new SQL query
        result = ai_engine.natural_language_to_sql(user_query, df)

        if result["success"] and result["sql_query"]:
            pending_sql.set(result["sql_query"])

            ai_response = (
                f"🔍 **{result['explanation']}**\n\n"
                f"**Generated SQL Query:**\n```sql\n{result['sql_query']}\n```\n\n"
                f"⚠️ **Please review the SQL query above.**\n\n"
                f"To execute this query, reply with:\n"
                f"• **'yes'** or **'confirm'** or **'execute'** to run the query\n"
                f"• **'no'** or **'cancel'** to abort"
            )
        else:
            ai_response = (
                f"💡 {result['error']}"
                if result["error"]
                else "💡 I can help you filter data! Try:\n"
                "• Use specific conditions (e.g., 'cost > 50')\n"
                "• Click the suggested prompts below"
            )

        await chat.append_message(ai_response)

    @render.data_frame
    def ai_filtered_table():
        """Display AI-filtered data"""
        return render.DataTable(
            ai_filtered_data_store.get(), height="100%", width="100%"
        )

    @render_altair
    def ai_plot_defects():
        """Chart 1: Average defect rate by supplier"""
        data = ai_filtered_data_store.get()

        if data.empty:
            return (
                alt.Chart(pd.DataFrame({"message": ["No data"]}))
                .mark_text(text="No data", size=20, color="gray")
                .properties(width="container", height=300)
            )

        return (
            alt.Chart(data)
            .mark_bar()
            .encode(
                x=alt.X(
                    "Supplier name:N", title="Supplier", axis=alt.Axis(labelAngle=-45)
                ),
                y=alt.Y("mean(Defect rates):Q", title="Avg Defect Rate (%)"),
                color=alt.Color(
                    "Supplier name:N", scale=alt.Scale(range=CP), legend=None
                ),
                tooltip=[
                    alt.Tooltip("Supplier name:N", title="Supplier"),
                    alt.Tooltip(
                        "mean(Defect rates):Q", format=".2f", title="Avg Defect Rate"
                    ),
                    alt.Tooltip("count():Q", title="Records"),
                ],
            )
            .properties(width="container", height=300)
        )

    @render_altair
    def ai_plot_costs():
        """Chart 2: Shipping cost distribution"""
        data = ai_filtered_data_store.get()

        if data.empty:
            return (
                alt.Chart(pd.DataFrame({"message": ["No data"]}))
                .mark_text(text="No data", size=20, color="gray")
                .properties(width="container", height=300)
            )

        return (
            alt.Chart(data)
            .mark_boxplot()
            .encode(
                x=alt.X(
                    "Transportation modes:N",
                    title="Transport Mode",
                    axis=alt.Axis(labelAngle=-45),
                ),
                y=alt.Y("Shipping costs:Q", title="Shipping Cost ($)"),
                color=alt.Color(
                    "Transportation modes:N", scale=alt.Scale(range=CP), legend=None
                ),
            )
            .properties(width="container", height=300)
        )

    @render.download(filename="ai_filtered_supply_chain.csv")
    def download_ai_filtered():
        """Download AI-filtered data"""
        yield ai_filtered_data_store.get().to_csv(index=False)

    @render.text
    def query_stats():
        """Display query statistics"""
        return (
            f"Queries used: {ai_engine.query_count}/{ai_engine.max_queries_per_session}\n"
            f"Records shown: {len(ai_filtered_data_store.get())}"
        )


app = App(app_ui, server)
