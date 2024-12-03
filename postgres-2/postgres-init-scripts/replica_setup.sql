SELECT pg_create_physical_replication_slot('replication_slot_slave1');

DO $$
BEGIN
    RAISE NOTICE 'Setting up replication';
    -- Write recovery settings
    EXECUTE format('
        COPY (SELECT ''primary_conninfo=''host=db port=5432 user=replicationUser password=replication sslmode=disable'' '') TO PROGRAM ''echo %s > /var/lib/postgresql/data/recovery.conf'';
    ');
END $$;