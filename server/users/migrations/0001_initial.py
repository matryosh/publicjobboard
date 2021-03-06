# Generated by Django 3.1 on 2021-10-20 22:33

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import phonenumber_field.modelfields
import users.models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomUser',
            fields=[
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('phone_number', phonenumber_field.modelfields.PhoneNumberField(blank=True, max_length=128, region=None)),
                ('user_number', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('photo', models.ImageField(blank=True, null=True, upload_to='media/photos')),
                ('user_type', models.CharField(choices=[('JB', 'Jobseeker'), ('CM', 'Company')], default='JB', max_length=2)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', users.models.CustomUserManager()),
            ],
        ),
        migrations.CreateModel(
            name='CompanyModel',
            fields=[
                ('company_name', models.CharField(blank=True, max_length=128)),
                ('description', models.CharField(blank=True, max_length=512)),
                ('company_id', models.SlugField(default='', max_length=128, primary_key=True, serialize=False)),
                ('user', models.OneToOneField(default='', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='JobExperienceModel',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('position', models.CharField(max_length=128)),
                ('company', models.CharField(blank=True, max_length=128)),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='JobSeekerModel',
            fields=[
                ('first_name', models.CharField(blank=True, max_length=128)),
                ('last_name', models.CharField(blank=True, max_length=128)),
                ('user_bio', models.CharField(blank=True, max_length=1200)),
                ('jobseeker_id', models.SlugField(default='', max_length=128, primary_key=True, serialize=False)),
                ('job_experience', models.ForeignKey(blank=True, default='', null=True, on_delete=django.db.models.deletion.CASCADE, to='users.jobexperiencemodel')),
                ('user', models.OneToOneField(default='', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='SkillModel',
            fields=[
                ('skill', models.CharField(max_length=64)),
                ('years', models.IntegerField()),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('jobseeker', models.ForeignKey(blank=True, default='', null=True, on_delete=django.db.models.deletion.CASCADE, to='users.jobseekermodel')),
            ],
        ),
        migrations.CreateModel(
            name='JobListingModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_type', models.CharField(choices=[('OP', 'Open'), ('CL', 'Closed')], default='OP', max_length=2)),
                ('title', models.CharField(max_length=128)),
                ('job_overview', models.TextField(blank=True, max_length=250)),
                ('qualifications', models.TextField()),
                ('responsibilities', models.TextField()),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.companymodel')),
            ],
        ),
        migrations.CreateModel(
            name='JobApplicationModel',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('cover_letter', models.TextField(blank=True)),
                ('applicant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.jobseekermodel')),
                ('job', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.joblistingmodel')),
            ],
        ),
    ]
