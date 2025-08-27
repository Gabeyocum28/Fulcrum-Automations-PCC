#!/usr/bin/env python3
"""
Fulcrum Data Processing Templates
Comprehensive data processing and transformation utilities for Fulcrum data
"""

import pandas as pd
import json
import csv
from pathlib import Path
from typing import Dict, List, Optional, Union, Any
import logging
from datetime import datetime, timedelta
import zipfile
import shutil

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class FulcrumDataProcessor:
    """
    Comprehensive data processing utilities for Fulcrum data
    """
    
    def __init__(self, output_directory: str = "processed_data"):
        """
        Initialize data processor
        
        Args:
            output_directory: Directory for processed data output
        """
        self.output_directory = Path(output_directory)
        self.output_directory.mkdir(exist_ok=True)
        
        # Create subdirectories
        (self.output_directory / "csv").mkdir(exist_ok=True)
        (self.output_directory / "json").mkdir(exist_ok=True)
        (self.output_directory / "excel").mkdir(exist_ok=True)
        (self.output_directory / "photos").mkdir(exist_ok=True)
        (self.output_directory / "reports").mkdir(exist_ok=True)
    
    def process_fulcrum_records(self, records: List[Dict], form_name: str) -> pd.DataFrame:
        """
        Process raw Fulcrum records into a clean DataFrame
        
        Args:
            records: List of Fulcrum record dictionaries
            form_name: Name of the form for identification
            
        Returns:
            Cleaned pandas DataFrame
        """
        if not records:
            logger.warning("No records to process")
            return pd.DataFrame()
        
        try:
            # Convert to DataFrame
            df = pd.DataFrame(records)
            
            # Extract form values
            if 'form_values' in df.columns:
                # Expand form_values into separate columns
                form_values_df = pd.json_normalize(df['form_values'])
                df = pd.concat([df.drop('form_values', axis=1), form_values_df], axis=1)
            
            # Clean up common Fulcrum fields
            df = self._clean_fulcrum_fields(df)
            
            # Add metadata
            df['_processed_at'] = datetime.now().isoformat()
            df['_form_name'] = form_name
            df['_record_count'] = len(df)
            
            logger.info(f"✅ Processed {len(df)} records from {form_name}")
            return df
            
        except Exception as e:
            logger.error(f"❌ Failed to process records: {e}")
            return pd.DataFrame()
    
    def _clean_fulcrum_fields(self, df: pd.DataFrame) -> pd.DataFrame:
        """Clean and standardize Fulcrum field names"""
        
        # Rename common Fulcrum fields
        field_mappings = {
            '_id': 'record_id',
            '_status': 'status',
            '_created_at': 'created_at',
            '_updated_at': 'updated_at',
            '_created_by': 'created_by',
            '_updated_by': 'updated_by',
            '_geometry': 'geometry',
            '_photos': 'photos',
            '_signatures': 'signatures',
            '_audio': 'audio',
            '_video': 'video',
            '_notes': 'notes'
        }
        
        df = df.rename(columns=field_mappings)
        
        # Convert timestamps
        timestamp_columns = ['created_at', 'updated_at']
        for col in timestamp_columns:
            if col in df.columns:
                df[col] = pd.to_datetime(df[col], errors='coerce')
        
        return df
    
    def filter_records_by_status(self, df: pd.DataFrame, status: str) -> pd.DataFrame:
        """Filter records by status"""
        if 'status' in df.columns:
            return df[df['status'] == status]
        return df
    
    def filter_records_by_date_range(self, df: pd.DataFrame, start_date: str, end_date: str) -> pd.DataFrame:
        """Filter records by date range"""
        if 'created_at' in df.columns:
            start = pd.to_datetime(start_date)
            end = pd.to_datetime(end_date)
            return df[(df['created_at'] >= start) & (df['created_at'] <= end)]
        return df
    
    def filter_records_by_field_value(self, df: pd.DataFrame, field_name: str, field_value: Any) -> pd.DataFrame:
        """Filter records by specific field value"""
        if field_name in df.columns:
            return df[df[field_name] == field_value]
        return df
    
    def export_to_csv(self, df: pd.DataFrame, filename: str, include_metadata: bool = True) -> str:
        """Export DataFrame to CSV"""
        try:
            output_path = self.output_directory / "csv" / f"{filename}.csv"
            
            # Add metadata if requested
            if include_metadata:
                metadata_df = pd.DataFrame({
                    'metadata': ['export_date', 'record_count', 'form_name'],
                    'value': [datetime.now().isoformat(), len(df), df.get('_form_name', 'Unknown').iloc[0] if len(df) > 0 else 'Unknown']
                })
                
                # Combine metadata with data
                combined_df = pd.concat([metadata_df, df], ignore_index=True)
            else:
                combined_df = df
            
            combined_df.to_csv(output_path, index=False)
            logger.info(f"✅ CSV exported to {output_path}")
            return str(output_path)
            
        except Exception as e:
            logger.error(f"❌ CSV export failed: {e}")
            return ""
    
    def export_to_json(self, df: pd.DataFrame, filename: str, include_metadata: bool = True) -> str:
        """Export DataFrame to JSON"""
        try:
            output_path = self.output_directory / "json" / f"{filename}.json"
            
            # Convert to records format
            records = df.to_dict('records')
            
            # Add metadata if requested
            if include_metadata:
                export_data = {
                    'metadata': {
                        'export_date': datetime.now().isoformat(),
                        'record_count': len(df),
                        'form_name': df.get('_form_name', 'Unknown').iloc[0] if len(df) > 0 else 'Unknown'
                    },
                    'records': records
                }
            else:
                export_data = records
            
            with open(output_path, 'w') as f:
                json.dump(export_data, f, indent=2, default=str)
            
            logger.info(f"✅ JSON exported to {output_path}")
            return str(output_path)
            
        except Exception as e:
            logger.error(f"❌ JSON export failed: {e}")
            return ""
    
    def export_to_excel(self, df: pd.DataFrame, filename: str, include_metadata: bool = True) -> str:
        """Export DataFrame to Excel"""
        try:
            output_path = self.output_directory / "excel" / f"{filename}.xlsx"
            
            with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
                # Export main data
                df.to_excel(writer, sheet_name='Data', index=False)
                
                # Export metadata if requested
                if include_metadata:
                    metadata_df = pd.DataFrame({
                        'Metadata': ['Export Date', 'Record Count', 'Form Name'],
                        'Value': [
                            datetime.now().isoformat(),
                            len(df),
                            df.get('_form_name', 'Unknown').iloc[0] if len(df) > 0 else 'Unknown'
                        ]
                    })
                    metadata_df.to_excel(writer, sheet_name='Metadata', index=False)
            
            logger.info(f"✅ Excel exported to {output_path}")
            return str(output_path)
            
        except Exception as e:
            logger.error(f"❌ Excel export failed: {e}")
            return ""
    
    def download_photos(self, df: pd.DataFrame, photo_field: str = 'photos') -> str:
        """Download photos from records"""
        try:
            photos_dir = self.output_directory / "photos"
            photos_dir.mkdir(exist_ok=True)
            
            photo_count = 0
            for idx, record in df.iterrows():
                if pd.notna(record.get(photo_field)) and record[photo_field]:
                    try:
                        photos = record[photo_field]
                        if isinstance(photos, str):
                            photos = json.loads(photos)
                        
                        if isinstance(photos, list):
                            for photo_idx, photo in enumerate(photos):
                                if isinstance(photo, dict) and 'url' in photo:
                                    photo_url = photo['url']
                                    photo_filename = f"record_{idx}_photo_{photo_idx}.jpg"
                                    photo_path = photos_dir / photo_filename
                                    
                                    # Download photo (placeholder - implement actual download)
                                    logger.info(f"📸 Would download photo: {photo_url} to {photo_path}")
                                    photo_count += 1
                    
                    except Exception as e:
                        logger.warning(f"Failed to process photos for record {idx}: {e}")
            
            logger.info(f"✅ Processed {photo_count} photos")
            return str(photos_dir)
            
        except Exception as e:
            logger.error(f"❌ Photo download failed: {e}")
            return ""
    
    def generate_summary_report(self, df: pd.DataFrame, form_name: str) -> str:
        """Generate a summary report of the data"""
        try:
            report_path = self.output_directory / "reports" / f"{form_name}_summary_report.txt"
            
            with open(report_path, 'w') as f:
                f.write(f"Fulcrum Data Summary Report\n")
                f.write(f"==========================\n\n")
                f.write(f"Form Name: {form_name}\n")
                f.write(f"Generated: {datetime.now().isoformat()}\n")
                f.write(f"Total Records: {len(df)}\n\n")
                
                # Status summary
                if 'status' in df.columns:
                    status_counts = df['status'].value_counts()
                    f.write("Status Summary:\n")
                    for status, count in status_counts.items():
                        f.write(f"  {status}: {count}\n")
                    f.write("\n")
                
                # Date range
                if 'created_at' in df.columns:
                    min_date = df['created_at'].min()
                    max_date = df['created_at'].max()
                    f.write(f"Date Range: {min_date} to {max_date}\n\n")
                
                # Field summary
                f.write("Field Summary:\n")
                for col in df.columns:
                    if col.startswith('_'):
                        continue
                    
                    non_null_count = df[col].notna().sum()
                    null_count = df[col].isna().sum()
                    f.write(f"  {col}: {non_null_count} non-null, {null_count} null\n")
                
                # Photo summary
                if 'photos' in df.columns:
                    photo_records = df['photos'].notna().sum()
                    f.write(f"\nRecords with Photos: {photo_records}\n")
                
                # Geometry summary
                if 'geometry' in df.columns:
                    geo_records = df['geometry'].notna().sum()
                    f.write(f"Records with Geometry: {geo_records}\n")
            
            logger.info(f"✅ Summary report generated: {report_path}")
            return str(report_path)
            
        except Exception as e:
            logger.error(f"❌ Report generation failed: {e}")
            return ""
    
    def create_data_package(self, df: pd.DataFrame, form_name: str, include_photos: bool = False) -> str:
        """Create a complete data package with all exports"""
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            package_name = f"{form_name}_data_package_{timestamp}"
            package_path = self.output_directory / package_name
            package_path.mkdir(exist_ok=True)
            
            # Export to all formats
            csv_path = self.export_to_csv(df, f"{form_name}_data", True)
            json_path = self.export_to_json(df, f"{form_name}_data", True)
            excel_path = self.export_to_excel(df, f"{form_name}_data", True)
            
            # Generate report
            report_path = self.generate_summary_report(df, form_name)
            
            # Download photos if requested
            if include_photos:
                photos_dir = self.download_photos(df)
                if photos_dir:
                    # Copy photos to package
                    package_photos_dir = package_path / "photos"
                    if Path(photos_dir).exists():
                        shutil.copytree(photos_dir, package_photos_dir, dirs_exist_ok=True)
            
            # Create package info file
            package_info = {
                'package_name': package_name,
                'created_at': datetime.now().isoformat(),
                'form_name': form_name,
                'record_count': len(df),
                'exports': {
                    'csv': csv_path,
                    'json': json_path,
                    'excel': excel_path,
                    'report': report_path
                },
                'includes_photos': include_photos
            }
            
            with open(package_path / "package_info.json", 'w') as f:
                json.dump(package_info, f, indent=2, default=str)
            
            # Create ZIP archive
            zip_path = self.output_directory / f"{package_name}.zip"
            with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                for file_path in package_path.rglob('*'):
                    if file_path.is_file():
                        zipf.write(file_path, file_path.relative_to(package_path))
            
            # Clean up temporary package directory
            shutil.rmtree(package_path)
            
            logger.info(f"✅ Data package created: {zip_path}")
            return str(zip_path)
            
        except Exception as e:
            logger.error(f"❌ Data package creation failed: {e}")
            return ""

