import django
import os

os.environ['DJANGO_SETTINGS_MODULE'] = "resto_server.settings"
django.setup()

from django.contrib.auth.models import User

if __name__ == "__main__":
    try:
        user = User.objects.get(username='ericbg@gmail.com', email='ericbg@gmail.com', 
                                            first_name="Eric", last_name="May")
    except User.DoesNotExist:
        user = User.objects.create_user(username='ericbg@gmail.com', email='ericbg@gmail.com', password='password',
                                            first_name="Eric", last_name="May")        

