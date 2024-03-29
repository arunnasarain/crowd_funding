from datetime import datetime

from database import get_db_connection
import mysql.connector
from flask import jsonify
import traceback


def create_project(req):
    try:
        new_project = req.json  # Get request body
        db = get_db_connection()
        dbcursor = db.cursor()

        # Check for empty or nil field
        if "" in new_project.values():
            return ("Some fields are not valid",), 400

        # Check if funding goal is positive non-zero value
        if new_project.get('fundingGoal') <= 0:
            return ("The funding goal cannot be negative or 0",), 400

        # Check if title already exists
        title_exists_query = f"SELECT title FROM projects WHERE title = '{new_project['title']}'"
        dbcursor.execute(title_exists_query)
        title_exists_result = dbcursor.fetchall()
        if title_exists_result:
            return ("The project with the same title already exists.",), 400

        # Insert data into table
        sql_insert = "INSERT INTO projects (title, description,category,funding_goal,current_funding,created_at,updated_at) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        values = (new_project['title'], new_project['description'], new_project['category'],
                  new_project['fundingGoal'], new_project['currentFunding'], datetime.now().isoformat(),
                  datetime.now().isoformat())
        dbcursor.execute(sql_insert, values)
        db.commit()

        # Fetch the last inserted row by row id
        last_insert_id = dbcursor.lastrowid
        dbcursor.execute("Select * from projects where id = %s", (last_insert_id,))
        project = dbcursor.fetchone()
        print(type(project))

        return {
            'id': project[0],
            'category': project[1],
            'createdAt': project[2],
            'currentFunding': float(project[3]),
            'description': project[4],
            'fundingGoal': float(project[5]),
            'title': project[6],
            'updatedAt': project[7]
        }, 200

    # Exception Handling
    except Exception as e:
        print("Exception occurred", e)
        return None, 500

    # Close cursor and DB connection
    finally:
        if 'db' in locals() and db.is_connected():
            dbcursor.close()
            db.close()


def get_all_projects():
    try:
        db = get_db_connection()
        dbcursor = db.cursor()
        dbcursor.execute("SELECT * FROM projects")
        projects = dbcursor.fetchall()

        project_with_keys = list()
        for project in projects:
            project_with_keys.append({
                'id': project[0],
                'category': project[1],
                'createdAt': project[2],
                'currentFunding': float(project[3]),
                'description': project[4],
                'fundingGoal': float(project[5]),
                'title': project[6],
                'updatedAt': project[7]
            })

        return project_with_keys, 200

    # Exception Handling
    except Exception as e:
        print("Exception occurred", e)
        return None, 500

    # Close cursor and DB connection
    finally:
        if 'db' in locals() and db.is_connected():
            dbcursor.close()
            db.close()


def get_projects_by_category(category):
    try:
        db = get_db_connection()
        dbcursor = db.cursor()
        print(category)

        # Get all projects under the given category
        dbcursor.execute(f"SELECT * FROM projects WHERE category = {category}")
        projects = dbcursor.fetchall()

        # Initialize a empty list and append the mapped key and value of projects
        project_with_keys = list()
        for project in projects:
            project_with_keys.append({
                'id': project[0],
                'category': project[1],
                'createdAt': project[2],
                'currentFunding': float(project[3]),
                'description': project[4],
                'fundingGoal': float(project[5]),
                'title': project[6],
                'updatedAt': project[7]
            })

        return project_with_keys, 200

    # Exception Handling
    except Exception as e:
        print("Exception occurred", e)
        return None, 500

    # Close cursor and DB connection
    finally:
        if 'db' in locals() and db.is_connected():
            dbcursor.close()
            db.close()


