import os
import json


def load(filename: str):
    """
    Args:
        filename (str): The path to the file to load data from.
    Returns:
        a\\ny | None: The file's content if it is loaded successfully, None if the file does not exist or is not a file.
    """
    if not os.path.isfile(filename):
        print(f"filename: {filename} either is not a file or does't exist")
        return None
    with open(filename) as file:
        data = json.load(file)
    return data


def get_project_count(db: list[dict]) -> int:
    """
    Args:
        db (list[dict]): The database to get the project count from.
    Returns:
        int: The number of projects in the database.
    """
    if not isinstance(db, list):
        # raise Exception(f"db must be list and not {type(db)}")
        print(f"db must be list and not {type(db)}")
        return 0
    return len(db)


def get_project(db: list[dict], id: int) -> dict | None:
    """
    Args:
        db (list[dict]): The database to get the project from.
        id (int): The ID of the project to get.
    Returns:
        dict | None: The project if it is found, None if the project is not found.
    """
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
    """
    Args:
        db (list[dict]): The database to search in.
        sort_by (str): The field to sort by. Default is "start_date".
        sort_order (str): The order to sort in. Default is "desc".
        techniques (list[str] | None): The techniques to search for. Default is None.
        search (str | None): The search query. Default is None.
        search_fields (list[str] | None): The fields to search in. Default is None.
    Returns:
        list[dict]: The projects that match the search/filter and sort criteria.
    """
    # Sort
    sorted_db = db.copy()
    sorted_db.sort(
        key=lambda project: project.get(sort_by, ""),
        reverse=True if sort_order == "desc" else False,
    )

    # Techniques
    filtered_db = [] if techniques else sorted_db
    if techniques:
        for project in sorted_db:
            # Checks if techniques exists inside techniques_used
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
                if search.upper() in str(value).upper():
                    searched_db.append(project)
                    break
    else:
        for project in filtered_db:
            for field in search_fields:
                if  search.upper() in str(project.get(field, "")).upper():
                    searched_db.append(project)
                    break
                

    return searched_db

def get_techniques(db: list[dict]) -> list[str]:
    """
    Args:
        db (list[dict]): The database to get the techniques from.
    Returns:
        list[str]: All the unique techniques used in projects in the database.
    """
    used_techniques = []
    for project in db:
        for technique in project["techniques_used"]:
            if not technique in used_techniques:
                used_techniques.append(technique)

    used_techniques.sort()
    return used_techniques


def get_technique_stats(db: list) -> dict[str, list[dict]]:
    """
    Args:
        db (list[dict]): The database to get the technique stats from.
    Returns:
        dict[str, list[dict]]: A dictionary with techniques as keys and a list of projects using that technique as values.
    """
    techniques_info: dict[str, list[dict]] = {}
    for project in db:
        for technique in project["techniques_used"]:
            if not technique in techniques_info:
                techniques_info[technique] = []

            techniques_info[technique].append(
                {"id": project["project_id"], "name": project["project_name"]}
            )

    return techniques_info
