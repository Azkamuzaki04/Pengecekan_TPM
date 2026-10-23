# Existing project did not have an accounts migration; this migration only records the app's UserProfile dependency safely.
from django.db import migrations
class Migration(migrations.Migration):
    initial = True
    dependencies = []
    operations = []
