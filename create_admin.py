import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gotomarketappbackend.config.settings')
django.setup()

from django.contrib.auth.models import User

# Details yahan bharein
username = 'paras_singh' 
email = 'paras@gmail.com'
password = 'Market@14'

if not User.objects.filter(username=username).exists():
    User.objects.create_superuser(username, email, password)
    print(f"Superuser '{username}' created successfully!")
else:
    print(f"Superuser '{username}' already exists.")