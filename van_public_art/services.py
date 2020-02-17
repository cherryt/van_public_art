from abc import ABC, abstractmethod
from sqlalchemy import or_

from van_public_art import app
from van_public_art.models import Artist, Artwork


class PublicArtService(ABC):

    @abstractmethod
    def get_all_items_count(self):
        pass
    
    @abstractmethod
    def get_items_by_page(self, start_item, page_length):
        pass

    @abstractmethod
    def get_filtered_items_count(self, search_value):
        pass

    @abstractmethod
    def get_filtered_items_by_page(self, search_value, start_item, page_length):
        pass

    @abstractmethod
    def _filter_by_search(search_value):
        pass

    def _get_page(start_item, page_length):
        if(page_length < 1):
             raise ZeroDivisionError("page_length cannot be 0")
        return (start_item/page_length)+1


class ArtistService(PublicArtService):

    def get_all_items_count(self):
        return Artist.query.count()

    def get_items_by_page(self, start_item, page_length):
        page = PublicArtService._get_page(start_item, page_length)
        artists = Artist.query.paginate(
            page, page_length, False).items
        return ArtistService._form_results(artists)
    
    def get_filtered_items_count(self, search_value):
        return Artist.query.filter(
            ArtistService._filter_by_search(search_value)
            ).count()

    def get_filtered_items_by_page(self, search_value, start_item, page_length):
        page = PublicArtService._get_page(start_item, page_length)
        artists = Artist.query.filter(
            ArtistService._filter_by_search(search_value)
            ).paginate(
                page, page_length, False).items
        return ArtistService._form_results(artists)
        
    @staticmethod
    def _form_results(data):
        return [
            {
                "name": f"{item.first_name} {item.last_name}",
                "info": item.biography
            } 
            for item in data
        ]

    @staticmethod
    def _filter_by_search(search_value):
        return (
            Artist.first_name.ilike(f"%{search_value}%") |
            Artist.last_name.ilike(f"%{search_value}%")
        )


class ArtworkService(PublicArtService):

    def get_all_items_count(self):
        return Artwork.query.count()
    
    def get_items_by_page(self, start_item, page_length):
        page = PublicArtService._get_page(start_item, page_length)
        artwork = Artwork.query.paginate(
            page, page_length, False).items
        return ArtworkService._form_results(artwork)

    def get_filtered_items_count(self, search_value):
        return Artwork.query.filter(
            ArtworkService._filter_by_search(search_value)
            ).count()

    def get_filtered_items_by_page(self, search_value, start_item, page_length):
        page = PublicArtService._get_page(start_item, page_length)
        artwork = Artwork.query.filter(
            ArtworkService._filter_by_search(search_value)
            ).paginate(
                page, page_length, False).items
        return ArtworkService._form_results(artwork)

    @staticmethod
    def _filter_by_search(search_value):
        return (
            Artwork.title.ilike(f"%{search_value}%") |
            Artwork.address.ilike(f"%{search_value}%") |
            Artwork.neighbourhood.ilike(f"%{search_value}%") |
            Artwork.description.ilike(f"%{search_value}%")
        )

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


class NeighbourhoodArtworkService(ArtworkService):

    def __init__(self, neighbourhood):
        self.neighbourhood = neighbourhood

    def get_all_items_count(self):
        return Artwork.query.filter(Artwork.neighbourhood == self.neighbourhood).count()
    
    def get_items_by_page(self, start_item, page_length):
        page = PublicArtService._get_page(start_item, page_length)
        artwork = Artwork.query.filter(
            Artwork.neighbourhood == self.neighbourhood).paginate(
                page, page_length, False).items
        return ArtworkService._form_results(artwork)
    
    def get_neighbourhoods():
        neighbourhoods = Artwork.get_neighbourhoods().all()
        return [neighbourhood[0] for neighbourhood in neighbourhoods]
    
    def get_filtered_items_count(self, search_value):
         return Artwork.query.filter(
             or_(
                Artwork.neighbourhood == self.neighbourhood,
                ArtworkService._filter_by_search(search_value)
                )).count()

    def get_filtered_items_by_page(self, search_value, start_item, page_length):
        page = PublicArtService._get_page(start_item, page_length)
        artwork = Artwork.query.filter(
            Artwork.neighbourhood == self.neighbourhood
            ).filter(
            ArtworkService._filter_by_search(search_value)
            ).paginate(
                page, page_length, False).items
        return ArtworkService._form_results(artwork)
