def update_status_break_in:
    UPDATE battery
    SET
    status_ref = 1,
    last_update = current_timestamp
    WHERE
    date(current_timestamp) - date(last_update) > -1 and status_ref != 7

    update
    battery as a
    set
    status_ref = 8
    from
    (select count (status_ref), battery_ref
    from batterylog
        where
    status_ref = 3
    group
    by
    battery_ref
    having
    count(status_ref) % 10 = 0) as b
    where
    a.battery_id = b.battery_ref



