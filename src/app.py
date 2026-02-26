from shiny import App, ui, render, reactive
from shinywidgets import output_widget, render_altair
import pandas as pd
import altair as alt
from datetime import date
from faicons import icon_svg

# Load data globally
df = pd.read_csv("data/raw/supply_chain_data.csv")

# Colorblind-friendly palette (Okabe-Ito)
# Blue, Orange, Green, Pink, Yellow, Light Blue, Light Orange
CP = ["#0072B2", "#D55E00", "#009E73", "#CC79A7", "#F0E442", "#56B4E9", "#E69F00"]
BASELINE = {
    "cost": df["Manufacturing costs"].mean(),
    "pass_rate": (df["Inspection results"] == "Pass").mean() * 100,
}

def compare(current, baseline, higher_is_better=True):
    """
    Classify current vs baseline — five states:
      significantly above / slightly above / stable / slightly below / significantly below
    Thresholds:  change < 1%: stable, 1–5%: slight, > 5%: significant
    """
    # guard: can't compute a meaningful delta
    if baseline == 0 or pd.isna(current):
        return dict(icon="circle-minus", theme="secondary", badge="no data", label="no data")

    # percentage change relative to baseline; sign tells direction
    pct = (current - baseline) / abs(baseline) * 100

    # "good" depends on context: higher MPG is good, lower HP is good for efficiency
    is_good = (pct > 0) if higher_is_better else (pct < 0)
    abs_pct = abs(pct)

    # badge string shown below the value: e.g. "+5.6 (+24.3%) vs overall avg"
    sign = "+" if pct >= 0 else ""
    badge = f"{sign}{current - baseline:.1f} ({sign}{pct:.1f}%) vs overall avg"

    # under 1% change — treat as noise, no colour signal
    if abs_pct < 1:
        return dict(icon="arrow-right", theme="secondary", badge="≈ stable vs overall avg", label="stable")

    # direction: matching FA icon
    icon = "arrow-trend-up" if pct > 0 else "arrow-trend-down"

    # colour: good changes are green (success ≥5%, teal <5%),
    #         bad changes are red (danger ≥5%, warning <5%)
    theme = (
        "success" if (is_good and abs_pct >= 5) else
        "teal"    if is_good                    else
        "danger"  if abs_pct >= 5               else
        "warning"
    )

    quantifier = "significantly" if abs_pct >= 5 else "slightly"
    return dict(icon=icon, theme=theme, badge=badge,
                label=f"{quantifier} {'above' if pct > 0 else 'below'} avg")


def kpi_showcase(cmp):
    """FA icon sized for the value-box showcase panel — inherits theme colour."""
    # fill defaults to currentColor, so the icon matches the box's text colour
    # fill_opacity softens it slightly so it doesn't overpower the value
    return icon_svg(cmp["icon"], height="0.75em", fill_opacity="0.85")

def kpi_caption(cmp):
    """Delta badge + five-state label rendered below the value."""
    return ui.tags.div(
        # bold first line: absolute + relative delta, e.g. "+5.6 (+24.3%) vs overall avg"
        ui.HTML(f'<strong style="opacity:0.9">{cmp["badge"]}</strong>'),
    )

app_ui = ui.page_fillable(
    ui.panel_title("Supply Chain Dashboard"),
    ui.layout_sidebar(
        ui.sidebar(
            ui.h5("Global Filters"),
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
            open="desktop",
        ),
        ui.layout_columns(
            # QUADRANT 1: Heatmap (Route vs Mode)
            ui.card(
                ui.card_header("Shipping Cost Matrix (Route vs. Mode)"),
                output_widget("plot_route_heatmap"),
                full_screen=True,
            ),
            # QUADRANT 2: Faceted Bars (Cost vs Time)
            ui.card(
                ui.card_header("Cost vs. Time Tradeoff by Mode"),
                output_widget("plot_cost_time_faceted"),
                full_screen=True,
            ),
            # QUADRANT 3: Sub-Quadrants (2x2 Grid)
            ui.layout_columns(
                ui.card(
                    ui.card_header("Customer Demographics"),
                    output_widget("plot_customer_demo"),
                ),
                ui.card(
                    ui.card_header("Stock Availability"),
                    output_widget("plot_availability"),
                ),
                ui.output_ui("value_cost_unit"),
                ui.output_ui("value_pass_rate"),
                col_widths=[6, 6, 6, 6],
            ),
            # QUADRANT 4: Quality Analysis
            ui.card(
                ui.card_header("Defect Rates by SKU"),
                output_widget("plot_defect_sku"),
                full_screen=True,
            ),
            col_widths=[6, 6, 6, 6],
        ),
        ui.hr(),
        ui.layout_columns(
            ui.markdown(
                f"**Supply Chain Dashboard** - Managing costs, demographics, and quality control | "
                f"**Authors:** Rocco Lee, Gaurang Ahuja, Junli Liu, Amanpreet Binepal | "
                f"[Github](https://github.com/UBC-MDS/DSCI-532_2026_27_Supply_Chain_Dashboard) | "
                f"**Last Updated:** {date.today()}"
                ),
        ),
    ),
)


def server(input, output, session):

    @reactive.calc
    def filtered_data():
        df_copy = df.copy()
        if input.input_product_type() != "All":
            df_copy = df_copy[df_copy["Product type"] == input.input_product_type()]
        if input.input_supplier() != "All":
            df_copy = df_copy[df_copy["Supplier name"] == input.input_supplier()]
        df_copy = df_copy[
            df_copy["Transportation modes"].isin(input.input_transport_mode())
        ]
        return df_copy

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
            .properties(height=300, width="container")
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
            .properties(height=120, width="container")
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
            .properties(height=120, width="container")
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
            .properties(height=120, width="container")
        )

    # KPI
    @render.ui
    def value_cost_unit():
        val = filtered_data()["Manufacturing costs"].mean()
        cmp = compare(val, BASELINE["cost"], higher_is_better=False)
        return ui.value_box(
            "Avg. Cost per Unit", f"${val:.2f}", kpi_caption(cmp),
            showcase=kpi_showcase(cmp),
            showcase_layout="top right",
            theme=cmp["theme"],
        )

    @render.ui
    def value_pass_rate():
        val = (filtered_data()["Inspection results"] == "Pass").mean() * 100
        cmp = compare(val, BASELINE["pass_rate"], higher_is_better=True)
        return ui.value_box(
            "Inspection Pass Rate", f"{val:.1f}%", kpi_caption(cmp),
            showcase=kpi_showcase(cmp),
            showcase_layout="top right",
            theme=cmp["theme"],
        )

    # Defect Rate Scatter plot
    @render_altair
    def plot_defect_sku():
        return (
            alt.Chart(filtered_data())
            .mark_circle(size=80)
            .encode(
                x=alt.X("SKU:N", axis=alt.Axis(labels=False), title="SKUs"),
                y=alt.Y("Defect rates:Q", title="Defect Rate (%)"),
                color=alt.Color(
                    "Supplier name:N", scale=alt.Scale(range=CP), title="Supplier"
                ),
                tooltip=[
                    "SKU",
                    "Supplier name",
                    alt.Tooltip("Defect rates:Q", format=".2f"),
                ],
            )
            .properties(height=300, width="container")
        )


app = App(app_ui, server)
