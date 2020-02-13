# from flask_sqlalchemy import SignallingSession

# from van_public_art.models import Artwork


# class TestArtwork:
#     def test_get_neighbourhoods(self, mocker):
#         test_artworks = [
#             Artwork(1, "title1", "address1", "neighbourhood1", "info1"),
#             Artwork(2, "title2", "address2", None, "info2"),
#         ]
#         mocker.patch.object(SignallingSession, "query", return_value=test_artworks)
#         result = Artwork.get_neighbourhoods()
#         assert len(result.all()) == 1