def get_project_details(project_id):
    try:
        db = get_db_connection()
        dbcursor = db.cursor()
        dbcursor.execute(f"SELECT * FROM projects WHERE id = '{project_id}'")
        project = dbcursor.fetchone() # Using fetchone as there cant be multiple entries with same project id

        if project is None:
            return None, 404

        # Check for any feedbacks related to this project
        dbcursor.execute(f"SELECT * FROM feedbacks WHERE project_id = {project_id}")
        feedbacks = dbcursor.fetchall()

        # Initiate an empty list and append the map of feedbacks
        feedback_with_keys = list()
        for feedback in feedbacks:
            feedback_with_keys.append({
                'feedbackId': feedback[0],
                'comment': feedback[1],
                'investorId': feedback[2],
                'projectId': feedback[3],
                'rating': feedback[4],
                'timestamp': feedback[5]
            })

        # Create a map and assign values to the keys.
        # Pass feedback_with_keys to feedbacks
        project_with_keys = {
            'id': project[0],
            'category': project[1],
            'createdAt': project[2],
            'currentFunding': float(project[3]),
            'description': project[4],
            'fundingGoal': float(project[5]),
            'title': project[6],
            'updatedAt': project[7],
            'feedbacks': feedback_with_keys
        }

        return project_with_keys, 200

    # Exception Handling
    except Exception as e:
        print("Exception occurred", e)
        return None, 500

    # Close cursor and DB connection
    finally:
        if 'db' in locals() and db.is_connected():
            dbcursor.close()
            db.close()


def get_all_investors():
    try:
        db = get_db_connection()
        dbcursor = db.cursor()
        dbcursor.execute("SELECT * FROM investors") # Fetching all investors
        investors = dbcursor.fetchall()

        investors_with_keys = list()
        for investor in investors:
            investors_with_keys.append({
                'investorId': investor[0],
                'email': investor[1],
                'investorName': investor[2],
                'totalInvestedAmount': float(investor[3]),
            })

        return investors_with_keys, 200

    # Exception Handling
    except Exception as e:
        print("Exception occurred", e)
        return None, 500

    # Close cursor and DB connection
    finally:
        if 'db' in locals() and db.is_connected():
            dbcursor.close()
            db.close()
            print("Database closed")


def make_investment(req):
    # req is flask request object. request.json has the request json body.
    new_investment = req.json
    try:
        db = get_db_connection()
        dbcursor = db.cursor()

        # Make sure no values are empty.
        # The values() return a tuple of all the values without the keys.
        if '' in new_investment.values():
            return ("Some fields are empty",), 400

        # Check if the amount is valid
        if new_investment['amount'] <= 0:
            return ("Amount must be non-zero positive value",), 400

        dbcursor.execute("SELECT * FROM projects where id=%s", (new_investment['project_id'],))
        project = dbcursor.fetchone()

        if project is None:
            return ("Project does not exist",), 400

        dbcursor.execute("SELECT * FROM investors where investor_id=%s", (new_investment['investor_id'],))
        investor = dbcursor.fetchone()

        if investor is None:
            return ("Investor does not exist",), 400

        dbcursor.execute("SELECT amount FROM investments WHERE project_id=%s", (new_investment['project_id'],))
        investments = dbcursor.fetchall()
        total_investment = 0

        # Add up all the investment made on the project
        for investment in investments:
            total_investment += float(investment[0])

        # Check if the investment have reached the goal 
        if total_investment >= project[5]:
            return ("The funding goal has already been reached.",), 400

        # Check if the current investment will not exceed funding goal
        if total_investment + new_investment['amount'] > project[5]:
            return ("The investment amount is too high.",), 400

        # Insert the data after all the checks are passed
        sql_insert = "INSERT INTO investments (amount, project_id, timestamp, investor_id) VALUES (%s, %s, %s, %s)"
        values = (new_investment['amount'], new_investment['project_id'], datetime.now().isoformat(),
                  new_investment['investor_id'])
        dbcursor.execute(sql_insert, values)
        db.commit()
        new_investment_id = dbcursor.lastrowid # Get the id of the last inserted row

        # Update the investors table for this investor
        updated_invested_amount = float(investor[3]) + new_investment['amount']
        sql_update = "UPDATE investors SET total_invested_amount=%s WHERE investor_id=%s"
        values = (updated_invested_amount, new_investment['investor_id'])
        dbcursor.execute(sql_update, values)
        db.commit()

        return ({
                    "investmentId": new_investment_id,
                    "projectId": new_investment['project_id'],
                    "investorId": new_investment['investor_id'],
                    "investorName": investor[2],
                    "investorEmail": investor[1],
                    "amountInvested": float(new_investment['amount']),
                    "timestamp": datetime.now().isoformat()
                }, 200)

    except Exception as e:
        print("Exception occurred", e)
        traceback.print_exc()
        return None, 500

    finally:
        if 'db' in locals() and db.is_connected():
            dbcursor.close()
            db.close()

    return investment


