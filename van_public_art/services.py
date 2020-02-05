from van_public_art.models import Artist, Artwork

class ArtistService():

    def get_all_artists():
        artists = Artist.query.all()
        results = [
            {
                "id": artist.id,
                "name": f"{artist.first_name} {artist.last_name}",
                "info": artist.biography
            } for artist in artists
        ]
        return results

class ArtworkService():

    def form_results(data):
        results = [
            {
                "id": item.id,
                "title": item.title,
                "address": item.address,
                "neighbourhood": item.neighbourhood,
                "info": item.description
            } for item in data
        ]
        return results

    def get_all_artwork():
        artworks = Artwork.query.all()
        results = [
            {
                "id": item.id,
                "title": item.title,
                "address": item.address,
                "neighbourhood": item.neighbourhood,
                "info": item.description
            } for item in artworks
        ]
        return results
    
    def get_artwork_by_neighbourhood(neighbourhood):
        artworks = Artwork.query.filter((Artwork.neighbourhood == neighbourhood))
        results = [
            {
                "id": item.id,
                "title": item.title,
                "address": item.address,
                "neighbourhood": item.neighbourhood,
                "info": item.description
            } for item in artworks
        ]
        return results
