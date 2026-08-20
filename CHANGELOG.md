# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.0.23] - 2026-08-20
- fix: correctly deserialize workflow node_finished stream data
- fix: ignore undefined stream events

## [0.0.21] - 2026-03-10
- feat: add more file types

## [0.0.20] - 2026-03-02
- refactor: exclude None values in model_dump for API requests

## [0.0.17] - 2026-02-02
- Support StreamEvent: node_retry
## [0.0.16] - 2025-01-XX
- Add support for getting segments/chunks from documents (`get_segments`, `aget_segments`)
- Add support for updating segments/chunks in documents (`update_segment`, `aupdate_segment`)
- Refactor examples/datasets.py to use CLI with --mode argument instead of commenting/uncommenting code
- Fix UpdateSegmentResponse model to match API response structure

## [0.0.15] - 2025-10-21
- Support Converstaion History message Async

## [0.0.14] - 2025-08-14
- Support Converstaion History message

## [0.0.11] - 2025-06-12
- Improved create_document_by_file: now supports passing a file path directly.
- Ensures only the base filename is sent to the API, preventing invalid filename errors.
- Internal refactor to use pathlib for filename extraction. 

## [0.0.8] - 2025-06-12
- Support document metadata utils (get, update)

## [0.0.7] - Previous Release
- Initial dataset management functionality

