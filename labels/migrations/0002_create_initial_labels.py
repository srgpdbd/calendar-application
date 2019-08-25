from django.db import migrations


INITIAL_LABELS = ['XS', 'S', 'M', 'L', 'XL', 'XXL']


def populate_labels(apps, schema_editor):
    Label = apps.get_model('labels', 'Label')
    for label_name in INITIAL_LABELS:
        Label.objects.create(name=label_name)


class Migration(migrations.Migration):

    dependencies = [
        ('labels', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(populate_labels),
    ]
