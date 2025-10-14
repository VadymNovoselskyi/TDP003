import os
from flask import Flask, render_template, request, url_for
import data_helper as data


def update_db():
    """
    Update the database from the DATA_FILE using data.load
    Updates last_db_change to the last modification time of the DATA_FILE \n
    Relies on global db and last_db_change variables \n

    Raises:
        Exception: If the database is not loaded.
    """
    global db
    global last_db_change

    db_tmp = data.load(DATA_FILE)
    if db_tmp is None:
        raise Exception("no data")

    db = db_tmp
    last_db_change = os.path.getmtime(DATA_FILE)


# Using pollign to check if db file was changed
def check_db_update():
    """
    Checks if the database has been updated
    If it has, calls the update_db function \n
    Relies on global last_db_change variable
    """
    current_db_change = os.path.getmtime(DATA_FILE)
    if not current_db_change == last_db_change:
        update_db()


app = Flask(__name__)  # type: ignore
DATA_FILE = "data.json"
update_db()


@app.route("/")
def index():
    """
    Renders the index page using "index.html" template
    """
    return render_template("index.html")


@app.route("/list")
def list():
    """
    Renders the list page using "list.html" template


    If sort_by and sort_order are provided, calls data.search function to search the database
    with search, search_fields, techniques, sort_by, and sort_order from GET-parameters. \n
    In this case renders"list.html" with projects=searched_db,
    project_count=data.get_project_count(searched_db), original_count=data.get_project_count(db),
    techniques=data.get_techniques(db).

    Otherwise, renders "list.html" with projects=db, project_count=data.get_project_count(db),
    original_count=data.get_project_count(db), techniques=data.get_techniques(db). \n

    Calls check_db_update function to check if the database has been updated 
    """
    check_db_update()
    search = request.args.get("search")
    search_fields = request.args.getlist("search_fields")
    techniques = request.args.getlist("techniques")
    sort_by = request.args.get("sort_by")
    sort_order = request.args.get("sort_order")

    if sort_by and sort_order:
        searched_db = data.search(
            db,
            sort_by,
            sort_order,
            techniques,
            search,
            search_fields if search_fields else None,
        )
        return render_template(
            "list.html",
            projects=searched_db,
            project_count=data.get_project_count(searched_db),
            original_count=data.get_project_count(db),
            techniques=data.get_techniques(db),
        )

    return render_template(
        "list.html",
        projects=db,
        project_count=data.get_project_count(db),
        original_count=data.get_project_count(db),
        techniques=data.get_techniques(db),
    )


@app.route("/techniques")
def techniques():
    """
    Renders the techniques page using "techniques.html" template
    with techniques=data.get_techniques(db), and techniques_stats=data.get_technique_stats(db). \n

    Calls check_db_update function to check if the database has been updated \n
    """
    check_db_update()
    return render_template(
        "techniques.html",
        techniques=data.get_techniques(db),
        techniques_stats=data.get_technique_stats(db),
    )


@app.route("/project/<int:project_id>")
def project(project_id: int):
    """
    Renders the project page using "project.html" template
    with project=data.get_project(db, project_id). \n

    Args:
        project_id (int): The ID of the project to display.

    If the project is not found, renders "error.html"
    with code=404 and message=f"Project not found for id: {project_id}".

    Calls check_db_update function to check if the database has been updated \n
    """
    check_db_update()
    project = data.get_project(db, project_id)
    if project is None:
        return render_template(
            "error.html", code=404, message=f"Project not found for id: {project_id}"
        )
    return render_template("project.html", project=project)


if __name__ == "__main__":
    """
    Runs the application on port 4001 in debug mode
    """
    app.run(debug=True, port=4001)
