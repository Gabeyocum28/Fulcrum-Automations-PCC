#!/usr/bin/env python3
"""
Fulcrum Query API Template
Based on official Fulcrum Query API documentation
Reference: https://docs.fulcrumapp.com/reference/query-get
"""

import requests
import json
import pandas as pd
from typing import Dict, List, Optional, Union
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class FulcrumQueryAPI:
    """
    Fulcrum Query API Client
    Supports both GET and POST query methods
    """
    
    def __init__(self, api_token: str, base_url: str = "https://api.fulcrumapp.com/api/v2"):
        """
        Initialize Query API Client
        
        Args:
            api_token: Your Fulcrum API token
            base_url: Fulcrum API base URL
        """
        self.api_token = api_token
        self.base_url = base_url
        self.headers = {
            "X-ApiToken": api_token,
            "Content-Type": "application/json"
        }
        self.session = requests.Session()
        self.session.headers.update(self.headers)
    
    def query_get(self, sql_query: str, format: str = "json", **params) -> Union[Dict, str]:
        """
        Execute GET query (for simple queries)
        
        Args:
            sql_query: SQL query string
            format: Output format ('json', 'csv', 'geojson')
            **params: Additional query parameters
            
        Returns:
            Query results in specified format
        """
        endpoint = "query"
        params.update({
            'q': sql_query,
            'format': format
        })
        
        try:
            response = self.session.get(f"{self.base_url}/{endpoint}", params=params)
            response.raise_for_status()
            
            if format == "json":
                return response.json()
            else:
                return response.text
                
        except requests.exceptions.RequestException as e:
            logger.error(f"GET query failed: {e}")
            raise
    
    def query_post(self, sql_query: str, format: str = "json", **params) -> Union[Dict, str]:
        """
        Execute POST query (for complex queries)
        
        Args:
            sql_query: SQL query string
            format: Output format ('json', 'csv', 'geojson')
            **params: Additional query parameters
            
        Returns:
            Query results in specified format
        """
        endpoint = "query"
        data = {
            'q': sql_query,
            'format': format,
            **params
        }
        
        try:
            response = self.session.post(f"{self.base_url}/{endpoint}", json=data)
            response.raise_for_status()
            
            if format == "json":
                return response.json()
            else:
                return response.text
                
        except requests.exceptions.RequestException as e:
            logger.error(f"POST query failed: {e}")
            raise
    
    def query_to_dataframe(self, sql_query: str, **params) -> pd.DataFrame:
        """
        Execute query and return results as pandas DataFrame
        
        Args:
            sql_query: SQL query string
            **params: Additional query parameters
            
        Returns:
            Pandas DataFrame with query results
        """
        try:
            results = self.query_get(sql_query, format="json", **params)
            
            if isinstance(results, dict) and 'rows' in results:
                # Convert to DataFrame
                df = pd.DataFrame(results['rows'])
                
                # Add field names if available
                if 'fields' in results:
                    field_names = [field['name'] for field in results['fields']]
                    if len(field_names) == len(df.columns):
                        df.columns = field_names
                
                return df
            else:
                logger.warning("Query results don't contain expected 'rows' field")
                return pd.DataFrame()
                
        except Exception as e:
            logger.error(f"Failed to convert query to DataFrame: {e}")
            return pd.DataFrame()

# ============================================================================
# QUERY TEMPLATES AND EXAMPLES
# ============================================================================

class FulcrumQueryTemplates:
    """
    Collection of useful Fulcrum Query API templates
    """
    
    @staticmethod
    def get_all_records(form_id: str) -> str:
        """Get all records from a form"""
        return f"SELECT * FROM {form_id}"
    
    @staticmethod
    def get_records_by_status(form_id: str, status: str) -> str:
        """Get records by status"""
        return f"SELECT * FROM {form_id} WHERE _status = '{status}'"
    
    @staticmethod
    def get_records_by_date_range(form_id: str, start_date: str, end_date: str) -> str:
        """Get records within a date range"""
        return f"""
        SELECT * FROM {form_id} 
        WHERE _created_at >= '{start_date}' 
        AND _created_at <= '{end_date}'
        """
    
    @staticmethod
    def get_records_by_field_value(form_id: str, field_name: str, field_value: str) -> str:
        """Get records by specific field value"""
        return f"SELECT * FROM {form_id} WHERE {field_name} = '{field_value}'"
    
    @staticmethod
    def get_records_with_photos(form_id: str) -> str:
        """Get records that have photos"""
        return f"SELECT * FROM {form_id} WHERE _photos IS NOT NULL"
    
    @staticmethod
    def get_records_by_location(form_id: str, lat: float, lon: float, radius_meters: float) -> str:
        """Get records within a geographic radius"""
        return f"""
        SELECT * FROM {form_id} 
        WHERE ST_DWithin(
            _geometry, 
            ST_SetSRID(ST_MakePoint({lon}, {lat}), 4326), 
            {radius_meters}
        )
        """
    
    @staticmethod
    def get_records_by_classification(form_id: str, classification_field: str, classification_value: str) -> str:
        """Get records by classification value"""
        return f"SELECT * FROM {form_id} WHERE {classification_field} = '{classification_value}'"
    
    @staticmethod
    def get_records_count_by_status(form_id: str) -> str:
        """Get count of records by status"""
        return f"""
        SELECT _status, COUNT(*) as count 
        FROM {form_id} 
        GROUP BY _status
        """
    
    @staticmethod
    def get_records_by_user(form_id: str, user_id: str) -> str:
        """Get records created by a specific user"""
        return f"SELECT * FROM {form_id} WHERE _created_by = '{user_id}'"
    
    @staticmethod
    def get_records_with_attachments(form_id: str) -> str:
        """Get records that have any type of attachments"""
        return f"""
        SELECT * FROM {form_id} 
        WHERE _photos IS NOT NULL 
        OR _signatures IS NOT NULL 
        OR _audio IS NOT NULL 
        OR _video IS NOT NULL
        """
    
    @staticmethod
    def get_records_by_priority(form_id: str, priority_field: str, priority_values: List[str]) -> str:
        """Get records by priority values"""
        priority_list = "', '".join(priority_values)
        return f"SELECT * FROM {form_id} WHERE {priority_field} IN ('{priority_list}')"
    
    @staticmethod
    def get_records_with_coordinates(form_id: str) -> str:
        """Get records that have geographic coordinates"""
        return f"SELECT * FROM {form_id} WHERE _geometry IS NOT NULL"
    
    @staticmethod
    def get_records_by_custom_field(form_id: str, field_name: str, operator: str, value: str) -> str:
        """Get records by custom field with operator"""
        return f"SELECT * FROM {form_id} WHERE {field_name} {operator} '{value}'"
    
    @staticmethod
    def get_records_with_notes(form_id: str) -> str:
        """Get records that have notes"""
        return f"SELECT * FROM {form_id} WHERE _notes IS NOT NULL AND _notes != ''"
    
    @staticmethod
    def get_records_by_multiple_criteria(form_id: str, criteria: Dict[str, str]) -> str:
        """Get records by multiple criteria"""
        conditions = []
        for field, value in criteria.items():
            conditions.append(f"{field} = '{value}'")
        
        where_clause = " AND ".join(conditions)
        return f"SELECT * FROM {form_id} WHERE {where_clause}"

