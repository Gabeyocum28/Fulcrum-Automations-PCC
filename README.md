# Fulcrum-Automations-PCC

## Projects

### 🏢 Inhouse Transfer
**Automated data processing and migration system for internal Fulcrum form transfers**

This project provides a comprehensive solution for automating the transfer and processing of Fulcrum form data between different systems, with intelligent field mapping, photo management, and data validation.

#### Features
✅ **Smart Field Mapping**: AI-powered field matching with confidence scoring  
✅ **Smart CSV Export**: Proper column names and clean data formatting  
✅ **Concurrent Photo Downloads**: 4-5x faster photo downloads with threading  
✅ **Organized Output**: Property folders with timestamp and structured layout  
✅ **Status Filtering**: Filter records by status before export  
✅ **Photo Management**: Download photos with proper indexing and organization  

#### Project Structure
```
Inhouse Transfer/
├── fulcrum_processor.py      # Main processing engine
├── auto_processor.py         # Automated workflow processor
├── fulcrum_config.ini        # Configuration settings
├── field_mappings.json       # Field mapping definitions
├── tests/                    # Comprehensive test suite
│   ├── integration/          # Integration tests
│   └── unit/                # Unit tests
├── debug/                    # Debug tools and test data
└── cached/                   # Cached data and exports
```

#### Quick Start
1. Install dependencies: `pip install -r requirements.txt`
2. Configure settings in `fulcrum_config.ini`
3. Run main processor: `python fulcrum_processor.py`

#### Use Cases
- **Form Migration**: Transfer data between different Fulcrum forms
- **Data Export**: Export Fulcrum data to CSV with photos
- **Field Mapping**: Automatically map fields between systems
- **Photo Management**: Download and organize associated photos
- **Data Validation**: Ensure data integrity during transfers

---

## Repository Overview
This repository contains automation tools and projects for PCC (Portland Community College) operations, focusing on streamlining data workflows and reducing manual processing time.

### Contributing
Please follow the established project structure and add comprehensive tests for new features.