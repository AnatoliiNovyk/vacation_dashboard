CREATE TABLE IF NOT EXISTS staff (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    fio TEXT NOT NULL,
    ipn TEXT NOT NULL CHECK(length(ipn) = 10),
    manager_fio TEXT,
    role TEXT NOT NULL,
    vacation_days_per_year INTEGER NOT NULL
);

CREATE TABLE IF NOT EXISTS vacations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    staff_id INTEGER NOT NULL,
    start_date TEXT NOT NULL,
    end_date TEXT NOT NULL,
    days_count INTEGER NOT NULL,
    FOREIGN KEY(staff_id) REFERENCES staff(id)
);
