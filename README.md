# postgres-sync

beginnings of a postgres synchronization solution. This is incomplete.

This doesn't use WAL replication or anything fancy. Essentially this is a simple synchronization solution that doesn't try cause IDs to match up.

I wanted to try avoid updating the tables but want records created in one postgresql install to be added to another.

# detecting new records

 * We keep track of the last row count on each server.
 * And then we check the row count of the server.
 * If the new row count is less than the last row count, that's a delete
 * If the new row count is higher than the last row count, we retrieve **last row count** to **new row count records** and save them in our database under new IDs.

# detecting changes

When the records have identical counts, we need to synchronize changed tables and rows.

 * We can sort the column names, then issue a query to fetch every record, sorted by that sorted column list.
 * We want to transform one side to the other side without transferring too much data.
 * We hash every row and store the data on the file system.
 * The other node synchronizes the hash list.
 * The other node hashes all its own records and checks if they exist in the hash list.
 * If a hash doesn't exist, it inserts the record into the database.
 * But it might be a column modification.


Rolling hash.

