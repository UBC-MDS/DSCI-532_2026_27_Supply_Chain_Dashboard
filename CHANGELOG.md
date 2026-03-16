# Changelog

All notable changes to the Supply Chain Dashboard project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [0.4.0] - 2026-03-15

### Added

- `Makefile` for test setup + running tests ([#61](https://github.com/UBC-MDS/DSCI-532_2026_27_Supply_Chain_Dashboard/issues/61))
- Created `compare.py` by extracting `def compare()` to its own file to enable testing ([#61](https://github.com/UBC-MDS/DSCI-532_2026_27_Supply_Chain_Dashboard/issues/61))
- `test_ui.py` for end to end tests ([#61](https://github.com/UBC-MDS/DSCI-532_2026_27_Supply_Chain_Dashboard/issues/61))
- Added Parquet and DuckDB database retrieval functionality ([#59](https://github.com/UBC-MDS/DSCI-532_2026_27_Supply_Chain_Dashboard/issues/59))
- Added reset button for sidebar filters ([#82](https://github.com/UBC-MDS/DSCI-532_2026_27_Supply_Chain_Dashboard/pull/82))
- Added faceting by shapes in SKU scatterplot([#71](https://github.com/UBC-MDS/DSCI-532_2026_27_Supply_Chain_Dashboard/pull/71))

### Changed

- Updated `requirements.txt` to include `pytest` and `pytest-playwright` ([#61](https://github.com/UBC-MDS/DSCI-532_2026_27_Supply_Chain_Dashboard/issues/61))
- `README` instructions ([#63](https://github.com/UBC-MDS/DSCI-532_2026_27_Supply_Chain_Dashboard/issues/63))
- Changed width of facet charts to prevent horizontal scrolling ([#76](https://github.com/UBC-MDS/DSCI-532_2026_27_Supply_Chain_Dashboard/issues/76))
- Changed dashboard widget widths to remove the need for scrolling([#79](https://github.com/UBC-MDS/DSCI-532_2026_27_Supply_Chain_Dashboard/issues/79))

### Fixed
- Fixed SKU scatterplot not filtering when clicking sidebar after click event implementation ([#77](https://github.com/UBC-MDS/DSCI-532_2026_27_Supply_Chain_Dashboard/issues/77))
- Fixed issue with filters not being applied to SKU scatterplot ([#83](https://github.com/UBC-MDS/DSCI-532_2026_27_Supply_Chain_Dashboard/pull/83))
- Fixed issues with AI Explorer ([#80](https://github.com/UBC-MDS/DSCI-532_2026_27_Supply_Chain_Dashboard/pull/80))

### Known Issues
- N/A

### Release Highlight
- Our motivation this milestone was to address feedback from our peers and polish existing features. This ranged from performance improvements in our AI Explorer, to adding a legend to better understand our KPI cards.

- Overhauled the UI and logic of the AI Explorer tab
- Refined the dashbaord's layout to make visuals easier to understand (e.g. adding a color legend for KPI cards) and use (e.g. removing the need to scroll on the dashboard)
- Created unit and UI tests for more secure future development

### Collaboration
- **CONTRIBUTING.md:**: Updated in PR [#73](https://github.com/UBC-MDS/DSCI-532_2026_27_Supply_Chain_Dashboard/pull/73)
- **M3 retrospective:**: After reviewing the collaboration feedback with the group, the biggest change we made was enforcing the policy of 1 review per PR. Unexpectedly, it did not significantly impact the speed of development because we were all on top of replying to Slack messages and letting each other know when a PR was created and what it aimed to accomplish.
- **M4:**: In this Milestone, we tried implementing a short meeting at the start of the lab working session so everyone was caught up with each other's progress and what issues were outstanding. This worked quite well in ensuring everyone was clear on what the priority items were, as well as giving members a chance to bring up any concerns with workload or open PR's that still needed reviewing.

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

**Trade-offs**
- The main trade-off we had to deal with when prioritizing feedback items to address was whether or not we had time to improve usability of our dashboard by adding more definitions and legends for graphs.Full rationale is in [#64](https://github.com/UBC-MDS/DSCI-532_2026_27_Supply_Chain_Dashboard/issues/64)

**Most Useful**
- In our opinion, the most useful material were the code examples. Because none of us had worked with Shiny before, figuring out the syntax was the most challenging aspect of this project. The code examples not only gave us a head start on which functions would be the most useful, it also gave us a template that we would be able to adapt from, saving a lot of headache versus figuring out the right syntax and functions to use through trial and error.

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