def get_investment_details_by_project_id(project_id):
    try:
        db = get_db_connection()
        dbcursor = db.cursor()
        dbcursor.execute("SELECT * FROM projects where id=%s", (project_id,))
        project = dbcursor.fetchone()

        if project is None:
            return ("Project does not exist",), 400

        # Fetch all investments for the project
        dbcursor.execute("SELECT * FROM investments where project_id=%s", (project_id,))
        investments = dbcursor.fetchall()

        investors_list = list()

        for investment in investments:
            dbcursor.execute("SELECT * FROM investors where investor_id=%s", (investment[4],))
            investor = dbcursor.fetchone()

            investors_list.append({
                "investorId": investment[4],
                "investorName": investor[2],
                "email": investor[1],
                "amount": float(investment[1])
            })

        return {
            "projectId": project[0],
            "currentFunding": float(project[3]),
            "fundingGoal": float(project[5]),
            "investors": investors_list,
            "timestamp": datetime.utcnow().isoformat()
        }, 200

    except Exception as e:
        print("Exception occurred", e)

    finally:
        if 'db' in locals() and db.is_connected():
            dbcursor.close()
            db.close()


def get_investor_dashboard(investor_id):
    try:
        db = get_db_connection()
        dbcursor = db.cursor()
        dbcursor.execute(f"SELECT * FROM investors where investor_id={investor_id}")
        investor = dbcursor.fetchone()

        if investor is None:
            return ("The investor with the specified ID was not found.",), 400

        total_investment = investor[3]

        dbcursor.execute(f"SELECT * FROM investments where investor_id={investor[0]}")
        investments = dbcursor.fetchall()

        projectInvestmentsMap = list()

        for investment in investments:
            dbcursor.execute(f"SELECT * FROM projects where id={investment[2]}")
            project = dbcursor.fetchone()

            projectInvestmentsMap.append({
                "projectId": investment[2],
                "title": project[6],
                "category": project[6],
                "fundingGoal": float(project[5]),
                "investedAmount": float(investment[1])
            })

        return {
            "investorId": investor[0],
            "investorName": investor[2],
            "email": investor[1],
            "totalInvestedAmount": float(investor[3]),
            "projectInvestments": projectInvestmentsMap,
            "timestamp": datetime.utcnow().isoformat()
        }, 200

    except Exception as e:
        print("Exception occurred", e)
        traceback.print_exc()

    finally:
        if 'db' in locals() and db.is_connected():
            dbcursor.close()
            db.close()


def submit_feedback(project_id, req):
    try:
        db = get_db_connection()
        dbcursor = db.cursor()

        dbcursor.execute(f"SELECT * FROM projects where id={project_id}")
        project = dbcursor.fetchone()

        if not project:
            return (f"Project with id {project_id}doesnt exist",), 400

        new_feedback = req.json

        if not all(new_feedback.values()):
            return "Some input fields are invalid", 400

        dbcursor.execute(f"SELECT * FROM investors where investor_id={new_feedback['investorId']}")
        investor = dbcursor.fetchone()

        if not investor:
            return f"Investor with id {new_feedback['investorId']}", 400

        rating = new_feedback['rating']

        if rating > 5 or rating < 0:
            return "Rating is invalid", 400

        comment = new_feedback['comment']

        if comment == "":
            return "Comment is invalid", 400

        sql_insert = "INSERT INTO feedbacks (comment,investor_id,project_id,rating,timestamp) VALUES (%s,%s,%s,%s,%s)"
        values = (comment, new_feedback['investorId'], project_id, rating, datetime.now().isoformat())
        dbcursor.execute(sql_insert, values)

        inserted_id = dbcursor.lastrowid

        dbcursor.execute("SELECT * FROM feedbacks WHERE feedback_id=%s", (inserted_id,))
        feedback = dbcursor.fetchone()

        return {
            "feedbackId": feedback[0],
            "projectId": feedback[3],
            "investorId": feedback[2],
            "rating": feedback[4],
            "comment": feedback[1],
            "timestamp": feedback[5]
        }, 200

    except Exception as e:
        print("Exception occurred", e)

    finally:
        if 'db' in locals() and db.is_connected():
            dbcursor.close()
            db.close()
