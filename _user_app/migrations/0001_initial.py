# Generated by Django 5.1.6 on 2025-03-09 20:01

import django.contrib.auth.models
import django.contrib.auth.validators
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("auth", "0012_alter_user_first_name_max_length"),
    ]

    operations = [
        migrations.CreateModel(
            name="CustomUser",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("password", models.CharField(max_length=128, verbose_name="password")),
                (
                    "last_login",
                    models.DateTimeField(
                        blank=True, null=True, verbose_name="last login"
                    ),
                ),
                (
                    "username",
                    models.CharField(
                        error_messages={
                            "unique": "A user with that username already exists."
                        },
                        help_text="Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.",
                        max_length=150,
                        unique=True,
                        validators=[
                            django.contrib.auth.validators.UnicodeUsernameValidator()
                        ],
                        verbose_name="username",
                    ),
                ),
                (
                    "first_name",
                    models.CharField(
                        blank=True, max_length=150, verbose_name="first name"
                    ),
                ),
                (
                    "last_name",
                    models.CharField(
                        blank=True, max_length=150, verbose_name="last name"
                    ),
                ),
                (
                    "email",
                    models.EmailField(
                        blank=True, max_length=254, verbose_name="email address"
                    ),
                ),
                (
                    "date_joined",
                    models.DateTimeField(
                        default=django.utils.timezone.now, verbose_name="date joined"
                    ),
                ),
                (
                    "gender",
                    models.CharField(
                        blank=True,
                        choices=[("M", "Male"), ("F", "Female")],
                        max_length=1,
                        null=True,
                    ),
                ),
                (
                    "phone_number",
                    models.CharField(blank=True, max_length=15, null=True),
                ),
                ("birthdate", models.DateField(blank=True, null=True)),
                (
                    "status",
                    models.CharField(
                        choices=[("A", "Active"), ("I", "Inactive"), ("P", "Pending")],
                        default="P",
                        max_length=1,
                    ),
                ),
                (
                    "role",
                    models.CharField(
                        choices=[("C", "Customer"), ("S", "Seller"), ("A", "Admin")],
                        default="C",
                        max_length=1,
                    ),
                ),
                (
                    "image_avatar",
                    models.ImageField(
                        blank=True, null=True, upload_to="image_avatars/"
                    ),
                ),
                ("is_superuser", models.BooleanField(default=False)),
                ("is_staff", models.BooleanField(default=False)),
                ("is_active", models.BooleanField(default=True)),
                ("groups", models.ManyToManyField(blank=True, to="auth.group")),
                (
                    "user_permissions",
                    models.ManyToManyField(blank=True, to="auth.permission"),
                ),
            ],
            options={
                "db_table": "user",
            },
            managers=[
                ("objects", django.contrib.auth.models.UserManager()),
            ],
        ),
    ]
