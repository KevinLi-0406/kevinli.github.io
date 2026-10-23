# Changelog

All notable changes to the D365 Log Sync Alert system will be documented in this file.

## [Unreleased]

### Planned
- Enhanced error handling for D365 API timeouts
- Add support for custom alert routing rules
- Implement alert deduplication across time windows

---

## [1.3.0] - 2026-10-23

### Added
- **Interactive Flowchart**: Created `flowchart.html` with clickable nodes showing the complete data flow from D365 to Feishu alerts
- **Comprehensive README**: Expanded documentation with detailed 8-step data flow, table schemas, and deployment guide

### Fixed
- **config_loader.py Field Index Bug**: Fixed incorrect field indexing when reading card configuration tables. Now uses explicit `--field` parameters to ensure correct field mapping
- **"是否启用" (enabled) Field**: Correctly reads the checkbox field to filter which alert scenarios should be processed. Only enabled scenarios generate cards

### Changed
- **Documentation Structure**: Reorganized README with clear sections for architecture, data flow, table schemas, and troubleshooting

### Technical Details
- Modified `load_card_configs()` in `config_loader.py` to use field-name-based indexing instead of positional indexing
- Added validation to ensure only `enabled=True` scenarios are processed in `card.py`

---

## [1.2.0] - 2026-10-22

### Added
- **Service Store Name Field**: Added new field to D365 integration log table to track which service store (repair center) each work order belongs to
- **Auto Owner Assignment**: Implemented automatic responsible person assignment based on Service Store Name mapping from 迈创站点运营 table
- **Non-Maitrox Owner Field**: Added "责任人" (owner) field to non-Maitrox config table for per-scenario owner assignment
- **40 New Abnormal Scenarios**: Expanded exception scenario options from 18 to 58, covering all B2X, MySav, and SDS integration scenarios

### Changed
- **Config Table Split**: Split single config table into two separate tables:
  - `tblePVTwOyMzPNG8` for Maitrox scenarios (Push WO to SCM)
  - `tblbscUEUlXSUQE4` for non-Maitrox scenarios (B2X, MySav, SDS)
- **Naming Convention**: Unified all scenario names to English prefix format (Maitrox-, B2X-, MySav-, SDS-)
- **Card Aggregation**: Implemented scenario grouping by aggregation codes (GROUP_DATA, GROUP_INTERFACE, GROUP_B2X, GROUP_MYSAV)

### Fixed
- **Historical Data Update**: Batch updated 666 historical records with correct Service Store Name and responsible person assignments
- **Pending Records**: Re-judged 359 "待补充" (pending) records using updated config rules

### Data Migration
- Updated 615 records with Service Store Name from D365 workorder entity
- Assigned responsible persons to all 666 records (100% coverage)
- Owner distribution: 廖利丽 (260), 李奕兴 (98), 庞舒尹 (87), 贡梦夏 (76), others

### Technical Details
- Modified `sync.py` to add `fetch_site_ops_mapping()` function
- Updated `parse_record()` to implement owner assignment logic:
  - Maitrox scenarios: match owner from Service Store Name
  - Non-Maitrox scenarios: read owner from config table
- Added `rejudge_pending_records.py` script for batch re-judgment

---

## [1.1.0] - 2026-10-14

### Added
- **Card Configuration Tables**: Created two new tables for alert card configuration:
  - `tblWugqhkySxdnlA` for Maitrox card configs
  - `tblcNZKfDloFgDPc` for non-Maitrox card configs
- **Configurable Card Properties**: Each scenario can now configure:
  - Card title and subtitle template
  - Card color (red, orange, yellow, blue, grey)
  - Whether to @mention users
  - Target chat group
  - Aggregation group code
  - Max records per card
- **Site Operations Table**: Created `tbl0Xiuz6KJ3SSC4` to map Service Store Names to responsible persons (16 records)

### Changed
- **Card Generation Logic**: Refactored `card.py` to read configurations from Bitable tables instead of hardcoded values
- **Aggregation Support**: Cards now group records by aggregation code and use first record's config for styling

### Technical Details
- Created `config_loader.py` module to centralize configuration loading
- Implemented fallback to default configs if table read fails
- Added support for `{scenario}` placeholder in subtitle templates

---

## [1.0.0] - 2026-10-13

### Added
- **Initial Implementation**: Complete D365 integration log sync and alert system
- **FetchXML Query**: Defined query to fetch integration logs from D365 production environment
- **Abnormal Scenario Detection**: Implemented rule-based detection using config table `tblIqZ9T8Ekj9h8y`
- **Alert Card Generation**: Created Card 2.0 format alerts with collapsible panels for work order details
- **Automated Workflow**: Hourly cron job (ID: a09e0a38-f275-4903-bd2d-839827902978) to sync and alert

### Core Features
- Query D365 production environment for failed integration logs (last 7 days)
- Detect abnormal scenarios based on configurable rules
- Write new records to Feishu Bitable with deduplication
- Generate alert cards for critical scenarios (BOM, master data, interface issues)
- Send cards to scm-spp communication group
- Mark records as alerted to prevent duplicate notifications

### Configuration
- **Log Table**: `tblTWNXVEKv0IScf` (D365 integration logs)
- **Config Table**: `tblIqZ9T8Ekj9h8y` (abnormal scenario rules)
- **Alert Group**: `oc_f1890b5bed23c01839dfb517c63bec48` (scm-spp group)

### Scripts
- `sync.py`: Core sync logic with deduplication and scenario detection
- `rules.py`: Abnormal scenario judgment engine
- `card.py`: Alert card generation with auto-splitting
- `common.py`: Constants and field mappings
- `fetch_existing_ids.py`: Deduplication helper

---

## Version History Summary

| Version | Date | Key Changes |
|---------|------|-------------|
| 1.3.0 | 2026-10-23 | Flowchart, README, config_loader fix, enabled field |
| 1.2.0 | 2026-10-22 | Service Store Name, auto owner, config split, 40 new scenarios |
| 1.1.0 | 2026-10-14 | Card config tables, site operations mapping, aggregation |
| 1.0.0 | 2026-10-13 | Initial release with core sync and alert functionality |

---

## Migration Notes

### Upgrading to 1.2.0
- Run `step1_query_service_store.py` and `step2_update_base.py` to populate Service Store Name for historical records
- Run `rejudge_pending_records.py` to re-judge records with "待补充" status
- Update SKILL.md to reflect new table IDs

### Upgrading to 1.1.0
- Create card configuration tables with appropriate fields
- Populate site operations table with Service Store Name to owner mappings
- Update card.py to use config_loader instead of hardcoded values

---

## Contributing

For internal use by SPP team. Contact Kevin Li (yixing.li@ninebot.com) for questions.

## License

Internal use only - Ninebot Segway
