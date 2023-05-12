from flask import Flask, render_template, redirect, url_for
import sqlite3
import json
from ai import OpenAI

app = Flask(__name__, template_folder='templates')

@app.route('/')
def hello():
    return render_template('base.html', title='Hello')

@app.route('/plan-sprint/<sprint_number>')
def planSprintRequest(sprint_number):
    planSprint(sprint_number)
    updateWorkerCapacity()
    return redirect('/sprint/{0}'.format(sprint_number))

@app.route('/reset-sprint/<sprint_number>')
def resetSprint(sprint_number):
    doReset(sprint_number)
    updateWorkerCapacity()
    return redirect('/sprint/{0}'.format(sprint_number))

def doReset(sprint_number):
    query = "UPDATE tickets SET assigned_worker_id = null WHERE sprint_number = {0}".format(sprint_number)
    connection = sqlite3.connect("hackathon.db")
    cursor = connection.cursor()
    cursor.execute(query)
    connection.commit()
    cursor.close()

def getSprintTickets(sprint_number):
    connection = sqlite3.connect("hackathon.db")
    query = "SELECT id, ticket_description, size from tickets where sprint_number = " + sprint_number + ";"
    cursor = connection.cursor()
    rows = cursor.execute(query).fetchall()    
    return rows

@app.route('/sprint/<sprint_number>')
def assignedSprintTickets(sprint_number):
    rows = getAssignedSprintTickets(sprint_number)
    tickets = [{'id': row[0], 'description': row[1], 'size': row[2], 'assigned_worker_id': row[3]} for row in rows]
    rows = getWorkers()
    workers = [{'id': row[0], 'skillset': row[1], 'capacity': row[2], 'remaining_capacity': row[3]} for row in rows]
    return render_template('hackathon.html', title='Current Sprint Tickets',
                           tickets=tickets, workers=workers)  

def updateWorkerCapacity():
    workers = getWorkers()
    for worker in workers:
        connection = sqlite3.connect("hackathon.db")
        cursor = connection.cursor()
        query = "SELECT SUM(size) FROM tickets WHERE assigned_worker_id = {0}".format(worker[0])
        used_capacity = cursor.execute(query).fetchall()[0][0]
        if used_capacity == None:
            used_capacity = 0
        remaining_capacity = worker[2] - used_capacity
        query = "UPDATE workers SET remaining_capacity = {0} WHERE id = {1}".format(remaining_capacity, worker[0])
        cursor.execute(query)
        connection.commit()
        cursor.close()


#@app.route('/sprint/<sprint_number>')
def getAssignedSprintTickets(sprint_number):
    connection = sqlite3.connect("hackathon.db")
    query = "SELECT id, ticket_description, size, assigned_worker_id from tickets where sprint_number = " + sprint_number + ";"
    cursor = connection.cursor()
    rows = cursor.execute(query).fetchall()
    return rows

#app.route('/workers')
def getWorkers():
    connection = sqlite3.connect("hackathon.db")
    query = "SELECT id, skillset, capacity, remaining_capacity from workers;"
    cursor = connection.cursor()
    rows = cursor.execute(query).fetchall()    
    return rows

#@app.route('/sprint-plan-prompt/<sprint_number>')
def getSprintPlanPrompt(sprint_number):
    workers = getWorkers()
    tickets = getSprintTickets(sprint_number)
    return json.dumps(planSprintPrompt(workers, tickets))


def planSprintPrompt(workers, tickets):
    worker_names = get_worker_names(workers)
    prompt = "I have {0} workers, numbered {1}. Each worker has a skillset and a capacity for the work week. ".format(len(workers), worker_names)
    for worker in workers:
        prompt += "Worker {0} has a skillset of {1} and a capacity of {2} hours. ".format(worker[0], worker[1], worker[2])
    prompt += "The team has {0} unassigned tasks to complete for the upcoming work week. ".format(len(tickets))
    for ticket in tickets:
        prompt += "Task {0} is to {1}. This is estimated to take {2} hours. ".format(ticket[0], ticket[1], ticket[2])
    prompt += ("Could you please assign these {0} tasks to my {1} workers primarily based on their skillset "
                "and making sure not to exceed each worker's inidividual capacity. Answer should be in a csv file format with column 1 being task number and column 2 being worker number assigned to the task. "
                "The csv file should begin with ``` and end with ``` and be plain formatted with no quotation marks.").format(len(tickets), len(workers))
    return prompt

def get_worker_names(workers):
    names = ""
    for worker in workers:
        names += str(worker[0]) + ", "
    names = names[:-2]
    return names

def planSprint(sprint_number):
    workers = getWorkers()
    tickets = getSprintTickets(sprint_number)
    prompt = planSprintPrompt(workers, tickets)
    ai = OpenAI()
    response = ai.makeQuery(prompt)
    print(response)
    consumed = consumeResponse(response)
    updateTickets(consumed)

def consumeResponse(response):
    result = response.split("```")[1]
    just_numbers = '1' + substring_after(result, '1').replace(", ", ",")
    lst = just_numbers.split("\n")
    lst = list(filter(None, lst))
    return [{"task":str[0], "worker":str[2]} for str in lst]

def updateTickets(response):
    for dict in response:
        query = "UPDATE tickets SET assigned_worker_id = {0} WHERE id = {1}".format(dict['worker'], dict['task'])
        connection = sqlite3.connect("hackathon.db")
        cursor = connection.cursor()
        cursor.execute(query)
        connection.commit()
        cursor.close()
    print("Records updated successfully")

def substring_after(s, delim):
    return s.partition(delim)[2]

app.run()
