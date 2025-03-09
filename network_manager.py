"""
AI CEO Management System - Network Manager
Provides enhanced network connectivity and data exchange capabilities
"""

import os
import json
import time
import threading
import socket
import requests
import random
from datetime import datetime

class NetworkManager:
    """
    Network connectivity manager for AI CEO system
    Handles network status checking and data exchange
    """
    
    def __init__(self, debug_mode=True):
        """Initialize the network manager"""
        self.debug_mode = debug_mode
        self.running = False
        self.thread = None
        self.status = "disconnected"
        self.connectivity_score = 0.0
        self.last_check_time = None
        self.ping_results = {}
        self.network_stats = {
            "api_connections": 0,
            "successful_requests": 0,
            "failed_requests": 0,
            "avg_latency": 0,
            "last_updated": datetime.now().isoformat()
        }
        
        # Test endpoints to check connectivity (common reliable services)
        self.test_endpoints = [
            {"name": "Google DNS", "host": "8.8.8.8", "port": 53, "type": "socket"},
            {"name": "Cloudflare DNS", "host": "1.1.1.1", "port": 53, "type": "socket"},
            {"name": "Google", "url": "https://www.google.com", "type": "http"},
            {"name": "Cloudflare", "url": "https://www.cloudflare.com", "type": "http"},
            {"name": "GitHub", "url": "https://api.github.com/zen", "type": "http"}
        ]
        
        # Initialize with a connectivity check
        self.check_connectivity()
    
    def check_connectivity(self):
        """
        Check internet connectivity using multiple methods
        Returns True if connected, False otherwise
        """
        # Reset results for each check
        self.ping_results = {}
        connection_success = 0
        total_tests = 0
        total_latency = 0
        
        # Check each endpoint
        for endpoint in self.test_endpoints:
            latency = None
            success = False
            
            try:
                if endpoint["type"] == "socket":
                    # Try to connect to socket (DNS servers)
                    start_time = time.time()
                    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    s.settimeout(2.0)
                    result = s.connect_ex((endpoint["host"], endpoint["port"]))
                    end_time = time.time()
                    s.close()
                    
                    if result == 0:
                        success = True
                        latency = (end_time - start_time) * 1000  # ms
                        
                elif endpoint["type"] == "http":
                    # Try HTTP request
                    start_time = time.time()
                    response = requests.get(endpoint["url"], timeout=3)
                    end_time = time.time()
                    
                    if response.status_code == 200:
                        success = True
                        latency = (end_time - start_time) * 1000  # ms
                
                total_tests += 1
                if success:
                    connection_success += 1
                    total_latency += latency
                    
                # Store result
                self.ping_results[endpoint["name"]] = {
                    "success": success,
                    "latency": latency if success else None
                }
                
            except Exception as e:
                self.ping_results[endpoint["name"]] = {
                    "success": False,
                    "error": str(e)
                }
        
        # Calculate connectivity score (0.0 to 1.0)
        if total_tests > 0:
            self.connectivity_score = connection_success / total_tests
        else:
            self.connectivity_score = 0.0
            
        # Update average latency
        if connection_success > 0:
            self.network_stats["avg_latency"] = total_latency / connection_success
        
        # Update status
        if self.connectivity_score >= 0.8:
            self.status = "excellent"
        elif self.connectivity_score >= 0.5:
            self.status = "good"
        elif self.connectivity_score > 0:
            self.status = "limited"
        else:
            self.status = "disconnected"
            
        self.last_check_time = datetime.now()
        self.network_stats["last_updated"] = self.last_check_time.isoformat()
        
        if self.debug_mode:
            print(f"[NETWORK] Connectivity check completed: {self.status} ({self.connectivity_score:.2f})")
            if self.connectivity_score > 0:
                print(f"[NETWORK] Average latency: {self.network_stats['avg_latency']:.2f} ms")
        
        return self.connectivity_score > 0
    
    def start_monitoring(self):
        """Start continuous network monitoring in a background thread"""
        if self.running:
            print("[NETWORK] Monitoring already running")
            return
        
        self.running = True
        self.thread = threading.Thread(target=self._monitoring_loop)
        self.thread.daemon = True
        self.thread.start()
        
        if self.debug_mode:
            print("[NETWORK] Continuous monitoring started")
    
    def stop_monitoring(self):
        """Stop network monitoring"""
        if not self.running:
            return
            
        self.running = False
        if self.thread:
            self.thread.join(timeout=2)
            
        if self.debug_mode:
            print("[NETWORK] Monitoring stopped")
    
    def _monitoring_loop(self):
        """Network monitoring loop executed in background"""
        check_interval = 30  # seconds between regular checks
        
        while self.running:
            try:
                # Check connectivity
                self.check_connectivity()
                
                # Simulate API calls occasionally
                if random.random() < 0.2 and self.connectivity_score > 0:
                    self._simulate_api_call()
                
                # Sleep until next check
                for _ in range(check_interval):
                    if not self.running:
                        break
                    time.sleep(1)
                    
            except Exception as e:
                print(f"[NETWORK] Error in monitoring loop: {str(e)}")
                time.sleep(5)
    
    def _simulate_api_call(self):
        """Simulate an API call to track statistics"""
        if self.connectivity_score <= 0:
            return
            
        # Decide if request will succeed based on connectivity
        success_chance = self.connectivity_score * 0.9
        success = random.random() < success_chance
        
        self.network_stats["api_connections"] += 1
        
        if success:
            self.network_stats["successful_requests"] += 1
        else:
            self.network_stats["failed_requests"] += 1
            
        if self.debug_mode and random.random() < 0.5:
            success_status = "successful" if success else "failed"
            print(f"[NETWORK] Simulated API call {success_status}")
    
    def get_network_status(self):
        """
        Get detailed network status information
        Returns a dictionary with network status details
        """
        # Refresh data if last check was more than 2 minutes ago
        if (self.last_check_time is None or 
                (datetime.now() - self.last_check_time).total_seconds() > 120):
            self.check_connectivity()
            
        status_data = {
            "status": self.status,
            "connectivity_score": round(self.connectivity_score, 2),
            "last_check": self.last_check_time.isoformat() if self.last_check_time else None,
            "endpoints": self.ping_results,
            "statistics": self.network_stats
        }
        
        return status_data
    
    def fetch_external_data(self, url, params=None, headers=None, timeout=5):
        """
        Fetch data from an external API
        
        Args:
            url (str): API endpoint URL
            params (dict, optional): Request parameters
            headers (dict, optional): Request headers
            timeout (int, optional): Request timeout in seconds
            
        Returns:
            dict: Response data (JSON) or None if request failed
        """
        if not self.connectivity_score > 0:
            print("[NETWORK] Cannot fetch data: No network connection")
            return None
            
        try:
            if self.debug_mode:
                print(f"[NETWORK] Fetching data from: {url}")
                
            response = requests.get(
                url, 
                params=params, 
                headers=headers, 
                timeout=timeout
            )
            
            # Check if request was successful
            if response.status_code == 200:
                self.network_stats["successful_requests"] += 1
                
                try:
                    # Try to parse as JSON
                    data = response.json()
                    return data
                except ValueError:
                    # Return text if not JSON
                    return {"text": response.text}
                    
            else:
                self.network_stats["failed_requests"] += 1
                if self.debug_mode:
                    print(f"[NETWORK] Request failed with status {response.status_code}")
                return None
                
        except Exception as e:
            self.network_stats["failed_requests"] += 1
            if self.debug_mode:
                print(f"[NETWORK] Error fetching data: {str(e)}")
            return None
    
    def post_data(self, url, data, headers=None, timeout=5):
        """
        Post data to an external API
        
        Args:
            url (str): API endpoint URL
            data (dict): Data to send
            headers (dict, optional): Request headers
            timeout (int, optional): Request timeout in seconds
            
        Returns:
            dict: Response data (JSON) or None if request failed
        """
        if not self.connectivity_score > 0:
            print("[NETWORK] Cannot post data: No network connection")
            return None
            
        try:
            if self.debug_mode:
                print(f"[NETWORK] Posting data to: {url}")
                
            if headers is None:
                headers = {'Content-Type': 'application/json'}
                
            response = requests.post(
                url, 
                json=data, 
                headers=headers, 
                timeout=timeout
            )
            
            # Check if request was successful
            if response.status_code in [200, 201, 202, 204]:
                self.network_stats["successful_requests"] += 1
                
                try:
                    # Try to parse as JSON
                    return response.json()
                except ValueError:
                    # Return text if not JSON
                    return {"status": "success", "text": response.text}
                    
            else:
                self.network_stats["failed_requests"] += 1
                if self.debug_mode:
                    print(f"[NETWORK] Request failed with status {response.status_code}")
                return None
                
        except Exception as e:
            self.network_stats["failed_requests"] += 1
            if self.debug_mode:
                print(f"[NETWORK] Error posting data: {str(e)}")
            return None


