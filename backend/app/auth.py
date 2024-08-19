import logging
import requests
from google_auth_oauthlib.flow import Flow
from django.http import JsonResponse
from django.contrib.auth.models import User, Group
from django.contrib.auth import authenticate
from rest_framework.decorators import api_view
from .models import Profile
from .auxil import get_edooshit_teachers, get_edooshit_students
from .config import GOOGLE_OAUTH2_REDIRECT_URI

logger = logging.getLogger(__name__)


def _create_user(user_data, *args, **kwargs):
    logger.info("Creating user account.")
    if not user_data:
        logger.error("User data not provided. Aborting.")
        return

    user = User.objects.create_user(
        username=user_data.get("email").split("@")[0],
        email=user_data.get("email"),
    )
    user.save()

    return user


def _update_user_basic_data(user_data, *args, **kwargs):
    logger.info("Updating user account.")
    user = User.objects.filter(email=user_data.get("email")).first()

    if not user:
        logger.error("User not found. Aborting.")
        return

    user.first_name = user_data.get("given_name")
    user.last_name = user_data.get("family_name")
    user.save()


def _update_user_group(user_data, *args, **kwargs):
    user = User.objects.filter(email=user_data.get("email")).first()
    if not user:
        logger.error("User not found. Aborting.")
        return

    # Add user to group if not already in some
    if not user.groups.exists():
        logger.info("Updating user group.")
        teachers_list = get_edooshit_teachers()
        if (user.first_name, user.last_name) in teachers_list:
            group = Group.objects.filter(name="Teacher").first()
            if not group:
                logger.error(
                    "Teachers group not found. Skipping. "
                    "User should be added to a group manually."
                )
            else:
                user.groups.add(group)
                logger.info("User added to teachers group.")
        else:
            group = Group.objects.filter(name="Student").first()
            if not group:
                logger.error(
                    "Students group not found. Skipping. "
                    "User should be added to a group manually."
                )
            else:
                user.groups.add(group)
                logger.info("User added to students group.")
        user.save()


def _find_student_class(first_name, last_name, *args, **kwargs):
    logger.info("Finding student class.")
    students_list = get_edooshit_students()

    for student in students_list:
        if (
            student["first_name"] in first_name
            and student["middle_name"] in first_name
            and student["last_name"] == last_name
        ):
            return student["class"]

    logger.info("Student class not found.")


def _update_user_profile(user_data, *args, **kwargs):
    user = User.objects.filter(email=user_data.get("email")).first()
    if not user:
        logger.error("User not found. Aborting.")
        return

    # TODO Update profile
    if not hasattr(user, "profile"):
        logger.info("Updating user profile.")
        profile = Profile(user=user)

        # Set student class
        if user.groups.filter(name="Student").exists():
            student_class = _find_student_class(user.first_name, user.last_name)
            if student_class:
                number, letter = student_class.split(".")
                profile.cls = Profile.Classes(f"{letter}{number}")

        profile.save()
        logger.info("Profile created.")


def _handle_first_google_login(user_data, *args, **kwargs):
    logger.info("Handling first time Google login.")
    lang = kwargs.get("lang")

    # Get or create user
    user = _create_user(user_data)
    if not user:
        logger.error("User not found or creating failed. Aborting.")
        return {
            "success": False,
            "error": (
                "User not found or creating failed."
                if lang == "en"
                else "Uživatel nenalezen nebo jeho vytváření selhalo."
            ),
        }

    # Update user profile and group
    _update_user_basic_data(user_data)
    _update_user_group(user_data)
    _update_user_profile(user_data)


def _get_user_data_from_db(user, *args, **kwargs):
    logger.info("Getting user data.")
    lang = kwargs.get("lang")
    try:
        return {
            "success": True,
            "user_id": user.id,
            "username": user.username,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "email": user.email,
        }
    except Exception as e:
        logger.error(f"Error: {e}")
        return {
            "success": False,
            "error": (
                "Error occurred when reading user from database."
                if lang == "en"
                else "Nastala chyba při čtení uživatele z databáze."
            ),
        }


@api_view(["POST"])
def handle_login(request, *args, **kwargs):
    logger.info("Handling login.")
    user_data = request.data.get("user_data")
    google_login = request.data.get("google")
    lang = request.headers.get("Language")

    if not user_data:
        logger.error("User data not provided. Aborting.")
        return JsonResponse(
            {
                "success": False,
                "error": (
                    "User data not provided."
                    if lang == "en"
                    else "Uživalská data nedostupná."
                ),
            }
        )

    if google_login:
        logger.info("Handling Google login.")
        user = User.objects.filter(email=user_data.get("email")).first()
        if not user:
            _handle_first_google_login(user_data, lang=lang)
            user = User.objects.filter(email=user_data.get("email")).first()
        return JsonResponse(_get_user_data_from_db(user, lang=lang))
    else:
        logger.info("Handling external login.")
        username = user_data.get("username")
        password = user_data.get("password")
        user = authenticate(username=username, password=password)
        if not user:
            return JsonResponse(
                {
                    "success": False,
                    "error": (
                        "Invalid username or password."
                        if lang == "en"
                        else "Neplatné uživatelské jméno nebo heslo."
                    ),
                }
            )
        return JsonResponse(_get_user_data_from_db(user, lang=lang))


@api_view(["POST"])
def get_google_profile(request, *args, **kwargs):
    logger.info("Getting Google profile using access token.")
    access_token = request.data.get("access_token")
    lang = request.headers.get("Language")

    if not access_token:
        logger.error("Access token not provided. Aborting.")
        return JsonResponse(
            {
                "success": False,
                "error": (
                    "Access token not provided."
                    if lang == "en"
                    else "Přístupový token nenalezen."
                ),
            }
        )

    response = requests.get(
        f"https://www.googleapis.com/oauth2/v3/userinfo",
        params={"access_token": access_token},
    )

    if response.status_code != 200:
        logger.error("Error occurred when getting Google profile.")
        return JsonResponse(
            {
                "success": False,
                "error": (
                    "Error occurred when getting Google profile."
                    if lang == "en"
                    else "Nastala chyba při načítání Google profilu."
                ),
            }
        )

    return JsonResponse({"success": True, "user_data": response.json()})
