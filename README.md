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
 * But it might be a column modification
 * We can sort the column names, then issue a query to fetch every record, sorted by that sorted column list.
 * We want to transform one side to the other side without transferring too much data.
 * We walk through the data and hash the data of the record combined with the previous hash of the previous record. 
 * To check for modifications, we check hash 0 and hash N (size of table), if the hashes don't match. If N (size of table) has equal hash to us, then the data is all the same on both servers.
 * We binary search the index for the first non-conflicting data record.
 * We know the two records that have changed between servers. Which record wins?
 * If we have a timestamp column, we use that.
 * We change the record that doesn't match the hash to look like the other.
 * This winner calculation needs to produce the same result on both servers when they both do this operation.
 * We could introduce a version column, and the higher version wins.


Rolling hash.

