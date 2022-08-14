# postgres-sync
beginnings of a postgres synchronization solution

This doesn't use WAL replication or anything fancy. Essentially this is a simple synchronization solution that doesn't try cause IDs to match up.

We assume we cannot update the schema of database tables.
