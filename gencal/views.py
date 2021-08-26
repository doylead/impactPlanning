from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.db import IntegrityError

from .models import User, Character, Day, Weapon

# Create your views here.

def login_view(request):
    """
    Provides an interface for users to log in to the site
    """
    if request.method == "POST":
        # Attempt to authenticate with the parameters provided
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        # Check if authentication was successful
        if user is not None:
            # Login successful
            login(request, user)
            return HttpResponseRedirect(reverse('index'))
        else:
            # Login unsuccessful
            return render(request, "gencal/login.html", {
                "message": "Invalid username and/or password"
            })
    else:
        return render(request, "gencal/login.html")


def logout_view(request):
    """
    Provides an interface for users to log out of the site
    """
    logout(request)
    return HttpResponseRedirect(reverse('index'))


def register(request):
    """
    Provides an interface for a user to register for an account with the site
    """
    if request.method == "POST":
        # Gather the submitted account information
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirmation = request.POST['confirmation']

        # Ensure that the password and confirmation match
        if password != confirmation:
            return render(request, "gencal/register.html", {
                "message": "Passwords must match"
            })

        # Attempt to create the user account
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "gencal/register.html", {
                "message": "Username is already taken"
            })

        # Log in with the newly created account
        login(request, user)
        return HttpResponseRedirect(reverse('index'))

    # Assuming the remainder are get requests
    else:
        return render(request, "gencal/register.html")


def index(request):
    """
    Returns the information page for the project
    """
    return render(request, "gencal/index.html")


def goals(request):
    """
    Returns a page where users can set their goals for materials gathering
    """
    if request.method == "POST":
        # if not request.user.is_authenticated:
        #     # Get a list of all character names that have been implemented
        #     character_names = sorted(list(Character.objects.all().values_list('name', flat=True)))
        #     return render(request, "gencal/goals.html", {
        #         "message": "Must be logged in to enter goals",
        #         "character_names": character_names
        #     })

        character_ascension_goals = []
        character_talent_goals = []
        weapon_ascension_goals = []

        for key in request.POST.keys():
            if 'CharacterAscension' in key:
                # Character ascension
                character_name = key.replace('CharacterAscensionCheck', "")
                character_ascension_goals.append(character_name)
            elif 'CharacterTalent' in key:
                # Character talent goal
                character_name = key.replace('CharacterTalentCheck', "")
                character_talent_goals.append(character_name)
            elif 'WeaponAscension' in key:
                # Weapon ascension goal
                weapon_name = key.replace("WeaponAscensionCheck", "")
                weapon_ascension_goals.append(weapon_name)

        if request.user.is_authenticated:
            # Clear previous goals
            request.user.char_talents.clear()
            request.user.char_ascension.clear()
            request.user.weapon_ascension.clear()

            # Add new goals
            character_ascension_goals_models = Character.objects.filter(name__in=character_ascension_goals)
            request.user.char_ascension.add(*character_ascension_goals_models)
            character_talent_goals_models = Character.objects.filter(name__in=character_talent_goals)
            request.user.char_talents.add(*character_talent_goals_models)
            weapon_ascension_goals_models = Weapon.objects.filter(name__in=weapon_ascension_goals)
            request.user.weapon_ascension.add(*weapon_ascension_goals_models)
        else:
            # Clear previous goals and adds new goals, using Django sessions
            request.session['character_ascension'] = character_ascension_goals
            request.session['character_talents'] = character_talent_goals
            request.session['weapon_ascensions'] = weapon_ascension_goals


    # Get a list of all character names that have been implemented
    character_names = sorted(list(Character.objects.all().values_list('name', flat=True)))
    weapons = {'Bows': [], 'Catalysts': [], 'Claymores': [], 'Polearms': [], 'Swords': []}

    for weapon in Weapon.objects.order_by("name"):
        key = f"{weapon.type.__str__()}s"
        weapons[key].append(weapon)

    return render(request, "gencal/goals.html", {
        "character_names": character_names,
        "weapons": weapons,

    })


def calendar(request):
    """
    Provides the user the ability to see and export a calendar for the availability of the items they need to farm
    """
    # Initialize a data structure to store calendar information
    calendar = {}
    days = Day.objects.all()
    for day in days:
        calendar[day.__str__()] = []

    # Add data for the character talents
    if request.user.is_authenticated:
        character_talents = request.user.char_talents.all()
        weapon_ascensions = request.user.weapon_ascension.all()
    else:
        character_talents = []
        weapon_ascensions = []
        if 'character_talents' in request.session:
            character_talents = Character.objects.filter(name__in=request.session['character_talents'])
        if 'weapon_ascensions' in request.session:
            weapon_ascensions = Weapon.objects.filter(name__in=request.session['weapon_ascensions'])

    for character in character_talents:
        talent_domain = character.talent_domain
        for day in talent_domain.available.all():
            display = f"{talent_domain.name} ({character.name})"
            calendar[day.__str__()].append(display)

    # Add data for the weapon ascensions
    for weapon in weapon_ascensions:
        ascension_domain = weapon.ascension_domain
        for day in ascension_domain.available.all():
            display = f"{ascension_domain.name} ({weapon.name})"
            calendar[day.__str__()].append(display)

    return render(request, "gencal/calendar.html", {
        'calendar': calendar
    })
