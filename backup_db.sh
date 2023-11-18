#!/bin/sh
#Move to /etc/cron.weekly
#chow 775 /etc/cron.weekly/backup_db.sh

now="$(date +'%d_%m_%Y_%H_%M_%S')"
filename="db_backup_$now".gz
backupfolder="/home/daniel/PiClima/MariaDB_Backups"
fullpathbackupfile="$backupfolder/$filename"
logfile="$backupfolder/log/"backup_log_"$(date +'%Y_%m')".txt
echo "mysqldump started at $(date +'%d-%m-%Y %H:%M:%S')" >> "$logfile"
mysqldump --user=dg --password=dg123 --default-character-set=utf8 tempodg | gzip > "$fullpathbackupfile"
echo "mysqldump finished at $(date +'%d-%m-%Y %H:%M:%S')" >> "$logfile"
chown daniel "$fullpathbackupfile"
chown daniel "$logfile"
echo "file permission changed" >> "$logfile"
find "$backupfolder" -name db_backup_* -mtime +8 -exec rm {} \;
echo "old files deleted" >> "$logfile"
echo "operation finished at $(date +'%d-%m-%Y %H:%M:%S')" >> "$logfile"
echo "*****************" >> "$logfile"
exit 0

