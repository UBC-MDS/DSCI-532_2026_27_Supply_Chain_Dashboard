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
from compare import compare

# Add src directory to Python path
_current_dir = Path(__file__).parent
if str(_current_dir) not in sys.path:
    sys.path.insert(0, str(_current_dir))

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
        # Aurora background orbs
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
        style="margin-top: 15px; margin-bottom: 15px;",
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
                    ui.hr(),
                    ui.div(
                        ui.markdown(
                            f"**✨ Supply Chain Dashboard** • Managing costs, demographics, and quality control\n\n"
                            f"👨‍💻 **Team:** Rocco Lee • Gaurang Ahuja • Junli Liu • Amanpreet Binepal\n\n"
                            f"🔗 [View on GitHub](https://github.com/UBC-MDS/DSCI-532_2026_27_Supply_Chain_Dashboard) • "
                            f"**Last Updated:** {date.today()}"
                        ),
                        style="text-align: center; opacity: 0.8; font-size: 14px; margin-top: 250px;",
                    ),
                    open="desktop",
                ),
                ui.layout_columns(
                    ui.layout_columns(
                        ui.layout_columns(
                            ui.output_ui("value_cost_unit"),
                            ui.output_ui("value_pass_rate"),
                            col_widths=[6, 6],
                        ),
                        ui.card(
                            ui.card_header("🔍 Defect Rates by SKU"),
                            output_widget("plot_defect_sku"),
                            full_screen=True,
                        ),
                        ui.layout_columns(
                            ui.card(
                                ui.card_header("👥 Customer Demographics"),
                                output_widget("plot_customer_demo"),
                                full_screen=True,
                                height="200px",
                            ),
                            ui.card(
                                ui.card_header("📦 Stock Availability"),
                                output_widget("plot_availability"),
                                full_screen=True,
                                height="200px",
                            ),
                            col_widths=[6, 6],
                        ),
                        col_widths=[12, 12, 12],
                    ),
                    ui.layout_columns(
                        ui.card(
                            ui.card_header("🌡️ Shipping Cost Matrix (Route vs. Mode)"),
                            output_widget("plot_route_heatmap"),
                            full_screen=True,
                        ),
                        ui.card(
                            ui.card_header("⚖️ Cost vs. Time Tradeoff by Mode"),
                            output_widget("plot_cost_time_faceted"),
                            full_screen=True,
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
                        "💡 Try these examples:\n\n"
                        "• Show high defect rate products\n"
                        "• Find cheapest shipping routes\n"
                        "• Which supplier has best quality?\n"
                        "• Products with cost > $50"
                    ),
                    ui.hr(),
                    ui.markdown("**📊 Session Statistics**"),
                    ui.output_text_verbatim("query_stats"),
                    open="desktop",
                    width=350,
                ),
                ui.layout_columns(
                    ui.card(
                        ui.card_header("💬 AI Assistant"),
                        chat_ui(id="ai_chat"),
                        full_screen=True,
                        height="550px",
                    ),
                    ui.card(
                        ui.card_header("📋 Filtered Results"),
                        ui.output_data_frame("ai_filtered_table"),
                        full_screen=True,
                    ),
                    ui.card(
                        ui.card_header("📊 Defect Rate by Supplier"),
                        output_widget("ai_plot_defects"),
                        full_screen=True,
                    ),
                    ui.card(
                        ui.card_header("💰 Shipping Cost Distribution"),
                        output_widget("ai_plot_costs"),
                        full_screen=True,
                    ),
                    col_widths=[12, 12, 6, 6],
                ),
                ui.layout_columns(
                    ui.download_button(
                        "download_ai_filtered",
                        "⬇ Download Filtered Data (CSV)",
                        class_="btn-success btn-lg",
                        width="100%",
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

    # Initialize Chat instance
    chat = Chat(id="ai_chat")

    # Add welcome message
    @reactive.effect
    def _():
        chat.append_message(
            "👋 Hi! I can help you filter and analyze the supply chain data. Try asking:\n\n"
            "- 'Show products with defect rate > 3%'\n"
            "- 'Find cheapest shipping routes'\n"
            "- 'Which supplier has the best quality?'"
        )

    @reactive.calc
    def filtered_data():
        query = supply_chain_table

        if input.input_product_type() != "All":
            query = query.filter(query["Product type"] == input.input_product_type())

        if input.input_supplier() != "All":
            query = query.filter(query["Supplier name"] == input.input_supplier())

        if input.input_transport_mode():
            query = query.filter(query["Transportation modes"].isin(input.input_transport_mode()))

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
            .properties(width=850, height=170)
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
            name="point", fields=["Supplier name"], on="click"
        )
        return (
            alt.Chart(df)
            .mark_circle(size=80)
            .encode(
                x=alt.X("SKU:N", axis=alt.Axis(labels=False), title="SKUs"),
                y=alt.Y("Defect rates:Q", title="Defect Rate (%)"),
                color=alt.Color(
                    "Supplier name:N", scale=alt.Scale(range=CP), title="Supplier"
                ),
                opacity=alt.condition(selection, alt.value(1.0), alt.value(0.10)),
                tooltip=[
                    "SKU",
                    "Supplier name",
                    alt.Tooltip("Defect rates:Q", format=".2f"),
                ],
            )
            .add_params(selection)
            .properties(width="container", height=400)
        )

    @reactive.effect
    def update_supplier():
        pt = reactive_read(plot_defect_sku.widget.selections, "point")
        if pt and pt.value:
            ui.update_select("input_supplier", selected=pt.value[0]["Supplier name"])
        else:
            ui.update_select("input_supplier", selected="All")

    # ==================== AI Explorer ====================

    @chat.on_user_submit
    async def handle_chat_input():
        """Handle user chat input"""
        # Get user messages
        user_messages = chat.messages()
        if not user_messages:
            return

        # Get last user message
        user_query = user_messages[-1]["content"]

        # Call AI engine
        result = ai_engine.natural_language_to_filter(user_query, df)

        if result["success"] and result["filter_code"]:
            # Apply filter
            filtered = ai_engine.apply_filter(df, result["filter_code"])
            ai_filtered_data_store.set(filtered)

            # AI response
            ai_response = (
                f"✅ **{result['explanation']}**\n\n"
                f"📊 Found **{len(filtered)}** matching records (out of {len(df)} total)\n\n"
                f"Data table and charts have been updated - check the results below!"
            )
        else:
            ai_response = (
                f"❌ {result['error']}"
                if result["error"]
                else "Unable to process this query. Please try:\n"
                "- Use simpler language\n"
                "- Specify conditions explicitly (e.g., '>3' instead of 'very high')"
            )

        # Append AI response
        await chat.append_message(ai_response)

    @render.data_frame
    def ai_filtered_table():
        """Display AI-filtered data"""
        return render.DataTable(
            ai_filtered_data_store.get(), height="450px", width="100%"
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
