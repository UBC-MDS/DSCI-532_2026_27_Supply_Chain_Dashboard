# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.2.0]

### Added
- `reports/m2_spec.md` as per requirements.
- 

### Changed
- Updated `environment.yml` to include `altair` and changed other versions to ensure consistency.


### Fixed
- Removed unnecessary generated files from the repository ([#85](https://github.com/UBC-MDS/ez-df-data-validator/issues/85)).

### CI / Infrastructure
- Created `dev` branch for staging and preview purposes.
- Deploy stable build (`main`) to Posit Connect Cloud.
- Deploy preview build (`dev`) to Posit Connect Cloud.

## [0.0.1] - 2026-01-10

### Added
- Initial repo setup ([#7](https://github.com/UBC-MDS/ez-df-data-validator/issues/7))
- edit readme ([#9](https://github.com/UBC-MDS/ez-df-data-validator/issues/9))
- create function spec for find_duplicates ([#10](https://github.com/UBC-MDS/ez-df-data-validator/issues/10))
- Add SchemaStandardizer for initial dataframe hygiene ([#11](https://github.com/UBC-MDS/ez-df-data-validator/issues/11))
- Handle missing ([#14](https://github.com/UBC-MDS/ez-df-data-validator/issues/14))
- Add missing_summary function specification ([#12](https://github.com/UBC-MDS/ez-df-data-validator/issues/12))
- Update README with missing_summary function details ([#15](https://github.com/UBC-MDS/ez-df-data-validator/issues/15))
- Format readme ([#16](https://github.com/UBC-MDS/ez-df-data-validator/issues/16))