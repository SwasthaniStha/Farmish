from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('product', '0005_alter_product_id_alter_product_lifespan'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='rate',
            field=models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Rate (NPR)'),
        ),
    ]
