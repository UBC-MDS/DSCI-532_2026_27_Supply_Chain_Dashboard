# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.2.0]

### Added
- `reports/m2_spec.md` as per App specification requirements. ([#25](https://github.com/UBC-MDS/DSCI-532_2026_27_Supply_Chain_Dashboard/issues/25))
- Changelog file ([#31](https://github.com/UBC-MDS/DSCI-532_2026_27_Supply_Chain_Dashboard/issues/31))
- `.gitignore` file
- `requirements.txt` file for Posit Cloud ([#24](https://github.com/UBC-MDS/DSCI-532_2026_27_Supply_Chain_Dashboard/issues/24))
- Data page with `DataTable` using tabs ([#36](https://github.com/UBC-MDS/DSCI-532_2026_27_Supply_Chain_Dashboard/issues/36))
- Added footer to the Dashboard with GitHub link, Author names, and Last Updated date ([#33](https://github.com/UBC-MDS/DSCI-532_2026_27_Supply_Chain_Dashboard/issues/33))

### Changed
- Update `environment.yml` to include `altair` and changed other versions to ensure consistency. ([#32](https://github.com/UBC-MDS/DSCI-532_2026_27_Supply_Chain_Dashboard/issues/32))
- Move app dependencies to `requirements.txt` ([#24](https://github.com/UBC-MDS/DSCI-532_2026_27_Supply_Chain_Dashboard/issues/24))
- `README` instructions ([#24](https://github.com/UBC-MDS/DSCI-532_2026_27_Supply_Chain_Dashboard/issues/24))
- Changed layout to put KPIs on top ([#29](https://github.com/UBC-MDS/DSCI-532_2026_27_Supply_Chain_Dashboard/issues/29))
- Moved download buttons to Data page ([#36](https://github.com/UBC-MDS/DSCI-532_2026_27_Supply_Chain_Dashboard/issues/36))


### Fixed
- Fixed plot sizing so rather than having to scroll the plots, we scroll the page ([#29](https://github.com/UBC-MDS/DSCI-532_2026_27_Supply_Chain_Dashboard/issues/29))
- Fixed sizing of UI cards ([#29](https://github.com/UBC-MDS/DSCI-532_2026_27_Supply_Chain_Dashboard/issues/29))
- Fixed Mode plot issue where plot didn't revert when reselecting all filters

### CI / Infrastructure
- Created `dev` branch for staging and preview purposes.
- Deploy stable build (`main`) to Posit Connect Cloud.
- Deploy preview build (`dev`) to Posit Connect Cloud.

### Known Issues

### Reflection

**Implementation Status:**

Job Stories:

- Job Story 1: implemented via the Cost vs. Time Tradeoff by Mode plot and Shipping Cost Matrix (Route vs. Mode).
- Job Story 2: implemented via the Defect Rates by SKU scatterplot.
- Job Story 3: revised via the Stock Availability barchart. Lead times was not included in the Stock Availability barchart.
- Job Story 4: revised with Avg. Cost per Unit and Inspection Pass Rate KPIs. They are not direct KPIs for revenue and product sales but they are connected to that assumption.

**Deviations:**

- We changed the layout of the dashboard since our KPIs were on the bottom. It was suggested that KPIs should be on the top left as it is the most important part. We also changed the layout to fit our plots better based on the movement of the KPI cards.
- Added a multi-page layout to add a separate DataTable that was not in the initial sketch.

**Known Issues:**

- We had an issue with the Altair plot not going back to its original state when reselecting all the filters. It was resolved by giving it a set width instead of setting it to "container".

**Best Practices:**

- Added comparisons vs a baseline for the KPIs like how it was shown in Lecture 4.
- Used a colorblind friendly palette.

**Self Assessment:**

- Strengths: Our layout for the dashboard was well revised to make it so our most important plots are on the top.
- Limitations: Our current plots for Job Story 3 and 4 were revised from the original changing how it approaches the job story.
- Future Improvements: Add a reset filter button, when clicking the download button have a popup to choose location, revise font formatting for KPI cards.

## [0.0.1] - 2026-02-13

### Added
- Initial repo setup ([#1](https://github.com/UBC-MDS/DSCI-532_2026_27_Supply_Chain_Dashboard/issues/1))
- Created proposal structure based on example repo ([#6](https://github.com/UBC-MDS/DSCI-532_2026_27_Supply_Chain_Dashboard/issues/6))
- Complete sections 1 and 2 of project proposal ([#11](https://github.com/UBC-MDS/DSCI-532_2026_27_Supply_Chain_Dashboard/issues/11))
- App skeleton and environment.yml ([#13](https://github.com/UBC-MDS/DSCI-532_2026_27_Supply_Chain_Dashboard/issues/13))
- Complete project documentation ([#9](https://github.com/UBC-MDS/DSCI-532_2026_27_Supply_Chain_Dashboard/issues/9))
- Complete project proposal sections 3 & 4 ([#16](https://github.com/UBC-MDS/DSCI-532_2026_27_Supply_Chain_Dashboard/issues/16))
- Proposal section 5 ([#18](https://github.com/UBC-MDS/DSCI-532_2026_27_Supply_Chain_Dashboard/issues/18))