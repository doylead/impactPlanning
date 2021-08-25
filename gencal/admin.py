from django.contrib import admin

from .models import User, Character, Weapon, DomainItem, WorldItem, GemItem, BossItem, WeeklyItem, Day, Element, StarRating, WeaponType

# Sorting schemes
class WorldItemAdmin(admin.ModelAdmin):
    ordering = ['name']


class DomainItemAdmin(admin.ModelAdmin):
    ordering = ['name']

# Register your models here.
admin.site.register(User)
admin.site.register(Character)
admin.site.register(Weapon)
admin.site.register(DomainItem, DomainItemAdmin)
admin.site.register(WorldItem, WorldItemAdmin)
admin.site.register(GemItem)
admin.site.register(BossItem)
admin.site.register(WeeklyItem)

# "Static" Models
admin.site.register(Day)
admin.site.register(Element)
admin.site.register(StarRating)
admin.site.register(WeaponType)