# 🏢 Inhouse Transfer

**Automated data processing and migration system for internal Fulcrum form transfers**

This project provides a comprehensive solution for automating the transfer and processing of Fulcrum form data between different systems, with intelligent field mapping, photo management, and data validation.

## 🚀 Features

✅ **Smart Field Mapping**: AI-powered field matching with confidence scoring  
✅ **Smart CSV Export**: Proper column names and clean data formatting  
✅ **Concurrent Photo Downloads**: 4-5x faster photo downloads with threading  
✅ **Organized Output**: Property folders with timestamp and structured layout  
✅ **Status Filtering**: Filter records by status before export  
✅ **Photo Management**: Download photos with proper indexing and organization  
✅ **Import Processing**: Complete data processing and import workflows  

## 📁 Project Structure

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

## 🚀 Quick Start

### 1. Installation
```bash
pip install -r requirements.txt
```

### 2. Setup
```bash
python fulcrum_processor.py
# Choose option 1: Setup API credentials
```

### 3. Export Data
```bash
python fulcrum_processor.py  
# Choose option 3: Filter records by status and export to CSV
```

## 🔧 Main Features

### CSV Export with Photo Downloads
- Export filtered data with proper column names
- Concurrent photo downloads (4-5x faster)
- Organized folder structure with timestamps
- Photo indexing and record mapping

### Output Structure
```
cached/
└── {PropertyName}_{Status}_{YYYYMMDD_HHMMSS}/
    ├── {PropertyName}_data.csv
    └── photos/
        ├── photo_index.csv
        └── {record_id}_{field_name}_{photo_id}.jpg
```

### Speed Improvements
- **Concurrent Downloads**: Up to 5 photos download simultaneously
- **Smart Progress**: Real-time progress with milestone updates  
- **Error Isolation**: Individual failures don't stop other downloads
- **API-Friendly**: Rate limiting to avoid overwhelming Fulcrum

## 📋 Usage

### Main Menu Options
1. Setup API credentials
2. List available forms  
3. **Filter records by status and export to CSV** ⭐
4. Download Data
5. Setup property mappings
6. Setup target form (for imports)
7. Process property data
8. Batch process multiple properties
9. Fully automated processing (download + import)
10. **Explore classification structure** 🔍

### Export Workflow
1. **Select Status Filter**: Choose which record statuses to export
2. **Generate CSV**: Clean data with proper column names
3. **Download Photos**: Optional concurrent photo downloads
4. **Organized Output**: Everything packaged in timestamped folders

## 🧠 Enhanced Classification Search 🔍

The tool now provides **deep classification search** that goes beyond surface-level matches:

- **Depth Tracking**: Shows exactly how deep each match is found in the hierarchy
- **Full Path Display**: Reveals the complete classification path (e.g., `LMH → NAVY → Bayview Hills District`)
- **Debug Mode**: Detailed search process for understanding how matches are found
- **Structure Explorer**: Interactive tool to explore the full classification hierarchy
- **Multiple Child Keys**: Searches through various nested structures (`children`, `items`, `child_items`, `sub_items`)

**Example Output:**
```
📁 Searching classification set: SCHOOLS
   Items in set: 10
   🔍 DEBUG MODE: Showing detailed search for SCHOOLS
  [D0] ✅ Heber Elementary School District (score: 0.50)
  [D1] ✅ San Dieguito Union High School District (score: 0.50)
  [D2] ✅ Santee School District (score: 0.50)
        📍 Full path: SCHOOLS → NAVY → Santee School District
```

## 🧠 Smart Field Mapping System 🧠

The tool now features an **intelligent field mapping system** that learns and remembers your preferences:

- **Memory System**: Remembers successful field mappings across sessions
- **Synonym Matching**: Uses comprehensive synonym dictionaries for better field recognition
- **Duplicate Prevention**: Ensures each source field can only map to one target field
- **Smart Suggestions**: Provides intelligent recommendations based on field similarity
- **Learning History**: Tracks mapping attempts to improve future suggestions

**Key Features:**
- **One-to-One Mapping**: `Number` can only map to `Number`, not also to `Unit Number`
- **Intelligent Recognition**: `Slice Length` automatically matches `slice_length`, `length`, etc.
- **Cross-Form Learning**: Mappings learned from one form help with similar forms
- **Memory Management**: View, export, and manage your field mapping memory

**Example Smart Mapping:**
```
✅ Survey Date ← survey_date (exact match)
✅ Address ← property_address (synonym match)
✅ Slice Length ← slice_length (exact match)
✅ Expansion Joint Length ← expansion_joint_length (exact match)
✅ High Point ← high_point (exact match)
✅ Low Point ← low_point (exact match)
✅ Technician Notes ← technician_notes (exact match)
✅ Before Photos ← before_pictures (synonym match)
✅ Date Completed ← completion_date (synonym match)
```

## 🧪 Testing

### Unit Tests
```bash
python tests/unit/test_quick_export.py
python tests/unit/test_photo_download.py
```

### Integration Tests  
```bash
python tests/integration/test_concurrent_download.py
python tests/integration/test_organized_export.py
python tests/integration/test_enhanced_classification_search.py
python tests/integration/test_smart_field_mapping.py
```

### Debug Tools
```bash
python debug/debug_export.py
```

## 📦 Requirements

```
pandas>=1.5.0
requests>=2.28.0
configparser>=5.3.0
openpyxl>=3.1.0
```

## ⚙️ Configuration

### API Setup
- Get your Fulcrum API token from https://web.fulcrumapp.com/settings/api
- Run the main script and choose option 1 to configure

### Property Mappings (Optional)
For import workflows, set up property mappings via option 5

## ⚡ Performance

### Photo Download Speed
- **Sequential**: ~3.3 seconds for 5 photos
- **Concurrent**: ~0.8 seconds for 5 photos  
- **Speedup**: 4x faster downloads

### Large Exports
- Handles hundreds of records efficiently
- Progress tracking for long operations
- Memory-efficient processing
- Automatic retry on failures

## 🔒 Security

- API tokens stored securely in config files
- No credentials in code or logs
- Proper file permissions on sensitive files
- Rate limiting respects API limits

## 🆘 Support

### Common Issues
- **Column names showing as numbers**: Fixed with proper form schema mapping
- **Slow photo downloads**: Solved with concurrent downloading
- **Unorganized outputs**: Resolved with timestamped folder structure

### Get Help
- Check test files for examples
- Review debug tools for troubleshooting  
- Examine folder structure in cached/ directory

---

This tool provides a complete solution for Fulcrum data export with professional organization, fast downloads, and clean output formatting!
