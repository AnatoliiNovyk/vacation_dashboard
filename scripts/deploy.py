#!/usr/bin/env python3
"""
Скрипт для розгортання Python додатку
"""

import os
import sys
import subprocess
import logging

def setup_logging():
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )
    return logging.getLogger(__name__)

def run_command(command, logger):
    """Виконання команди з логуванням"""
    logger.info(f"Executing: {command}")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        logger.info(f"Success: {result.stdout}")
        return True
    except subprocess.CalledProcessError as e:
        logger.error(f"Error: {e.stderr}")
        return False

def main():
    logger = setup_logging()
    logger.info("Starting Python application deployment")
    
    # Перевірка Python залежностей
    if not run_command("pip install -r requirements.txt", logger):
        logger.error("Failed to install Python dependencies")
        sys.exit(1)
    
    # Перевірка структури бази даних
    if not run_command("python -c 'from data.db_operations import _init_db; _init_db()'", logger):
        logger.error("Failed to initialize database")
        sys.exit(1)
    
    # Запуск health check
    if not run_command("python scripts/health_check.py", logger):
        logger.warning("Health check failed, but continuing deployment")
    
    logger.info("Deployment completed successfully")

if __name__ == "__main__":
    main()