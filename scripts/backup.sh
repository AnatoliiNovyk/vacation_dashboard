#!/bin/bash

# Скрипт для резервного копіювання бази даних
# Використання: ./backup.sh

BACKUP_DIR="/app/backups"
DB_PATH="/app/data/vacations.db"
DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_FILE="$BACKUP_DIR/vacations_backup_$DATE.db"

# Створення директорії для бекапів
mkdir -p $BACKUP_DIR

# Створення бекапу
if [ -f "$DB_PATH" ]; then
    cp "$DB_PATH" "$BACKUP_FILE"
    echo "Backup created: $BACKUP_FILE"
    
    # Видалення старих бекапів (старше 30 днів)
    find $BACKUP_DIR -name "vacations_backup_*.db" -mtime +30 -delete
    echo "Old backups cleaned up"
else
    echo "Database file not found: $DB_PATH"
    exit 1
fi