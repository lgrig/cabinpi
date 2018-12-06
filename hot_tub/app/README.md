how to build an interruptable background task

1) Build a database table
2) Have the "turn off", "turn on" functions simply write to that table
3) Query for the latest entry of that table
4) nested while loops

While True:
    if query_latest == 'on':
        turn_on
        sleep(30)
    else:
        turn_off
        sleep(30)

separate program writes to the database!
