# Generated migration for IP Wizard models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('projects', '0001_initial'),
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Country',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(help_text='ISO 3166-1 alpha-2 code', max_length=2, unique=True)),
                ('name', models.CharField(max_length=100)),
                ('flag_emoji', models.CharField(blank=True, max_length=4)),
                ('ip_prefix', models.IntegerField(default=0, help_text="Added to region's first 2 postal digits to get second octet. E.g., 0 for HR, 100 for SI")),
                ('postal_digits', models.IntegerField(default=5, help_text='Number of digits in postal code (5 for HR, 4 for SI)')),
            ],
            options={
                'verbose_name_plural': 'Countries',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Region',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('postal_prefix', models.CharField(help_text='First 2 digits of postal code', max_length=2)),
                ('main_city', models.CharField(max_length=100)),
                ('main_postal_code', models.CharField(max_length=10)),
                ('population', models.IntegerField(default=0)),
                ('country', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='regions', to='ipwizard.Country')),
            ],
            options={
                'ordering': ['country', 'postal_prefix'],
                'unique_together': {('country', 'postal_prefix')},
            },
        ),
        migrations.CreateModel(
            name='ProjectPoolSettings',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('default_prefix', models.IntegerField(default=28, help_text='Default prefix length for user allocations (e.g., 28 = /28 = 14 clients)')),
                ('self_service_max_prefix', models.IntegerField(default=26, help_text='Largest allocation without sheriff approval (e.g., 26 = /26 = 62 clients)')),
                ('name', models.CharField(blank=True, help_text='Custom name for this pool', max_length=100)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pool_settings', to='projects.Project')),
                ('pool', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='project_settings', to='core.IpPool')),
                ('region', models.ForeignKey(blank=True, help_text='Region this pool was created from (if using simple mode)', null=True, on_delete=django.db.models.deletion.SET_NULL, to='ipwizard.Region')),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='created_pool_settings', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Project Pool Settings',
                'verbose_name_plural': 'Project Pool Settings',
                'unique_together': {('project', 'pool')},
            },
        ),
        migrations.CreateModel(
            name='UserAllocationRequest',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('requested_prefix', models.IntegerField()),
                ('reason', models.TextField(blank=True)),
                ('status', models.CharField(choices=[('pending', 'Pending'), ('approved', 'Approved'), ('rejected', 'Rejected')], default='pending', max_length=20)),
                ('sheriff_comment', models.TextField(blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('approved_at', models.DateTimeField(blank=True, null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ip_allocation_requests', to=settings.AUTH_USER_MODEL)),
                ('pool_settings', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='allocation_requests', to='ipwizard.ProjectPoolSettings')),
                ('allocated_pool', models.ForeignKey(blank=True, help_text='The actual allocated subnet from the pool', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='allocation_requests', to='core.IpPool')),
                ('approved_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='approved_allocations', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
    ]
