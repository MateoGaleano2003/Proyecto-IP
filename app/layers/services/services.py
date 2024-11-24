# capa de servicio/lógica de negocio

from ..persistence import repositories
from ..utilities import translator
from django.contrib.auth import get_user
from ..transport import transport
from app.models import Favourite

def getAllImages(input=None):
    # obtiene un listado de datos "crudos" desde la API, usando a transport.py.
    json_collection = transport.getAllImages(input)


    # recorre cada dato crudo de la colección anterior, lo convierte en una Card y lo agrega a images.
    images = []
    for elem in json_collection:
        card = translator.fromRequestIntoCard(elem)
        images.append(card)

    return images

# añadir favoritos (usado desde el template 'home.html')
def saveFavourite(request):
    for elem in request:
        card = translator.fromRepositoryIntoCard(elem) # transformamos un request del template en una Card.
        user = get_user(request) # le asignamos el usuario correspondiente.

    return repositories.saveFavourite(card) # lo guardamos en la base.

# usados desde el template 'favourites.html'
def getAllFavourites(request):
    if not request.user.is_authenticated:
        return []
    else:
        user = get_user(request)

        favourite_list = Favourite.objects.filter(user=user).values('id', 'url', 'name', 'status', 'last_location', 'first_seen') # buscamos desde el repositories.py TODOS los favoritos del usuario (variable 'user').
        mapped_favourites = []

        for favourite in favourite_list:
            card = translator.fromRequestIntoCard(favourite) # transformamos cada favorito en una Card, y lo almacenamos en card.
            mapped_favourites.append(card)

        return mapped_favourites

def deleteFavourite(request):
    favId = translator.fromRepositoryIntoCard('id')
    return repositories.deleteFavourite(favId) # borramos un favorito por su ID.