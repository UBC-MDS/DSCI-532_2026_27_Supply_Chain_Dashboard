# Adapted from code/lecture02/core/app-01-ui.py

from shiny import App, ui

# UI
app_ui = ui.page_fillable(
    ui.panel_title("Supply Chain Dashboard"),
    ui.layout_sidebar(
        ui.sidebar("sidebar inputs", open="desktop"),
        
        ui.layout_columns(
            ui.card(ui.card_header("Map of route coverage across India"), full_screen=True),
            ui.card(ui.card_header("Defect rate per sku"), full_screen=True),
            col_widths=[6, 6],
        ),

        ui.layout_columns(
            ui.card(ui.card_header("Customer demographic breakdown"), full_screen=True),
            ui.card(ui.card_header("Product type availability breakdown"), full_screen=True),
            ui.card(ui.card_header("Best sellers"), full_screen=True),
            col_widths=[3, 3, 6],
        ),

        ui.layout_columns(
            ui.card(ui.card_header("Cost per unit"), full_screen=True),
            ui.card(ui.card_header("Overall inspection pass rate"), full_screen=True),
            ui.card(
                ui.card_header("Filters"),
                ui.p("Filter for product category"),
                ui.p("Filter for supplier"),
            ),
            col_widths=[3, 3, 6],
        ),
    ),
)


# Server
def server(input, output, session):
    pass


# Create app
app = App(app_ui, server)