# ============================================================================
# USAGE EXAMPLES
# ============================================================================

def example_usage():
    """Example usage of the Fulcrum Data Processor"""
    
    # Initialize processor
    processor = FulcrumDataProcessor("example_output")
    
    # Example data (replace with actual Fulcrum data)
    sample_records = [
        {
            "id": "1",
            "form_values": {"name": "Property A", "status": "active", "priority": "high"},
            "_status": "active",
            "_created_at": "2024-01-01T10:00:00Z",
            "_photos": '[{"url": "https://example.com/photo1.jpg"}]'
        },
        {
            "id": "2", 
            "form_values": {"name": "Property B", "status": "inactive", "priority": "medium"},
            "_status": "inactive",
            "_created_at": "2024-01-02T11:00:00Z",
            "_photos": None
        }
    ]
    
    # Process records
    df = processor.process_fulcrum_records(sample_records, "Property Survey")
    
    # Filter active records
    active_df = processor.filter_records_by_status(df, "active")
    
    # Export to different formats
    csv_path = processor.export_to_csv(df, "property_survey_data")
    json_path = processor.export_to_json(df, "property_survey_data")
    excel_path = processor.export_to_excel(df, "property_survey_data")
    
    # Generate report
    report_path = processor.generate_summary_report(df, "Property Survey")
    
    # Create complete data package
    package_path = processor.create_data_package(df, "Property Survey", include_photos=False)
    
    print(f"✅ Processing complete!")
    print(f"📊 Records processed: {len(df)}")
    print(f"📁 Output directory: {processor.output_directory}")

if __name__ == "__main__":
    example_usage()
