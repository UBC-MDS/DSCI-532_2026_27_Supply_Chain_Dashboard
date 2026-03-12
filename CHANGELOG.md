# Changelog

All notable changes to the Supply Chain Dashboard project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [0.4.0] - 2026-03-(TODO)

### Added

- `reports/m2_spec.md` as per App specification requirements. ([#25](https://github.com/UBC-MDS/DSCI-532_2026_27_Supply_Chain_Dashboard/issues/25))
- Changelog file ([#31](https://github.com/UBC-MDS/DSCI-532_2026_27_Supply_Chain_Dashboard/issues/31))
- `.gitignore` file
- `requirements.txt` file for Posit Cloud ([#24](https://github.com/UBC-MDS/DSCI-532_2026_27_Supply_Chain_Dashboard/issues/24))
- Footer to the Dashboard with GitHub link, Author names, and Last Updated date  ([#33](https://github.com/UBC-MDS/DSCI-532_2026_27_Supply_Chain_Dashboard/issues/33))
- Data page with `DataTable` using tabs for organized data viewing ([#36](https://github.com/UBC-MDS/DSCI-532_2026_27_Supply_Chain_Dashboard/issues/36))
- `filters` toggle switch in Data tab to show/hide column filtering UI in the data table
- Dev branch for staging and preview deployments
- CI/CD pipeline deploying to Posit Connect Cloud (stable on `main`, preview on `dev`)

### Changed

- Updated `reports/m2_spec.md` to reflect actual implementation:
  - Added Data tab components (filters toggle, download buttons) to Component Inventory
  - Enhanced Reactivity Diagram with separate sections for Dashboard and Data tabs
  - Expanded Calculation Details with detailed transformation logic and auxiliary components
  - Updated total component count from 12 to 15 components
  - Added component summary statistics and revision history
- Moved download buttons to Data page for better organization ([#36](https://github.com/UBC-MDS/DSCI-532_2026_27_Supply_Chain_Dashboard/issues/36))
- Repositioned KPIs to top of dashboard for improved visibility ([#29](https://github.com/UBC-MDS/DSCI-532_2026_27_Supply_Chain_Dashboard/issues/29))
- Updated `environment.yml` to include Altair and standardized package versions ([#32](https://github.com/UBC-MDS/DSCI-532_2026_27_Supply_Chain_Dashboard/issues/32))
- Move app dependencies to `requirements.txt` ([#24](https://github.com/UBC-MDS/DSCI-532_2026_27_Supply_Chain_Dashboard/issues/24))
- `README` instructions ([#24](https://github.com/UBC-MDS/DSCI-532_2026_27_Supply_Chain_Dashboard/issues/24))
- Revised Job Stories #3 and #4 in `m2_spec.md`:
  - Job Story #3: Shifted focus from "lead times and stock levels" to stock availability visualization
  - Job Story #4: Changed from "revenue and sales KPIs" to inspection pass rate and manufacturing cost per unit

### Fixed



### Known Issues



### Reflection

**Function extraction:**
- **`compare`**: The compare function handled the logic for the KPI indicators, showing what kind of changes the current selection had against the baseline.

**Unit tests:**
- The three tests cover various scenarios that the `compare` function could face

**UI tests:**
- The four tests cover different behaviours (Transport filter, Supplier filter, Navigation, and Download button)

**Challenge:**
- Figuring out what part of the `app.py` code to refactor/extract out
- Testing the asynchronous nature of the dashboard

**Strengths:**
- Unit tests check basic behaviour for business rules (success vs danger thresholds)
- UI tests perform integration testing and ensure the app runs as expected (reflected on the UI)

**Areas for Improvement:**
- Add more tests to increase code coverage (possibly include the use of some tools to track coverage)
- Integrate testing into a GitHub Actions workflow

---

## [0.3.0] - 2026-02-08

### Fixed

- Made KPI boxes smaller so it does not take as much space ([#51](https://github.com/UBC-MDS/DSCI-532_2026_27_Supply_Chain_Dashboard/issues/51))
- Changed layout; moved `Customer Demographic` and `Stock Availability` plots to the left side below the `Defect Rates by SKU` scatterplot ([#51](https://github.com/UBC-MDS/DSCI-532_2026_27_Supply_Chain_Dashboard/issues/51))
- Moved footer to the sidebar to make it so the dashboard page does not scroll anymore ([#51](https://github.com/UBC-MDS/DSCI-532_2026_27_Supply_Chain_Dashboard/issues/51))
- Added padding to title of dashboard to fix spacing ([#54](https://github.com/UBC-MDS/DSCI-532_2026_27_Supply_Chain_Dashboard/issues/54))

## [0.2.0] - 2026-02-28

### Added

- `reports/m2_spec.md` as per App specification requirements. ([#25](https://github.com/UBC-MDS/DSCI-532_2026_27_Supply_Chain_Dashboard/issues/25))
- Changelog file ([#31](https://github.com/UBC-MDS/DSCI-532_2026_27_Supply_Chain_Dashboard/issues/31))
- `.gitignore` file
- `requirements.txt` file for Posit Cloud ([#24](https://github.com/UBC-MDS/DSCI-532_2026_27_Supply_Chain_Dashboard/issues/24))
- Footer to the Dashboard with GitHub link, Author names, and Last Updated date  ([#33](https://github.com/UBC-MDS/DSCI-532_2026_27_Supply_Chain_Dashboard/issues/33))
- Data page with `DataTable` using tabs for organized data viewing ([#36](https://github.com/UBC-MDS/DSCI-532_2026_27_Supply_Chain_Dashboard/issues/36))
- `filters` toggle switch in Data tab to show/hide column filtering UI in the data table
- Dev branch for staging and preview deployments
- CI/CD pipeline deploying to Posit Connect Cloud (stable on `main`, preview on `dev`)

### Changed

- Updated `reports/m2_spec.md` to reflect actual implementation:
  - Added Data tab components (filters toggle, download buttons) to Component Inventory
  - Enhanced Reactivity Diagram with separate sections for Dashboard and Data tabs
  - Expanded Calculation Details with detailed transformation logic and auxiliary components
  - Updated total component count from 12 to 15 components
  - Added component summary statistics and revision history
- Moved download buttons to Data page for better organization ([#36](https://github.com/UBC-MDS/DSCI-532_2026_27_Supply_Chain_Dashboard/issues/36))
- Repositioned KPIs to top of dashboard for improved visibility ([#29](https://github.com/UBC-MDS/DSCI-532_2026_27_Supply_Chain_Dashboard/issues/29))
- Updated `environment.yml` to include Altair and standardized package versions ([#32](https://github.com/UBC-MDS/DSCI-532_2026_27_Supply_Chain_Dashboard/issues/32))
- Move app dependencies to `requirements.txt` ([#24](https://github.com/UBC-MDS/DSCI-532_2026_27_Supply_Chain_Dashboard/issues/24))
- `README` instructions ([#24](https://github.com/UBC-MDS/DSCI-532_2026_27_Supply_Chain_Dashboard/issues/24))
- Revised Job Stories #3 and #4 in `m2_spec.md`:
  - Job Story #3: Shifted focus from "lead times and stock levels" to stock availability visualization
  - Job Story #4: Changed from "revenue and sales KPIs" to inspection pass rate and manufacturing cost per unit

### Fixed

- Fixed plot sizing issue to allow page scrolling instead of plot-specific scrolling ([#29](https://github.com/UBC-MDS/DSCI-532_2026_27_Supply_Chain_Dashboard/issues/29))
- Fixed sizing of UI cards for consistent layout ([#29](https://github.com/UBC-MDS/DSCI-532_2026_27_Supply_Chain_Dashboard/issues/29))
- Fixed Mode plot issue where plot didn't revert when reselecting all filters ([#29](https://github.com/UBC-MDS/DSCI-532_2026_27_Supply_Chain_Dashboard/issues/29))

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

- Initial repository setup with standard directory structure ([#1](https://github.com/UBC-MDS/DSCI-532_2026_27_Supply_Chain_Dashboard/issues/1))
- Project proposal documentation in `reports/` directory ([#9](https://github.com/UBC-MDS/DSCI-532_2026_27_Supply_Chain_Dashboard/issues/9))
- Basic app skeleton in `src/app.py` with placeholder layout ([#13](https://github.com/UBC-MDS/DSCI-532_2026_27_Supply_Chain_Dashboard/issues/13))
- Environment configuration files (`environment.yml`) ([#13](https://github.com/UBC-MDS/DSCI-532_2026_27_Supply_Chain_Dashboard/issues/13))
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