# ============================================================================
# ADVANCED QUERY EXAMPLES
# ============================================================================

class AdvancedFulcrumQueries:
    """
    Advanced query examples for complex data analysis
    """
    
    @staticmethod
    def get_records_with_photo_count(form_id: str) -> str:
        """Get records with photo count"""
        return f"""
        SELECT 
            *,
            CASE 
                WHEN _photos IS NULL THEN 0
                ELSE json_array_length(_photos)
            END as photo_count
        FROM {form_id}
        """
    
    @staticmethod
    def get_records_by_time_period(form_id: str, period: str = "day") -> str:
        """Get records grouped by time period"""
        if period == "day":
            date_format = "YYYY-MM-DD"
        elif period == "week":
            date_format = "YYYY-WW"
        elif period == "month":
            date_format = "YYYY-MM"
        else:
            date_format = "YYYY-MM-DD"
        
        return f"""
        SELECT 
            DATE_TRUNC('{period}', _created_at::timestamp) as period,
            COUNT(*) as record_count
        FROM {form_id}
        GROUP BY period
        ORDER BY period
        """
    
    @staticmethod
    def get_records_with_geometry_info(form_id: str) -> str:
        """Get records with detailed geometry information"""
        return f"""
        SELECT 
            *,
            ST_X(_geometry) as longitude,
            ST_Y(_geometry) as latitude,
            ST_AsText(_geometry) as geometry_text
        FROM {form_id}
        WHERE _geometry IS NOT NULL
        """
    
    @staticmethod
    def get_records_by_field_pattern(form_id: str, field_name: str, pattern: str) -> str:
        """Get records by field pattern matching"""
        return f"SELECT * FROM {form_id} WHERE {field_name} LIKE '%{pattern}%'"
    
    @staticmethod
    def get_records_with_validation_errors(form_id: str) -> str:
        """Get records that may have validation issues"""
        return f"""
        SELECT * FROM {form_id} 
        WHERE _status = 'error' 
        OR _validation_errors IS NOT NULL
        """

# ============================================================================
# USAGE EXAMPLES
# ============================================================================

def example_usage():
    """Example usage of the Fulcrum Query API"""
    
    # Initialize client
    api_token = "your_api_token_here"
    query_client = FulcrumQueryAPI(api_token)
    
    # Example form ID (replace with actual form ID)
    form_id = "your_form_id_here"
    
    try:
        # Get all records
        all_records_query = FulcrumQueryTemplates.get_all_records(form_id)
        print(f"📋 Query: {all_records_query}")
        
        # Execute query
        results = query_client.query_get(all_records_query, format="json")
        print(f"✅ Found {len(results.get('rows', []))} records")
        
        # Get records by status
        active_records_query = FulcrumQueryTemplates.get_records_by_status(form_id, "active")
        active_results = query_client.query_get(active_records_query, format="json")
        print(f"🟢 Found {len(active_results.get('rows', []))} active records")
        
        # Get records as DataFrame
        df = query_client.query_to_dataframe(all_records_query)
        print(f"📊 DataFrame shape: {df.shape}")
        
        # Advanced query example
        photo_count_query = AdvancedFulcrumQueries.get_records_with_photo_count(form_id)
        photo_results = query_client.query_get(photo_count_query, format="json")
        print(f"📸 Photo count query executed successfully")
        
    except Exception as e:
        print(f"❌ Query failed: {e}")

def export_to_csv_example():
    """Example of exporting query results to CSV"""
    
    api_token = "your_api_token_here"
    query_client = FulcrumQueryAPI(api_token)
    form_id = "your_form_id_here"
    
    try:
        # Get records by status
        query = FulcrumQueryTemplates.get_records_by_status(form_id, "active")
        
        # Export to CSV
        csv_data = query_client.query_get(query, format="csv")
        
        # Save to file
        with open("active_records.csv", "w") as f:
            f.write(csv_data)
        
        print("✅ CSV export completed successfully")
        
    except Exception as e:
        print(f"❌ CSV export failed: {e}")

if __name__ == "__main__":
    example_usage()
    export_to_csv_example()