# Test function for network manager
def test_network_manager():
    """Run a test of the network manager"""
    print("\n======== Network Manager Test ========")
    print("Initializing network manager...")
    
    # Create the network manager
    network = NetworkManager(debug_mode=True)
    
    # Check connectivity
    print("\nChecking network connectivity...")
    connected = network.check_connectivity()
    
    print(f"Connected: {connected}")
    print(f"Status: {network.status}")
    print(f"Score: {network.connectivity_score:.2f}")
    
    if connected:
        print("\nEndpoint status:")
        for name, result in network.ping_results.items():
            status = "✓" if result["success"] else "✗"
            latency = f"{result['latency']:.2f} ms" if result["success"] else "N/A"
            print(f"  {name}: {status} ({latency})")
    
    # Start monitoring
    print("\nStarting network monitoring...")
    network.start_monitoring()
    
    try:
        # Let it run for a few seconds
        for i in range(3):
            print(f"\nMonitoring cycle {i+1}/3")
            time.sleep(3)
            
            # Get network status
            status = network.get_network_status()
            print(f"Current status: {status['status']}")
            
            # Try to fetch some external data
            if network.connectivity_score > 0 and i == 1:
                print("\nTesting external data fetch...")
                try:
                    data = network.fetch_external_data("https://api.github.com/zen")
                    if data:
                        print(f"Received data: {data}")
                except Exception as e:
                    print(f"Fetch error: {str(e)}")
        
    finally:
        # Stop monitoring
        network.stop_monitoring()
        
    print("\nNetwork statistics:")
    for key, value in network.network_stats.items():
        print(f"  {key}: {value}")
        
    print("\nNetwork manager test complete!")
    print("=====================================")


if __name__ == "__main__":
    # Run standalone test
    test_network_manager()