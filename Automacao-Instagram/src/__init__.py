"""
Instagram Automation - Source Package
Version: 1.0.0
"""

__version__ = "1.0.0"
__author__ = "Claude AI"

from src.api.instagram_publisher import InstagramPublisher
from src.scheduler.scheduler_manager import SchedulerManager
from src.utils.config_manager import ConfigManager

__all__ = [
    "InstagramPublisher",
    "SchedulerManager",
    "ConfigManager"
]