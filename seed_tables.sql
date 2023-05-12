INSERT INTO workers (worker_name, skillset, capacity, remaining_capacity)
VALUES
	("Jamie", "Python, presenting, debugging", 25, 25),
	("Cameron", "SQL, Excel, mentoring", 30, 30),
	("Yun", "web development, Java, governance", 20, 20);

INSERT INTO tickets (sprint_number, ticket_description, size)
VALUES
	(1, "Create database table", 5),
	(1, "Add new button to website", 3),
    (1, "Train new team member", 10),
    (1, "Build new Pandas machine learning model", 15),
    (1, "Present to stakeholders", 5),
    (1, "Create governance document", 10),
    (1, "Debug failed TeamCity build", 2),
    (1, "Update cost spreadsheet", 12),
    (1, "Add feature to Springboot application", 4);

INSERT INTO sprints(starting_date, ending_date, total_tickets, tickets_completed, total_size, ticket_completion_time)
VALUES
    ('2023-04-24', '2023-04-28', 9, 0, 66, 0);