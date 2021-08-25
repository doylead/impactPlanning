from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.
class User(AbstractUser):
    """
    A model for user registration, extending from AbstractUser
    """
    # Tracks who this user's goals
    char_talents = models.ManyToManyField("Character", blank=True, related_name="users_building_talents")
    char_ascension = models.ManyToManyField("Character", blank=True, related_name="users_building_ascension")
    weapon_ascension = models.ManyToManyField("Weapon", blank=True, related_name="users_building_weapon")

    # Provides a representation of a user
    def __str__(self):
        return self.username


class Character(models.Model):
    """
    A model for in-game characters
    """
    # Basic information about the character
    name = models.CharField(max_length=64)
    # element
    # weapon_type
    # rarity

    # Materials needed to raise talent levels
    talent_domain = models.ForeignKey("DomainItem", on_delete=models.CASCADE)
    talent_dropped = models.ForeignKey("WorldItem", on_delete=models.CASCADE)
    talent_weekly = models.ForeignKey("WeeklyItem", on_delete=models.CASCADE)

    # Materials needed to ascend characters/gain levels
    ascension_gem = models.ForeignKey("GemItem", on_delete=models.CASCADE, related_name="character_gems")
    ascension_boss = models.ForeignKey("BossItem", on_delete=models.CASCADE, related_name="character_boss_drops")
    ascension_farmed = models.ForeignKey("WorldItem", on_delete=models.CASCADE, related_name="character_ascension_farmed")
    ascension_dropped = models.ForeignKey("WorldItem", on_delete=models.CASCADE, related_name="character_ascension_dropped")

    # Provides a representation of a character
    def __str__(self):
        return self.name


class Weapon(models.Model):
    """
    A model to represent information about in-game weapons
    """
    # Basic information about the weapon
    name = models.CharField(max_length=64)
    type = models.ForeignKey("WeaponType", on_delete=models.CASCADE, related_name="weapons_by_type")
    rarity = models.ForeignKey("StarRating", on_delete=models.CASCADE, related_name="weapons_by_rarity")

    # Materials needed to ascend weapons/gain levels
    ascension_domain = models.ForeignKey("DomainItem", on_delete=models.CASCADE)
    ascension_first = models.ForeignKey("WorldItem", on_delete=models.CASCADE, related_name="weapon_ascension_first")
    ascension_second = models.ForeignKey("WorldItem", on_delete=models.CASCADE, related_name="weapon_ascension_second")

    # Provides a representation of a weapon
    def __str__(self):
        return f"{self.name} ({self.rarity})"


class DomainItem(models.Model):
    """
    A model to represent items dropped in domains
    """
    name = models.CharField(max_length=64)
    # location
    available = models.ManyToManyField("Day", blank=True, related_name="available_domain_items")

    # Provides a representation of a DomainItem
    def __str__(self):
        return self.name


class WorldItem(models.Model):
    """
    A model to represent items dropped or farmed in the open world
    """
    name = models.CharField(max_length=64)

    # Provides a representation of a WorldItem
    def __str__(self):
        return self.name


class GemItem(models.Model):
    """
    A model to represent the various gems used (dropped by bosses and available in souvenir shops)
    """
    name = models.CharField(max_length=64)

    # Provides a representation of a GemItem
    def __str__(self):
        return self.name


class BossItem(models.Model):
    """
    A model to represent items dropped from open world bosses
    """
    name = models.CharField(max_length=64)
    # dropped_by

    # Provides a representation of a BossItem
    def __str__(self):
        return self.name


class WeeklyItem(models.Model):
    """
    A model to represent items dropped from weekly bosses
    """
    name = models.CharField(max_length=64)
    # dropped_by

    # Provides a representation of a WeeklyItem
    def __str__(self):
        return self.name


#---------------------------------------------------------#
# "Static" models (values not expected to change after    #
# initialization)                                         #
#---------------------------------------------------------#

class Day(models.Model):
    """
    A model to represent a day
    """
    DAYS_OF_WEEK = (
        ('0', ('Monday') ),
        ('1', ('Tuesday') ),
        ('2', ('Wednesday') ),
        ('3', ('Thursday') ),
        ('4', ('Friday') ),
        ('5', ('Saturday') ),
        ('6', ('Sunday') )
    )
    name = models.CharField(max_length=1, choices=DAYS_OF_WEEK)

    # Provide a representation of a day
    def __str__(self):
        DAYS_OF_WEEK = {
            '0': 'Monday',
            '1': 'Tuesday',
            '2': 'Wednesday',
            '3': 'Thursday',
            '4': 'Friday',
            '5': 'Saturday',
            '6': 'Sunday'
        }
        return DAYS_OF_WEEK[self.name]


class Element(models.Model):
    """
    A model to represent an element ("element" referring to characters' elemental abilities)
    """
    ELEMENTS_AVAILABLE = (
        ('0', ('Anemo')),
        ('1', ('Cryo')),
        ('2', ('Dendro')),
        ('3', ('Electro')),
        ('4', ('Geo')),
        ('5', ('Hydro')),
        ('6', ('Pyro')),
        ('7', ('Traveler'))
    )
    name = models.CharField(max_length=1, choices=ELEMENTS_AVAILABLE)

    # Provide a representaiton of an element
    def __str__(self):
        ELEMENTS_AVAILABLE = {
            '0': 'Anemo',
            '1': 'Cryo',
            '2': 'Dendro',
            '3': 'Electro',
            '4': 'Geo',
            '5': 'Hydro',
            '6': 'Pyro',
            '7': 'Traveler'
        }
        return ELEMENTS_AVAILABLE[self.name]


class StarRating(models.Model):
    """
    A model to represent the rarity of some objects like characters or weapons
    """
    STAR_RATINGS_AVAILABLE = (
        ('0', ('No Stars')),
        ('1', ('1 Star')),
        ('2', ('2 Stars')),
        ('3', ('3 Stars')),
        ('4', ('4 Stars')),
        ('5', ('5 Stars'))
    )
    rating = models.CharField(max_length=1, choices=STAR_RATINGS_AVAILABLE)

    # Provides a representation of a StarRating
    def __str__(self):
        STAR_RATINGS_AVAILABLE = {
            '0': 'No Stars',
            '1': '1 Star',
            '2': '2 Stars',
            '3': '3 Stars',
            '4': '4 Stars',
            '5': '5 Stars'
        }
        return STAR_RATINGS_AVAILABLE[self.rating]


class WeaponType(models.Model):
    """
    A model to represent weapon types
    """
    WEAPON_TYPES_AVAILABLE = (
        ('0', ('Bow')),
        ('1', ('Catalyst')),
        ('2', ('Claymore')),
        ('3', ('Polearm')),
        ('4', ('Sword'))
    )
    type = models.CharField(max_length=1, choices=WEAPON_TYPES_AVAILABLE)

    # Provides a representation of a WeaponType
    def __str__(self):
        WEAPON_TYPES_AVAILABLE = {
            '0': 'Bow',
            '1': 'Catalyst',
            '2': 'Claymore',
            '3': 'Polearm',
            '4': 'Sword'
        }
        return WEAPON_TYPES_AVAILABLE[self.type]
