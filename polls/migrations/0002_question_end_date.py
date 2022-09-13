import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='end_date',
            field=models.DateTimeField(default=datetime.datetime(2022, 9, 14, 9, 00, 00, 592223, tzinfo=utc), verbose_name='date end'),
        ),
    ]