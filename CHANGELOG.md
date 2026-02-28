# Changelog

All notable changes to the Supply Chain Dashboard project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [0.2.0] - 2026-02-28

### Added

- `reports/m2_spec.md` as per App specification requirements
- Data page with `DataTable` using tabs for organized data viewing
- `filters` toggle switch in Data tab to show/hide column filtering UI in the data table
- Footer to the Dashboard with GitHub link, Author names, and Last Updated date
- `requirements.txt` for Posit Cloud deployment
- Dev branch for staging and preview deployments
- CI/CD pipeline deploying to Posit Connect Cloud (stable on `main`, preview on `dev`)

### Changed

- Updated `reports/m2_spec.md` to reflect actual implementation:
  - Added Data tab components (filters toggle, download buttons) to Component Inventory
  - Enhanced Reactivity Diagram with separate sections for Dashboard and Data tabs
  - Expanded Calculation Details with detailed transformation logic and auxiliary components
  - Updated total component count from 12 to 15 components
  - Added component summary statistics and revision history
- Moved download buttons to Data page for better organization
- Repositioned KPIs to top of dashboard for improved visibility
- Updated `environment.yml` to include Altair and standardized package versions
- Revised Job Stories #3 and #4 in `m2_spec.md`:
  - Job Story #3: Shifted focus from "lead times and stock levels" to stock availability visualization
  - Job Story #4: Changed from "revenue and sales KPIs" to inspection pass rate and manufacturing cost per unit

### Fixed

- Fixed plot sizing issue to allow page scrolling instead of plot-specific scrolling
- Fixed sizing of UI cards for consistent layout
- Fixed Mode plot issue where plot didn't revert when reselecting all filters

### Known Issues

- Font size and formatting could be improved for better readability
- Reset filter button functionality not yet implemented (planned for future milestone)

### Reflection

**Job Stories Implementation Status:**
- **Job Story #1** (Cost Analysis): ✅ Fully implemented through transportation mode filters and shipping cost heatmap
- **Job Story #2** (Supplier Performance): ✅ Fully implemented with supplier dropdown and defect rate scatter plot
- **Job Story #3** (Inventory Planning): 🔄 Implemented with stock availability visualization (revised from original lead time focus)
- **Job Story #4** (Business Monitoring): 🔄 Implemented with KPI value boxes for cost per unit and inspection pass rate (revised from revenue/sales metrics)

**Layout and Design:**
- Successfully repositioned KPIs to top of dashboard, recognizing their importance as primary metrics
- Implemented multi-page layout (Dashboard and Data tabs) not originally sketched in M1, enhancing data exploration capabilities
- Added 15 components total (exceeding the 8-component minimum for a 4-person team), demonstrating comprehensive implementation

**Deviations from Original Plan:**
- Added Data tab with additional components (filters toggle, download buttons) during implementation to enhance user experience
- Job Stories #3 and #4 were revised to better align with available data and dashboard capabilities

**Strengths:**
- Hub-and-spoke reactivity architecture efficiently filters data once per user interaction
- Comprehensive component inventory with clear separation between core and auxiliary components
- Detailed specification documentation supporting future development in M3/M4

**Areas for Improvement:**
- Enhanced font formatting and sizing for better visual hierarchy
- Addition of reset filter button for improved user experience
- Further refinement of revised job stories in future milestones

---

## [0.0.1] - 2026-02-13

### Added

- Initial repository setup with standard directory structure
- Project proposal documentation in `reports/` directory
- Basic app skeleton in `src/app.py` with placeholder layout
- Environment configuration files (`environment.yml`)
- `README.md` with project description and setup instructions
- `CONTRIBUTING.md` with collaboration guidelines
- `.gitignore` configured for Python projects

### Notes

This release establishes the foundation for the Supply Chain Dashboard project, completing all Milestone 1 Phase 3 requirements.

---

## Release History

- [0.2.0] - Dashboard prototype with full functionality (Milestone 2)
- [0.0.1] - Initial project setup and skeleton app (Milestone 1)

---

_For detailed component specifications and architecture, see `reports/m2_spec.md`_
