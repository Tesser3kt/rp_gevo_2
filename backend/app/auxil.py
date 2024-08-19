import logging
import requests
from .config import EDOOSHIT_API

logger = logging.getLogger(__name__)


def get_edooshit_teachers():
    logger.info("Getting teachers from Edooshit API.")
    r = requests.get(EDOOSHIT_API["teachers"])

    teachers = [
        (teacher["Firstname"], teacher["Lastname"])
        for teacher in r.json().get("Employees")
    ]
    logger.info("Teachers fetched.")

    return teachers


def get_edooshit_students():
    logger.info("Getting students from Edooshit API.")
    r = requests.get(EDOOSHIT_API["students"])

    students = [
        {
            "first_name": student["Firstname"],
            "middle_name": (
                student["Middlename"] if student["Middlename"] else ""
            ),
            "last_name": student["Lastname"],
            "class": student["ClassName"],
        }
        for student in r.json().get("Students")
    ]
    logger.info("Students fetched.")

    return students
