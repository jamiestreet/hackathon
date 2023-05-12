CREATE TABLE workers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    worker_name TEXT NOT NULL,
    skillset TEXT NOT NULL,
    capacity INTEGER NOT NULL,
    remaining_capacity INTEGER NOT NULL
);

CREATE TABLE tickets (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    sprint_number INTEGER,
    ticket_description TEXT NOT NULL,
    size INTEGER NOT NULL,
    assigned_worker_id INTEGER,
    completed INTEGER,
    time_to_complete INTEGER
);

CREATE TABLE sprints (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    starting_date DATE NOT NULL,
    ending_date DATE NOT NULL,
    total_tickets INTEGER NOT NULL,
    tickets_completed INTEGER NOT NULL,
    total_size INTEGER NOT NULL,
    ticket_completion_time INTEGER NOT NULL
);