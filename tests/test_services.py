# from unittest import mock
# from unittest.mock import MagicMock

# import pytest

# from van_public_art.models import Artist
# from van_public_art.services import ArtistService


# class TestArtistService:
#     @pytest.fixture(scope="session")
#     def test_artists(self):
#         return [
#             Artist(0, "first", "last", "info"),
#             Artist(1, "first1", "last1", "info1"),
#             Artist(2, "first2", "last2", "info2"),
#         ]

#     def test_get_all_items_count(self, mocker):
#         # given
#         mocker.patch.object(Artist.query, "count", return_value=1)

#         # when
#         result = ArtistService().get_all_items_count()

#         # then
#         assert result == 1

#     @mock.patch("flask_sqlalchemy._QueryProperty.__get__")
#     def test_get_items_by_page(self, query_mock):
#         test_artists = TestArtistService.test_artists
#         query_mock.return_value.paginate.return_value.items = test_artists
#         results = ArtistService().get_items_by_page(1, 1)
#         expected = [
#             {
#                 "name": f"{test_artists[0].first_name} {test_artists[0].last_name}",
#                 "info": test_artists[0].biography,
#             },
#             {
#                 "name": f"{test_artists[1].first_name} {test_artists[1].last_name}",
#                 "info": test_artists[1].biography,
#             },
#             {
#                 "name": f"{test_artists[2].first_name} {test_artists[2].last_name}",
#                 "info": test_artists[2].biography,
#             },
#         ]
#         assert results == expected

#     @mock.patch("flask_sqlalchemy._QueryProperty.__get__")
#     def test_get_items_by_page_if_empty_results(self, query_mock):
#         query_mock.return_value.paginate.return_value.items = []
#         results = ArtistService().get_items_by_page(1, 1)
#         expected = []
#         assert results == expected

#     @mock.patch.object(Artist, "first_name")
#     @mock.patch.object(Artist, "last_name")
#     @mock.patch("flask_sqlalchemy._QueryProperty.__get__")
#     def test_get_filtered_items_by_page(
#         self, query_mock, last_name_mock, first_name_mock
#     ):
#         test_artists = TestArtistService.test_artists
#         query_mock.return_value.paginate.return_value.items = test_artists
#         search_term = "search"
#         results = ArtistService().get_filtered_items_by_page(search_term, 1, 1)
#         Artist.first_name.ilike.assert_called_with(f"%{search_term}%")
#         Artist.last_name.ilike.assert_called_with(f"%{search_term}%")
#         # last_name_mock.ilike.assert_called_with(f"%{search_term}%")
