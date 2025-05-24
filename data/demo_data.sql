CREATE TABLE IF NOT EXISTS staff (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    fio TEXT NOT NULL,
    ipn TEXT NOT NULL UNIQUE,
    manager_fio TEXT,
    role TEXT NOT NULL CHECK (role IN ('Employee', 'Manager', 'HR Manager')),
    vacation_days_per_year INTEGER NOT NULL,
    remaining_vacation_days INTEGER DEFAULT 0 -- Added default for simplicity
);

CREATE TABLE IF NOT EXISTS vacations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    staff_id INTEGER NOT NULL,
    start_date TEXT NOT NULL, -- YYYY-MM-DD
    end_date TEXT NOT NULL,   -- YYYY-MM-DD
    days_count INTEGER NOT NULL,
    FOREIGN KEY (staff_id) REFERENCES staff(id)
);

-- Сотрудники
INSERT INTO staff (fio, ipn, manager_fio, role, vacation_days_per_year) VALUES 
('Иванов Иван', '1234567890', 'Петров Петр', 'Employee', 24),
('Сидорова Мария', '0987654321', 'Петров Петр', 'Employee', 24),
('Петров Петр', '1111111111', NULL, 'Manager', 26),
('Антонова Анна', '2222222222', NULL, 'HR Manager', 30);

-- Отпуска
INSERT INTO vacations (staff_id, start_date, end_date, days_count) VALUES
(1, '2025-06-01', '2025-06-14', 14),
(2, '2025-07-10', '2025-07-20', 11),
(3, '2025-08-05', '2025-08-15', 11);
