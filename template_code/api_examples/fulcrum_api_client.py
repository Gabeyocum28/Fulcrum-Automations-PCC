#!/usr/bin/env python3
"""
Fulcrum API Client Template
Based on official fulcrum-python library: https://github.com/fulcrumapp/fulcrum-python
Comprehensive template for all Fulcrum API operations
"""

import requests
import json
import time
from pathlib import Path
from typing import Dict, List, Optional, Union
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class FulcrumAPIClient:
    """
    Comprehensive Fulcrum API Client
    Supports all major Fulcrum API endpoints and operations
    """
    
    def __init__(self, api_token: str, base_url: str = "https://api.fulcrumapp.com/api/v2"):
        """
        Initialize Fulcrum API Client
        
        Args:
            api_token: Your Fulcrum API token
            base_url: Fulcrum API base URL (default: v2 API)
        """
        self.api_token = api_token
        self.base_url = base_url
        self.headers = {
            "X-ApiToken": api_token,
            "Content-Type": "application/json"
        }
        self.session = requests.Session()
        self.session.headers.update(self.headers)
        
        # Rate limiting
        self.rate_limit_delay = 0.1  # 100ms between requests
        self.last_request_time = 0
    
    def _rate_limit(self):
        """Implement basic rate limiting"""
        current_time = time.time()
        time_since_last = current_time - self.last_request_time
        if time_since_last < self.rate_limit_delay:
            time.sleep(self.rate_limit_delay - time_since_last)
        self.last_request_time = time.time()
    
    def _make_request(self, method: str, endpoint: str, **kwargs) -> Dict:
        """
        Make HTTP request to Fulcrum API
        
        Args:
            method: HTTP method (GET, POST, PUT, DELETE)
            endpoint: API endpoint
            **kwargs: Additional request parameters
            
        Returns:
            API response as dictionary
        """
        self._rate_limit()
        
        url = f"{self.base_url}/{endpoint}"
        
        try:
            response = self.session.request(method, url, **kwargs)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"API request failed: {e}")
            raise
    
    # ============================================================================
    # FORMS API METHODS
    # ============================================================================
    
    def get_forms(self, form_filter: str = "all", **params) -> List[Dict]:
        """
        Get forms from Fulcrum
        
        Args:
            form_filter: Filter forms by status ('all', 'active', 'inactive')
            **params: Additional query parameters
            
        Returns:
            List of forms
        """
        endpoint = "forms"
        if form_filter != "all":
            params['status'] = form_filter
        
        response = self._make_request("GET", endpoint, params=params)
        return response.get("forms", [])
    
    def get_form(self, form_id: str) -> Dict:
        """
        Get a specific form by ID
        
        Args:
            form_id: Form UUID
            
        Returns:
            Form data
        """
        endpoint = f"forms/{form_id}"
        return self._make_request("GET", endpoint)
    
    def create_form(self, form_data: Dict) -> Dict:
        """
        Create a new form
        
        Args:
            form_data: Form configuration data
            
        Returns:
            Created form data
        """
        endpoint = "forms"
        return self._make_request("POST", endpoint, json=form_data)
    
    def update_form(self, form_id: str, form_data: Dict) -> Dict:
        """
        Update an existing form
        
        Args:
            form_id: Form UUID
            form_data: Updated form data
            
        Returns:
            Updated form data
        """
        endpoint = f"forms/{form_id}"
        return self._make_request("PUT", endpoint, json=form_data)
    
    def delete_form(self, form_id: str) -> bool:
        """
        Delete a form
        
        Args:
            form_id: Form UUID
            
        Returns:
            True if successful
        """
        endpoint = f"forms/{form_id}"
        self._make_request("DELETE", endpoint)
        return True
    
    # ============================================================================
    # RECORDS API METHODS
    # ============================================================================
    
    def get_records(self, form_id: str, **params) -> List[Dict]:
        """
        Get records from a form
        
        Args:
            form_id: Form UUID
            **params: Query parameters (status, created_at, updated_at, etc.)
            
        Returns:
            List of records
        """
        endpoint = "records"
        params['form_id'] = form_id
        response = self._make_request("GET", endpoint, params=params)
        return response.get("records", [])
    
    def get_record(self, record_id: str) -> Dict:
        """
        Get a specific record by ID
        
        Args:
            record_id: Record UUID
            
        Returns:
            Record data
        """
        endpoint = f"records/{record_id}"
        return self._make_request("GET", endpoint)
    
    def create_record(self, record_data: Dict) -> Dict:
        """
        Create a new record
        
        Args:
            record_data: Record data with form_values
            
        Returns:
            Created record data
        """
        endpoint = "records"
        return self._make_request("POST", endpoint, json=record_data)
    
    def update_record(self, record_id: str, record_data: Dict) -> Dict:
        """
        Update an existing record
        
        Args:
            record_id: Record UUID
            record_data: Updated record data
            
        Returns:
            Updated record data
        """
        endpoint = f"records/{record_id}"
        return self._make_request("PUT", endpoint, json=record_data)
    
    def delete_record(self, record_id: str) -> bool:
        """
        Delete a record
        
        Args:
            record_id: Record UUID
            
        Returns:
            True if successful
        """
        endpoint = f"records/{record_id}"
        self._make_request("DELETE", endpoint)
        return True
    
    # ============================================================================
    # CLASSIFICATION SETS API METHODS
    # ============================================================================
    
    def get_classification_sets(self) -> List[Dict]:
        """
        Get all classification sets
        
        Returns:
            List of classification sets
        """
        endpoint = "classification_sets"
        response = self._make_request("GET", endpoint)
        return response.get("classification_sets", [])
    
    def get_classification_set(self, set_id: str) -> Dict:
        """
        Get a specific classification set
        
        Args:
            set_id: Classification set UUID
            
        Returns:
            Classification set data
        """
        endpoint = f"classification_sets/{set_id}"
        return self._make_request("GET", endpoint)
    
    # ============================================================================
    # PHOTOS API METHODS
    # ============================================================================
    
    def get_photos(self, **params) -> List[Dict]:
        """
        Get photos
        
        Args:
            **params: Query parameters
            
        Returns:
            List of photos
        """
        endpoint = "photos"
        response = self._make_request("GET", endpoint, params=params)
        return response.get("photos", [])
    
    def get_photo(self, photo_id: str) -> Dict:
        """
        Get a specific photo
        
        Args:
            photo_id: Photo UUID
            
        Returns:
            Photo data
        """
        endpoint = f"photos/{photo_id}"
        return self._make_request("GET", endpoint)
    
    def download_photo(self, photo_id: str, size: str = "original") -> bytes:
        """
        Download photo media
        
        Args:
            photo_id: Photo UUID
            size: Photo size ('original', 'thumbnail', 'large')
            
        Returns:
            Photo binary data
        """
        endpoint = f"photos/{photo_id}/media"
        params = {'size': size}
        response = self.session.get(f"{self.base_url}/{endpoint}", params=params)
        response.raise_for_status()
        return response.content
    
    def upload_photo(self, file_path: str, **params) -> Dict:
        """
        Upload a photo
        
        Args:
            file_path: Path to photo file
            **params: Additional parameters
            
        Returns:
            Uploaded photo data
        """
        endpoint = "photos"
        
        with open(file_path, 'rb') as f:
            files = {'file': f}
            response = self.session.post(f"{self.base_url}/{endpoint}", files=files, data=params)
            response.raise_for_status()
            return response.json()
    
    # ============================================================================
    # PROJECTS API METHODS
    # ============================================================================
    
    def get_projects(self, **params) -> List[Dict]:
        """
        Get projects
        
        Args:
            **params: Query parameters
            
        Returns:
            List of projects
        """
        endpoint = "projects"
        response = self._make_request("GET", endpoint, params=params)
        return response.get("projects", [])
    
    def get_project(self, project_id: str) -> Dict:
        """
        Get a specific project
        
        Args:
            project_id: Project UUID
            
        Returns:
            Project data
        """
        endpoint = f"projects/{project_id}"
        return self._make_request("GET", endpoint)
    
    # ============================================================================
    # CHANGESETS API METHODS
    # ============================================================================
    
    def get_changesets(self, **params) -> List[Dict]:
        """
        Get changesets
        
        Args:
            **params: Query parameters
            
        Returns:
            List of changesets
        """
        endpoint = "changesets"
        response = self._make_request("GET", endpoint, params=params)
        return response.get("changesets", [])
    
    def get_changeset(self, changeset_id: str) -> Dict:
        """
        Get a specific changeset
        
        Args:
            changeset_id: Changeset UUID
            
        Returns:
            Changeset data
        """
        endpoint = f"changesets/{changeset_id}"
        return self._make_request("GET", endpoint)
    
    def close_changeset(self, changeset_id: str) -> Dict:
        """
        Close a changeset
        
        Args:
            changeset_id: Changeset UUID
            
        Returns:
            Closed changeset data
        """
        endpoint = f"changesets/{changeset_id}/close"
        return self._make_request("POST", endpoint)
    
    # ============================================================================
    # UTILITY METHODS
    # ============================================================================
    
    def test_connection(self) -> bool:
        """
        Test API connection
        
        Returns:
            True if connection successful
        """
        try:
            response = self._make_request("GET", "forms")
            return True
        except Exception as e:
            logger.error(f"Connection test failed: {e}")
            return False
    
    def get_account_info(self) -> Dict:
        """
        Get account information
        
        Returns:
            Account data
        """
        endpoint = "account"
        return self._make_request("GET", endpoint)
    
    def get_api_limits(self) -> Dict:
        """
        Get API rate limit information
        
        Returns:
            Rate limit data
        """
        # Note: Fulcrum may not expose this endpoint
        # This is a placeholder for future implementation
        return {"rate_limit": "Not implemented", "remaining": "Unknown"}

# ============================================================================
# USAGE EXAMPLES
# ============================================================================

def example_usage():
    """Example usage of the Fulcrum API Client"""
    
    # Initialize client
    api_token = "your_api_token_here"
    client = FulcrumAPIClient(api_token)
    
    # Test connection
    if client.test_connection():
        print("✅ Connected to Fulcrum API")
        
        # Get all forms
        forms = client.get_forms()
        print(f"📋 Found {len(forms)} forms")
        
        # Get active forms only
        active_forms = client.get_forms("active")
        print(f"🟢 Found {len(active_forms)} active forms")
        
        # Get a specific form
        if forms:
            form = client.get_form(forms[0]['id'])
            print(f"📝 Form: {form['form']['name']}")
        
        # Get classification sets
        classification_sets = client.get_classification_sets()
        print(f"🏷️ Found {len(classification_sets)} classification sets")
        
        # Get account info
        account = client.get_account_info()
        print(f"👤 Account: {account.get('account', {}).get('name', 'Unknown')}")
        
    else:
        print("❌ Failed to connect to Fulcrum API")

if __name__ == "__main__":
    example_usage()
