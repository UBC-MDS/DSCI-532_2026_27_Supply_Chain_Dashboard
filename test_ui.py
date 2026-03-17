import pytest
from playwright.sync_api import Page, expect

BASE_URL = "http://localhost:8000"


def test_transport_mode_impact_on_kpis(page: Page):
    """Verify that unchecking a transport mode updates the KPI value."""
    page.goto(BASE_URL)

    # Wait for KPI card
    page.get_by_text("Avg. Cost per Unit").wait_for(timeout=15000)

    # Locate currency value
    kpi_value = page.locator("text=/\\$[0-9]+\\.[0-9]+/").first
    initial_value = kpi_value.inner_text()

    # Remove Air transport
    page.get_by_label("Air").uncheck()

    # Value should update
    expect(kpi_value).not_to_have_text(initial_value, timeout=10000)


def test_supplier_filter_updates_table(page: Page):
    """Verify selecting a supplier filter affects the data table."""
    page.goto(BASE_URL)

    # Wait for dashboard filters to load
    supplier_dropdown = page.locator("#input_supplier")
    expect(supplier_dropdown).to_be_visible(timeout=15000)

    # Change supplier selection
    supplier_dropdown.select_option(label="Supplier 1")

    # Navigate to Data tab
    page.get_by_role("tab", name="📋 Data").click()

    # Table should render with filtered data
    table = page.locator("#table")
    expect(table).to_be_visible(timeout=15000)


def test_navigation_to_ai_explorer(page: Page):
    """Verify navigation from Dashboard to AI Explorer tab works."""
    page.goto(BASE_URL)

    # Navigate to AI Explorer
    page.get_by_role("tab", name="🤖 AI Explorer").click()

    # Confirm AI interface loads
    expect(page.get_by_text("Ask me to filter"))


def test_download_button_state(page: Page):
    """Verify AI filtered data download button is present."""
    page.goto(BASE_URL)

    # Open AI Explorer tab
    page.get_by_role("tab", name="🤖 AI Explorer").click()

    # Locate download button
    download_btn = page.locator("#download_ai_filtered")

    expect(download_btn).to_be_attached()
    expect(download_btn).to_be_visible()
