# PostgreSQL Backups

The ansible deployment configuration enables automatically making backups of the PostgreSQL data.

# Types of backups

* SQL Dump: the pg_dumpall command is used to extract a PostgreSQL database cluster into a script file. This command generates a file with SQL commands that, when fed back to the server, it will recreate the database in the same state as it was at the time of the dump. This file can later used to restore the database as it was when the backup was created.

* Continuous archiving base backup: combining a file-system-level backup with backup of the Write Ahead Log files, we can restore the database restoring the file-system-level backup and replaying the WAL files. This allows us to restore the database to its state at any time since the base backup was taken. The file-system-level backup is the base backup.

* Continuous archiving WAL files: a running PostgreSQL system produces an indefinitely long sequence of WAL records. The system physically divides this sequence into WAL segment files, which are normally 16MB apiece.

# Backup Ansible Configuration

Backups are stored on /var/postgres_backups or where the config.yml variable config.postgres_backups.folder points to. SQL dump files are on /var/postgres_backups/dump, base backups are on /var/postgres_backups/base and WAL files are on /var/postgres_backups/wal

In the backup system that deployment-tool installs, a SQL dump and a base backup are done daily (or with the frequency that you configure with config.postgres_backups.base_backups). For that, a cron task is configured to call /usr/bin/create_backup_postgres.sh. That script calls pg_dumpall to create the SQL dump file and pg_basebackup to create the continuous archiving base backup, so two different types of backup are created. It also calls /usr/bin/clean_old_postgres_backups.sh script, which will clean base, dump and wal backups that are older than the parameter configured in config.postgres_backups.base_backups.keep_days. Also, at least every ten minutes (configured in config.postgres_backups.archive_timeout) a new WAL file is created. All backups are compressed in order to minimize the space used.

The name of the base and dump backups is the date up to the second when the backup was created. For example, base backup files use this format: /var/postgres_backups/day_month_year_hour_min_sec/base.tar.gz and dump backups use this format: /var/postgres_backups/dump_day_month_year_hour_min_sec.gz

PostgreSQL backup archiving can be completely stopped configuring config.postgres_backups.enabled to false. This won't delete any previous backups. Beware that if you stop making backups and after some time you activate the backup system again, clean_old_postgres_backups.sh will then also be called again and it will recycle/delete base/dump backups that are older than the number of days configured in config.postgres_backups.base_backups.keep_days

A new base and dump backup is created every time postgres_backups.yml is deployed. This behaviour can be disabled setting parameter config.postgres_backups.backup_on_deploy to false.

# Restoring a continuous archiving backup

Restoring a continuous archiving backup to its latest state, based on all the archived wals and a specific base backup, can be easily done calling:

    # /usr/bin/restore_backup_postgres.sh day_month_year_hour_min_sec 'date'

This command must be executed from root, and the first parameter is the name of the folder of the base backup to be used. If the data_folder of the cluster already exists, this script will create a full, gzipped, copy of it in the folder /var/postgres_backups/restore_backups before restoring the backup.

The second argument is the specific date you want to recover the database to. This is an optional argument, and it's only valid for restoring continuous archiving backups. An example date is '2004-07-14 22:39:00 EST'. If you want to recover the state of the database as it was after a given transaction, please set recovery_target_xid on file /etc/postgresql/9.4/main/recovery.conf before calling script restore_backup_postgres.sh instead.

# Restoring a SQL dump backup

Restoring a SQL dump backup from /var/postgres_backups/dump can easily done calling

    # /usr/bin/restore_backup_postgres.sh dump_day_month_year_hour_min_sec

Notice that "dump_" has been added on the argument.

This will recreate the database status as it was when the the backup was created. If the data_folder of the cluster exists, it will first make a copy of it in /var/postgres_backups/restore_backups

NOTE: As of now, restoring a SQL dump backup implies dropping and recreating the cluster. This means that once the backup is restored, wal backups will use timeline 1 from index ..0001. As these new wal files clash with the old backup wal files, during the restoration all old wal files are moved to a /var/postgres_backups/wal/$DATE subfolder, with the aim of preserving them and allowing wal backups. This also means that if you want to restore a continuous archiving backup after restoring a sql dump backup, you will first have to manually move the wal files back from /var/postgres_backups/wal/$DATE to /var/postgres_backups/wal/

# Logs

The Postgresql backup archiving system that deployment-tool installs generates a series of log entries on /var/log/syslog. An easy way to review them is to use the command:

    # cat /var/log/syslog | grep _postgres

Or, if you want to keep an eye on new log entries as they are generated:

    # tail -F /var/log/syslog