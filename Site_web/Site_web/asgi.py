list
import os

from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Site_web.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    # Vous pouvez ajouter d'autres protocoles comme websocket ici
})