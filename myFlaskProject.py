# TODO: ask about presentationslagret nr 5. Ar det alt eller liten text

import os
from flask import Flask, render_template, request, url_for
import data_helper as data


def update_db():
    """
    Update the database
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
    Check if the database has been updated
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
    Render the index page
    """
    return render_template("index.html")


# TODO: do we need to save search terms???
@app.route("/list")
def list():
    """
    Render the list page
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
    Render the techniques page
    """
    check_db_update()
    return render_template(
        "techniques.html",
        techniques=data.get_techniques(db),
        techniques_stats=data.get_technique_stats(db),
    )


# TODO: Do we need a GET-variable for project_id?????
# TODO: Fix so the correct error statuscode is sent to the user if the file doesnt exist (404)
@app.route("/project/<int:project_id>")
def project(project_id: int):
    """
    Render the project page
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
    Run the application
    """
    app.run(debug=True, port=4001)
