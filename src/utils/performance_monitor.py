import time
from contextlib import contextmanager
from .logger import Logger

class PerformanceMonitor:
    def __init__(self):
        self.logger = Logger(__name__)
        self.metrics = {}
        
    @contextmanager
    def measure_time(self, operation_name):
        """Context manager to measure execution time"""
        start_time = time.time()
        try:
            yield
        finally:
            execution_time = time.time() - start_time
            self.metrics[operation_name] = execution_time
            self.logger.debug(f"{operation_name} took {execution_time:.2f} seconds")
            
    def get_metrics(self):
        """Return all collected metrics"""
        return self.metrics
        
    def generate_report(self):
        """Generate performance report"""
        report = ["Performance Report:"]
        total_time = 0
        
        for operation, duration in self.metrics.items():
            report.append(f"- {operation}: {duration:.2f}s")
            total_time += duration
            
        report.append(f"\nTotal execution time: {total_time:.2f}s")
        return "\n".join(report) 