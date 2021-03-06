# Generated by Django 3.2.4 on 2021-08-19 23:07

import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='BossItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
            ],
        ),
        migrations.CreateModel(
            name='Day',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(choices=[('0', 'Monday'), ('1', 'Tuesday'), ('2', 'Wednesday'), ('3', 'Thursday'), ('4', 'Friday'), ('5', 'Saturday'), ('6', 'Sunday')], max_length=1)),
            ],
        ),
        migrations.CreateModel(
            name='DomainItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
                ('available', models.ManyToManyField(blank=True, related_name='available_domain_items', to='gencal.Day')),
            ],
        ),
        migrations.CreateModel(
            name='Element',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(choices=[(0, 'Anemo'), (1, 'Cryo'), (2, 'Dendro'), (3, 'Electro'), (4, 'Geo'), (5, 'Hydro'), (6, 'Pyro')], max_length=1)),
            ],
        ),
        migrations.CreateModel(
            name='WeeklyItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
            ],
        ),
        migrations.CreateModel(
            name='WorldItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
            ],
        ),
        migrations.CreateModel(
            name='Weapon',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField(max_length=64)),
                ('ascension_domain', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gencal.domainitem')),
                ('ascension_first', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='weapon_ascension_first', to='gencal.worlditem')),
                ('ascension_second', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='weapon_ascension_second', to='gencal.worlditem')),
            ],
        ),
        migrations.CreateModel(
            name='Character',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField(max_length=64)),
                ('ascension_boss', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='character_boss_drops', to='gencal.bossitem')),
                ('ascension_dropped', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='character_ascension_dropped', to='gencal.worlditem')),
                ('ascension_farmed', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='character_ascension_farmed', to='gencal.worlditem')),
                ('ascension_gem', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='character_gems', to='gencal.bossitem')),
                ('talent_domain', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gencal.domainitem')),
                ('talent_dropped', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gencal.worlditem')),
                ('talent_weekly', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gencal.weeklyitem')),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('char_ascension', models.ManyToManyField(blank=True, related_name='users_building_ascension', to='gencal.Character')),
                ('char_talents', models.ManyToManyField(blank=True, related_name='users_building_talents', to='gencal.Character')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
                ('weapon_ascension', models.ManyToManyField(blank=True, related_name='users_building_weapon', to='gencal.Weapon')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
    ]
