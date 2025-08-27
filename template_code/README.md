# 🏗️ Fulcrum Template Code Collection

## 📚 **Overview**

This folder contains a comprehensive collection of reusable code templates, examples, and utilities for Fulcrum development projects. All code is based on official Fulcrum documentation and best practices from the [fulcrum-python library](https://github.com/fulcrumapp/fulcrum-python) and [Fulcrum Developer Documentation](https://docs.fulcrumapp.com/).

## 🗂️ **Folder Structure**

```
template_code/
├── README.md                           # This file
├── api_examples/                       # API client templates
│   └── fulcrum_api_client.py          # Comprehensive API client
├── query_examples/                     # Query API templates
│   └── fulcrum_query_api.py           # Query API client & templates
├── data_processing/                    # Data processing utilities
│   └── fulcrum_data_processor.py      # Data processing & export
├── automation_scripts/                 # Automation examples
├── utility_functions/                  # Utility functions
└── documentation/                      # Additional documentation
```

## 🚀 **Quick Start**

### **1. API Client Template**
```python
from template_code.api_examples.fulcrum_api_client import FulcrumAPIClient

# Initialize client
client = FulcrumAPIClient("your_api_token")

# Get all forms
forms = client.get_forms()
print(f"Found {len(forms)} forms")

# Get records from a form
records = client.get_records("form_id_here")
print(f"Found {len(records)} records")
```

### **2. Query API Template**
```python
from template_code.query_examples.fulcrum_query_api import FulcrumQueryAPI, FulcrumQueryTemplates

# Initialize query client
query_client = FulcrumQueryAPI("your_api_token")

# Use predefined templates
sql = FulcrumQueryTemplates.get_records_by_status("form_id", "active")
results = query_client.query_get(sql, format="json")

# Export to CSV
csv_data = query_client.query_get(sql, format="csv")
```

### **3. Data Processing Template**
```python
from template_code.data_processing.fulcrum_data_processor import FulcrumDataProcessor

# Initialize processor
processor = FulcrumDataProcessor("output_directory")

# Process records
df = processor.process_fulcrum_records(records, "Form Name")

# Export to multiple formats
processor.export_to_csv(df, "filename")
processor.export_to_excel(df, "filename")
processor.export_to_json(df, "filename")
```

## 🔧 **Available Templates**

### **API Examples (`api_examples/`)**
- **`fulcrum_api_client.py`** - Complete API client with all endpoints
  - Forms API (CRUD operations)
  - Records API (CRUD operations)
  - Classification Sets API
  - Photos API (upload/download)
  - Projects API
  - Changesets API
  - Rate limiting and error handling

### **Query Examples (`query_examples/`)**
- **`fulcrum_query_api.py`** - Query API client and templates
  - GET and POST query methods
  - Pre-built query templates
  - CSV, JSON, GeoJSON export
  - Pandas DataFrame integration
  - Advanced query examples

### **Data Processing (`data_processing/`)**
- **`fulcrum_data_processor.py`** - Data processing utilities
  - Record cleaning and normalization
  - Multiple export formats (CSV, JSON, Excel)
  - Photo download utilities
  - Summary report generation
  - Data package creation

## 📋 **Query Template Examples**

### **Basic Queries**
```python
# Get all records
FulcrumQueryTemplates.get_all_records(form_id)

# Get records by status
FulcrumQueryTemplates.get_records_by_status(form_id, "active")

# Get records by date range
FulcrumQueryTemplates.get_records_by_date_range(form_id, "2024-01-01", "2024-12-31")
```

### **Advanced Queries**
```python
# Get records with photo count
AdvancedFulcrumQueries.get_records_with_photo_count(form_id)

# Get records by time period
AdvancedFulcrumQueries.get_records_by_time_period(form_id, "month")

# Get records with geometry info
AdvancedFulcrumQueries.get_records_with_geometry_info(form_id)
```

### **Geographic Queries**
```python
# Get records within radius
FulcrumQueryTemplates.get_records_by_location(
    form_id, lat=40.7128, lon=-74.0060, radius_meters=1000
)

# Get records with coordinates
FulcrumQueryTemplates.get_records_with_coordinates(form_id)
```

## 📊 **Data Processing Features**

### **Export Formats**
- **CSV** - Standard CSV with metadata
- **JSON** - Structured JSON with metadata
- **Excel** - Multi-sheet Excel with metadata
- **Photos** - Download and organize photos
- **Reports** - Summary and analysis reports

### **Data Cleaning**
- Field name standardization
- Timestamp conversion
- Form values extraction
- Metadata addition
- Error handling

### **Filtering & Analysis**
- Status-based filtering
- Date range filtering
- Field value filtering
- Geographic filtering
- Custom criteria filtering

## 🔑 **Authentication & Setup**

### **API Token**
1. Get your API token from [Fulcrum Settings](https://web.fulcrumapp.com/settings/api)
2. Use the token in all client initializations
3. Store securely (use environment variables in production)

### **Dependencies**
```bash
pip install requests pandas openpyxl
```

## 📖 **Documentation References**

### **Official Fulcrum Resources**
- [Fulcrum Python Library](https://github.com/fulcrumapp/fulcrum-python) - Official Python client
- [Fulcrum Developer Documentation](https://docs.fulcrumapp.com/) - Complete API reference
- [Query API Reference](https://docs.fulcrumapp.com/reference/query-get) - Query API documentation
- [Fulcrum GitHub Organization](https://github.com/orgs/fulcrumapp/repositories) - 100+ repositories

### **Key API Endpoints**
- **Forms**: `/api/v2/forms`
- **Records**: `/api/v2/records`
- **Query**: `/api/v2/query`
- **Classification Sets**: `/api/v2/classification_sets`
- **Photos**: `/api/v2/photos`
- **Projects**: `/api/v2/projects`

## 🎯 **Use Cases**

### **Data Export & Analysis**
- Export form data to CSV/Excel
- Generate summary reports
- Analyze record patterns
- Photo and attachment management

### **Automation & Integration**
- Automated data processing
- Scheduled exports
- Integration with other systems
- Batch operations

### **Quality Control**
- Data validation
- Error checking
- Status monitoring
- Performance analysis

## 🚀 **Best Practices**

### **Rate Limiting**
- Implement delays between API calls
- Use batch operations when possible
- Monitor API usage

### **Error Handling**
- Always check API responses
- Implement retry logic
- Log errors for debugging

### **Data Management**
- Process data in chunks for large datasets
- Use appropriate export formats
- Include metadata with exports

## 🔄 **Extending Templates**

### **Adding New API Endpoints**
```python
def new_endpoint_method(self, param1: str, param2: str) -> Dict:
    """New endpoint method"""
    endpoint = "new_endpoint"
    params = {'param1': param1, 'param2': param2}
    return self._make_request("GET", endpoint, params=params)
```

### **Adding New Query Templates**
```python
@staticmethod
def new_query_template(form_id: str, custom_param: str) -> str:
    """New query template"""
    return f"SELECT * FROM {form_id} WHERE custom_field = '{custom_param}'"
```

### **Adding New Export Formats**
```python
def export_to_new_format(self, df: pd.DataFrame, filename: str) -> str:
    """Export to new format"""
    # Implementation here
    pass
```

## 📝 **Contributing**

### **Template Guidelines**
- Follow existing code patterns
- Include comprehensive documentation
- Add usage examples
- Implement proper error handling
- Use type hints

### **Testing**
- Test with real Fulcrum data
- Verify API responses
- Check export formats
- Validate error handling

## 🎉 **Getting Help**

### **Common Issues**
- **API Token Issues**: Verify token is valid and has proper permissions
- **Rate Limiting**: Implement delays between requests
- **Data Format**: Check Fulcrum API response structure
- **Export Errors**: Verify file permissions and disk space

### **Resources**
- Check the official Fulcrum documentation
- Review the fulcrum-python library examples
- Use the provided template code as reference
- Implement proper logging for debugging

## 📄 **License**

This template code is provided as-is for educational and development purposes. Please refer to the original Fulcrum documentation and libraries for licensing information.

---

**Happy Coding with Fulcrum! 🚀✨**
