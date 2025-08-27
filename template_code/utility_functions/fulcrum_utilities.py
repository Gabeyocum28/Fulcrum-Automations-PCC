#!/usr/bin/env python3
"""
Fulcrum Utility Functions
Common utility functions for Fulcrum development
"""

import json
import csv
import os
from pathlib import Path
from typing import Dict, List, Optional, Union, Any
from datetime import datetime, timedelta
import logging
import hashlib
import re

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class FulcrumUtilities:
    """
    Utility functions for Fulcrum development
    """
    
    @staticmethod
    def validate_api_token(token: str) -> bool:
        """
        Basic validation of API token format
        
        Args:
            token: API token to validate
            
        Returns:
            True if token appears valid
        """
        if not token:
            return False
        
        # Fulcrum tokens are typically long alphanumeric strings
        if len(token) < 20:
            return False
        
        # Check if it contains only valid characters
        valid_chars = re.match(r'^[a-zA-Z0-9\-_]+$', token)
        return valid_chars is not None
    
    @staticmethod
    def sanitize_filename(filename: str) -> str:
        """
        Sanitize filename for safe file operations
        
        Args:
            filename: Original filename
            
        Returns:
            Sanitized filename
        """
        # Remove or replace invalid characters
        invalid_chars = '<>:"/\\|?*'
        for char in invalid_chars:
            filename = filename.replace(char, '_')
        
        # Remove leading/trailing spaces and dots
        filename = filename.strip(' .')
        
        # Limit length
        if len(filename) > 200:
            filename = filename[:200]
        
        return filename
    
    @staticmethod
    def create_backup_filename(original_name: str, extension: str = "") -> str:
        """
        Create a backup filename with timestamp
        
        Args:
            original_name: Original filename
            extension: File extension
            
        Returns:
            Backup filename with timestamp
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        if extension and not extension.startswith('.'):
            extension = f".{extension}"
        
        return f"{original_name}_backup_{timestamp}{extension}"
    
    @staticmethod
    def parse_fulcrum_date(date_string: str) -> Optional[datetime]:
        """
        Parse Fulcrum date string to datetime object
        
        Args:
            date_string: Date string from Fulcrum API
            
        Returns:
            Parsed datetime object or None
        """
        if not date_string:
            return None
        
        try:
            # Fulcrum dates are typically ISO 8601 format
            return datetime.fromisoformat(date_string.replace('Z', '+00:00'))
        except ValueError:
            try:
                # Try parsing as timestamp
                timestamp = float(date_string) / 1000  # Convert from milliseconds
                return datetime.fromtimestamp(timestamp)
            except (ValueError, OSError):
                logger.warning(f"Could not parse date: {date_string}")
                return None
    
    @staticmethod
    def format_fulcrum_date(dt: datetime) -> str:
        """
        Format datetime to Fulcrum-compatible string
        
        Args:
            dt: Datetime object
            
        Returns:
            Formatted date string
        """
        return dt.isoformat() + 'Z'
    
    @staticmethod
    def extract_form_values(record: Dict) -> Dict:
        """
        Extract form values from a Fulcrum record
        
        Args:
            record: Fulcrum record dictionary
            
        Returns:
            Extracted form values
        """
        if 'form_values' in record:
            return record['form_values']
        elif 'record' in record and 'form_values' in record['record']:
            return record['record']['form_values']
        else:
            return {}
    
    @staticmethod
    def flatten_nested_dict(data: Dict, parent_key: str = '', sep: str = '_') -> Dict:
        """
        Flatten nested dictionary structure
        
        Args:
            data: Nested dictionary
            parent_key: Parent key for nested items
            sep: Separator for nested keys
            
        Returns:
            Flattened dictionary
        """
        items = []
        for k, v in data.items():
            new_key = f"{parent_key}{sep}{k}" if parent_key else k
            if isinstance(v, dict):
                items.extend(flatten_nested_dict(v, new_key, sep=sep).items())
            elif isinstance(v, list):
                # Handle lists by creating indexed keys
                for i, item in enumerate(v):
                    if isinstance(item, dict):
                        items.extend(flatten_nested_dict(item, f"{new_key}_{i}", sep=sep).items())
                    else:
                        items.append((f"{new_key}_{i}", item))
            else:
                items.append((new_key, v))
        return dict(items)
    
    @staticmethod
    def calculate_record_hash(record: Dict) -> str:
        """
        Calculate hash for a record to detect changes
        
        Args:
            record: Record dictionary
            
        Returns:
            MD5 hash string
        """
        # Create a stable representation of the record
        record_str = json.dumps(record, sort_keys=True, default=str)
        return hashlib.md5(record_str.encode()).hexdigest()
    
    @staticmethod
    def merge_records(records: List[Dict], merge_key: str = 'id') -> List[Dict]:
        """
        Merge records with the same key, keeping the most recent
        
        Args:
            records: List of records
            merge_key: Key to use for merging
            
        Returns:
            Merged records list
        """
        merged = {}
        
        for record in records:
            key = record.get(merge_key)
            if not key:
                continue
            
            if key not in merged:
                merged[key] = record
            else:
                # Keep the most recent record
                current_updated = merged[key].get('_updated_at', '')
                new_updated = record.get('_updated_at', '')
                
                if new_updated > current_updated:
                    merged[key] = record
        
        return list(merged.values())
    
    @staticmethod
    def filter_records_by_field(records: List[Dict], field: str, value: Any, operator: str = '==') -> List[Dict]:
        """
        Filter records by field value with different operators
        
        Args:
            records: List of records
            field: Field name to filter on
            value: Value to compare against
            operator: Comparison operator ('==', '!=', '>', '<', '>=', '<=', 'in', 'contains')
            
        Returns:
            Filtered records list
        """
        filtered = []
        
        for record in records:
            record_value = record.get(field)
            
            if operator == '==':
                if record_value == value:
                    filtered.append(record)
            elif operator == '!=':
                if record_value != value:
                    filtered.append(record)
            elif operator == '>':
                if record_value > value:
                    filtered.append(record)
            elif operator == '<':
                if record_value < value:
                    filtered.append(record)
            elif operator == '>=':
                if record_value >= value:
                    filtered.append(record)
            elif operator == '<=':
                if record_value <= value:
                    filtered.append(record)
            elif operator == 'in':
                if record_value in value:
                    filtered.append(record)
            elif operator == 'contains':
                if isinstance(record_value, str) and value in record_value:
                    filtered.append(record)
            elif operator == 'not_contains':
                if isinstance(record_value, str) and value not in record_value:
                    filtered.append(record)
        
        return filtered
    
    @staticmethod
    def sort_records(records: List[Dict], sort_key: str, reverse: bool = False) -> List[Dict]:
        """
        Sort records by a specific key
        
        Args:
            records: List of records
            sort_key: Key to sort by
            reverse: Sort in reverse order
            
        Returns:
            Sorted records list
        """
        def get_sort_value(record):
            value = record.get(sort_key)
            if isinstance(value, str):
                return value.lower()
            return value
        
        return sorted(records, key=get_sort_value, reverse=reverse)
    
    @staticmethod
    def paginate_records(records: List[Dict], page_size: int = 100) -> List[List[Dict]]:
        """
        Split records into pages
        
        Args:
            records: List of records
            page_size: Number of records per page
            
        Returns:
            List of record pages
        """
        pages = []
        for i in range(0, len(records), page_size):
            pages.append(records[i:i + page_size])
        return pages
    
    @staticmethod
    def export_records_to_csv(records: List[Dict], filename: str, field_mapping: Optional[Dict] = None) -> str:
        """
        Export records to CSV file
        
        Args:
            records: List of records
            filename: Output filename
            field_mapping: Optional field name mapping
            
        Returns:
            Path to exported file
        """
        if not records:
            logger.warning("No records to export")
            return ""
        
        try:
            # Get all unique field names
            all_fields = set()
            for record in records:
                all_fields.update(record.keys())
            
            # Apply field mapping if provided
            if field_mapping:
                all_fields = {field_mapping.get(field, field) for field in all_fields}
            
            # Sort fields for consistent output
            sorted_fields = sorted(all_fields)
            
            # Write CSV
            with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=sorted_fields)
                writer.writeheader()
                
                for record in records:
                    # Map field names if mapping provided
                    if field_mapping:
                        mapped_record = {}
                        for key, value in record.items():
                            mapped_key = field_mapping.get(key, key)
                            mapped_record[mapped_key] = value
                        writer.writerow(mapped_record)
                    else:
                        writer.writerow(record)
            
            logger.info(f"✅ Exported {len(records)} records to {filename}")
            return filename
            
        except Exception as e:
            logger.error(f"❌ CSV export failed: {e}")
            return ""
    
    @staticmethod
    def create_field_mapping(records: List[Dict], custom_names: Optional[Dict] = None) -> Dict[str, str]:
        """
        Create a field mapping for export
        
        Args:
            records: List of records
            custom_names: Custom field name mappings
            
        Returns:
            Field mapping dictionary
        """
        if not records:
            return {}
        
        # Get all field names
        all_fields = set()
        for record in records:
            all_fields.update(record.keys())
        
        # Create default mapping
        mapping = {}
        for field in all_fields:
            # Remove common prefixes
            clean_name = field
            if field.startswith('_'):
                clean_name = field[1:]  # Remove leading underscore
            
            # Apply custom names if provided
            if custom_names and field in custom_names:
                clean_name = custom_names[field]
            
            mapping[field] = clean_name
        
        return mapping
    
    @staticmethod
    def validate_record_structure(record: Dict, required_fields: List[str]) -> Dict[str, Any]:
        """
        Validate record structure and return validation results
        
        Args:
            record: Record to validate
            required_fields: List of required field names
            
        Returns:
            Validation results dictionary
        """
        results = {
            'is_valid': True,
            'missing_fields': [],
            'empty_fields': [],
            'field_types': {},
            'warnings': []
        }
        
        # Check required fields
        for field in required_fields:
            if field not in record:
                results['missing_fields'].append(field)
                results['is_valid'] = False
            elif record[field] is None or record[field] == '':
                results['empty_fields'].append(field)
        
        # Check field types
        for field, value in record.items():
            if value is not None:
                results['field_types'][field] = type(value).__name__
        
        # Add warnings for empty required fields
        if results['empty_fields']:
            results['warnings'].append(f"Empty required fields: {', '.join(results['empty_fields'])}")
        
        return results
    
    @staticmethod
    def create_record_summary(records: List[Dict]) -> Dict[str, Any]:
        """
        Create a summary of records
        
        Args:
            records: List of records
            
        Returns:
            Summary dictionary
        """
        if not records:
            return {'total_records': 0}
        
        summary = {
            'total_records': len(records),
            'field_count': len(records[0]) if records else 0,
            'field_names': list(records[0].keys()) if records else [],
            'date_range': {},
            'status_counts': {},
            'field_types': {}
        }
        
        # Analyze date range
        dates = []
        for record in records:
            if '_created_at' in record:
                date = FulcrumUtilities.parse_fulcrum_date(record['_created_at'])
                if date:
                    dates.append(date)
        
        if dates:
            summary['date_range'] = {
                'earliest': min(dates).isoformat(),
                'latest': max(dates).isoformat(),
                'span_days': (max(dates) - min(dates)).days
            }
        
        # Analyze status counts
        for record in records:
            status = record.get('_status', 'unknown')
            summary['status_counts'][status] = summary['status_counts'].get(status, 0) + 1
        
        # Analyze field types
        if records:
            for field, value in records[0].items():
                if value is not None:
                    summary['field_types'][field] = type(value).__name__
        
        return summary

# ============================================================================
# USAGE EXAMPLES
# ============================================================================

def example_usage():
    """Example usage of Fulcrum utilities"""
    
    # Sample records
    sample_records = [
        {
            'id': '1',
            'name': 'Property A',
            'status': 'active',
            '_created_at': '2024-01-01T10:00:00Z',
            '_status': 'active'
        },
        {
            'id': '2',
            'name': 'Property B',
            'status': 'inactive',
            '_created_at': '2024-01-02T11:00:00Z',
            '_status': 'inactive'
        }
    ]
    
    # Validate API token
    token = "sample_token_12345"
    is_valid = FulcrumUtilities.validate_api_token(token)
    print(f"Token valid: {is_valid}")
    
    # Parse dates
    date_str = "2024-01-01T10:00:00Z"
    parsed_date = FulcrumUtilities.parse_fulcrum_date(date_str)
    print(f"Parsed date: {parsed_date}")
    
    # Filter records
    active_records = FulcrumUtilities.filter_records_by_field(sample_records, 'status', 'active')
    print(f"Active records: {len(active_records)}")
    
    # Sort records
    sorted_records = FulcrumUtilities.sort_records(sample_records, 'name')
    print(f"Sorted by name: {[r['name'] for r in sorted_records]}")
    
    # Create summary
    summary = FulcrumUtilities.create_record_summary(sample_records)
    print(f"Summary: {summary}")
    
    # Export to CSV
    csv_file = FulcrumUtilities.export_records_to_csv(sample_records, 'sample_export.csv')
    print(f"CSV exported: {csv_file}")

if __name__ == "__main__":
    example_usage()
