import os
import json


def load(filename: str):
    if not os.path.isfile(filename):
        print(f"filename: {filename} either is not a file or does't exist")
        return None
    with open(filename) as file:
        data = json.load(file)
    return data


def get_project_count(db: list[dict]) -> int:
    if not isinstance(db, list):
        # raise Exception(f"db must be list and not {type(db)}")
        print(f"db must be list and not {type(db)}")
        return 0
    return len(db)


def get_project(db: list[dict], id: int) -> dict | None:
    if not isinstance(db, list):
        # raise Exception(f"db must be list and not {type(db)}")
        print(f"db must be list and not {type(db)}")
        return {}

    for project in db:
        if project.get("project_id") == id:
            return project
    print(f"No project with project_id found for {id}")


def search(
    db: list[dict],
    sort_by: str = "start_date",
    sort_order: str = "desc",
    techniques: list[str] | None = None,
    search: str | None = None,
    search_fields: list[str] | None = None,
):
    # Sort
    sorted_db = db.copy()
    sorted_db.sort(
        key=lambda project: project.get(sort_by, "99999"),
        reverse=True if sort_order == "desc" else False,
    )

    # Techniques
    filtered_db = [] if techniques else sorted_db
    if techniques:
        for project in sorted_db:
            if set(techniques).issubset(project["techniques_used"]):
                filtered_db.append(project)

    # Search
    searched_db = []
    if not search:
        return filtered_db
    elif search_fields== []:
        return [] 
    elif search_fields == None:
        for project in filtered_db:
            for value in project.values():
                if search == value:
                    searched_db.append(project)
                    break
    else:
        for project in filtered_db:
            for field in search_fields:
                if str(project.get(field, "")).upper() == search.upper():
                    searched_db.append(project)
                    break
                

    return searched_db

def get_techniques(db: list[dict]) -> list[str]:
    used_techniques = []
    for project in db:
        for technique in project["techniques_used"]:
            if not technique in used_techniques:
                used_techniques.append(technique)

    used_techniques.sort()
    return used_techniques


def get_technique_stats(db: list) -> dict[str, list[dict]]:
    techniques_info: dict[str, list[dict]] = {}
    for project in db:
        for technique in project["techniques_used"]:
            if not technique in techniques_info:
                techniques_info[technique] = []

            techniques_info[technique].append(
                {"id": project["project_id"], "name": project["project_name"]}
            )

    return techniques_info
