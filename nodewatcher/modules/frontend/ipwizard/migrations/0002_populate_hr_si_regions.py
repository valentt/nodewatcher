# Data migration to populate HR and SI regions
from django.db import migrations


def populate_countries_and_regions(apps, schema_editor):
    Country = apps.get_model('ipwizard', 'Country')
    Region = apps.get_model('ipwizard', 'Region')

    # Croatia
    hr = Country.objects.create(
        code='HR',
        name='Hrvatska',
        flag_emoji='HR',  # Flag code
        ip_prefix=0,  # 10.XX.0.0 where XX = postal prefix
        postal_digits=5,
    )

    # Croatian regions (zupanije)
    hr_regions = [
        ('10', 'Grad Zagreb', 'Zagreb', '10000', 806341),
        ('20', 'Dubrovacko-neretvanska', 'Dubrovnik', '20000', 42615),
        ('21', 'Splitsko-dalmatinska', 'Split', '21000', 178102),
        ('22', 'Sibensko-kninska', 'Sibenik', '22000', 46332),
        ('23', 'Zadarska', 'Zadar', '23000', 75062),
        ('31', 'Osjecko-baranjska', 'Osijek', '31000', 108048),
        ('32', 'Vukovarsko-srijemska', 'Vukovar', '32000', 27683),
        ('33', 'Viroviticko-podravska', 'Virovitica', '33000', 21291),
        ('34', 'Pozesko-slavonska', 'Pozega', '34000', 26248),
        ('35', 'Brodsko-posavska', 'Slavonski Brod', '35000', 59141),
        ('40', 'Medimurska', 'Cakovec', '40000', 27104),
        ('42', 'Varazdinska', 'Varazdin', '42000', 46946),
        ('43', 'Bjelovarsko-bilogorska', 'Bjelovar', '43000', 40276),
        ('44', 'Sisacko-moslavacka', 'Sisak', '44000', 47768),
        ('47', 'Karlovacka', 'Karlovac', '47000', 55705),
        ('48', 'Koprivnicko-krizevacka', 'Koprivnica', '48000', 30872),
        ('49', 'Krapinsko-zagorska', 'Krapina', '49000', 15000),
        ('51', 'Primorsko-goranska', 'Rijeka', '51000', 128624),
        ('52', 'Istarska', 'Pazin', '52000', 57460),
        ('53', 'Licko-senjska', 'Gospic', '53000', 12745),
    ]

    for postal, name, city, postal_code, pop in hr_regions:
        Region.objects.create(
            country=hr,
            postal_prefix=postal,
            name=name,
            main_city=city,
            main_postal_code=postal_code,
            population=pop,
        )

    # Slovenia
    si = Country.objects.create(
        code='SI',
        name='Slovenija',
        flag_emoji='SI',  # Flag code
        ip_prefix=100,  # 10.1XX.0.0 where XX = postal prefix
        postal_digits=4,
    )

    # Slovenian regions
    si_regions = [
        ('10', 'Osrednjeslovenska', 'Ljubljana', '1000', 295504),
        ('20', 'Podravska', 'Maribor', '2000', 95171),
        ('30', 'Savinjska', 'Celje', '3000', 37490),
        ('40', 'Gorenjska', 'Kranj', '4000', 37373),
        ('50', 'Goriska', 'Nova Gorica', '5000', 13000),
        ('60', 'Obalno-kraska', 'Koper', '6000', 25753),
        ('80', 'Jugovzhodna Slovenija', 'Novo Mesto', '8000', 24000),
        ('90', 'Pomurska', 'Murska Sobota', '9000', 11000),
    ]

    for postal, name, city, postal_code, pop in si_regions:
        Region.objects.create(
            country=si,
            postal_prefix=postal,
            name=name,
            main_city=city,
            main_postal_code=postal_code,
            population=pop,
        )


def reverse_populate(apps, schema_editor):
    Country = apps.get_model('ipwizard', 'Country')
    Country.objects.filter(code__in=['HR', 'SI']).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('ipwizard', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(populate_countries_and_regions, reverse_populate),
    ]
