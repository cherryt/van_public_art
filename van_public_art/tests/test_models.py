from unittest import mock

from van_public_art import db
from van_public_art.models import Artwork



class TestModels:

    @mock.patch.object(db, 'session')
    def test_get_neighbourhoods(self, session_mock):
        test_artworks = [
            Artwork(1, "title1", "address1", "neighbourhood1", "info1"),
            Artwork(2, "title2", "address2", None, "info2")
            ]
        session_mock.return_value.query.return_value = test_artworks
        neighbourhoods = Artwork.get_neighbourhoods()
        assert(len(neighbourhoods.all()) == 1)