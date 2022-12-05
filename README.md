# Fetch Rewards #
## Solution ##

I chose to write my solution using python. Before running the solution, but after the Postgres database is set up, connect to the postgres database using the command in the instructions:

```
psql -d postgres -U postgres  -p 5432 -h localhost -W
```

Enter `postgres` when prompted for the password. Then enter the following line to change the app_version column type to `VARCHAR`:

```sql
ALTER TABLE user_logins ALTER COLUMN app_version TYPE VARCHAR;
```

I'm not actually sure if this is correct, but I could not think of a good way to make the data fit into an `integer` column, so I thought this was the best solution. After this, run 

```
python read_queue_write_postgres.py
```

on the command line to run the solution. The postgres database should be populated with the data after the program is done running.


## Thought process ##

I started my solution with a copy of the `create_and_write_to_queue.py` file from the scripts folder and kept some of the lines relevant to the queue connection. For reading the data, through trial and error I eventually arrived at line 24 to read each message as a dictionary of the column names and values, which could then be transformed into a dataframe using pandas. I then hashed the `ip` and `device_id` columns to mask the true values. Hashing allows users to identify when there are duplicates since duplicates will be hashed to the same value. For the date column, I used a datetime function to get the current date. There was also a date field in the message metadata which could have been used for this column.

For the write component, the only challenge was figuring out the correct syntax for creating a connection to the postgres db. 



## Next Steps ##
The main way I would flesh out this project would be to create additional tables for when we see duplicate values for some of the columns. For example, we could create a table of just users and the different device_types which they use, or of users and the different device_ids associated with each user. 
