from abc import ABC, abstractmethod

from van_public_art import app
from van_public_art.models import Artist, Artwork

class PublicArtService(ABC):

    @abstractmethod
    def get_all_items_count(self):
        pass
    
    @abstractmethod
    def get_items_by_page(self, startItem, pageLength):
        pass


class ArtistService(PublicArtService):

    def get_all_items_count(self):
        return Artist.query.count()

    def get_items_by_page(self, startItem, pageLength):
        page = (startItem/pageLength)+1
        artists = Artist.query.paginate(
            page, pageLength, False).items
        results = [
            {
                "name": f"{artist.first_name} {artist.last_name}",
                "info": artist.biography
            } for artist in artists
        ]
        return results


class ArtworkService(PublicArtService):

    @staticmethod
    def _form_results(data):
        return [
            {
                "id": item.id,
                "title": item.title,
                "address": item.address,
                "neighbourhood": item.neighbourhood,
                "info": item.description
            }
            for item in data
        ]

    def get_all_items_count(self):
        return Artwork.query.count()
    
    def get_items_by_page(self, startItem, pageLength):
        page = (startItem/pageLength)+1
        artwork = Artwork.query.paginate(
            page, pageLength, False).items
        return ArtworkService._form_results(artwork)


class NeighbourhoodArtworkService(ArtworkService):

    def __init__(self, neighbourhood):
        self.neighbourhood = neighbourhood

    def get_all_items_count(self):
        return Artwork.query.filter(Artwork.neighbourhood == self.neighbourhood).count()
    
    def get_items_by_page(self, startItem, pageLength):
        page = (startItem/pageLength)+1
        artwork = Artwork.query.filter(
            Artwork.neighbourhood == self.neighbourhood).paginate(
                page, pageLength, False).items
        return ArtworkService._form_results(artwork)
    
    def get_neighbourhoods():
        neighbourhoods = Artwork.get_neighbourhoods().all()
        return [neighbourhood[0] for neighbourhood in neighbourhoods]
