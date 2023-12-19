#!/bin/sh
#Move to /etc/cron.weekly
#chow 775 /etc/cron.weekly/backup_db.sh

myuser=MYUSER
deleteprevious=+15
dbUser=DBUSER
dbPass=DBPASS
dbDatabase=tempodg
now="$(date +'%d_%m_%Y_%H_%M_%S')"
filename="db_backup_$now".gz
backupfolder="/home/daniel/PiClima/MariaDB_Backups"
fullpathbackupfile="$backupfolder/$filename"
logfile="$backupfolder/log/"backup_log_"$(date +'%Y_%m')".txt

echo "mysqldump started at $(date +'%d-%m-%Y %H:%M:%S')" >> "$logfile"
mysqldump --user=$dbUser --password=$dbPass --default-character-set=utf8 $dbDatabase | gzip > "$fullpathbackupfile"
echo "mysqldump finished at $(date +'%d-%m-%Y %H:%M:%S')" >> "$logfile"
chown $myuser "$fullpathbackupfile"
chown $myuser "$logfile"
echo "file permission changed" >> "$logfile"
find "$backupfolder" -name db_backup_* -mtime $deleteprevious -exec rm {} \;
echo "old files deleted" >> "$logfile"
echo "operation finished at $(date +'%d-%m-%Y %H:%M:%S')" >> "$logfile"
echo "*****************" >> "$logfile"
exit 0

