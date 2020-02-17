import pytest

from van_public_art.models import Artist, Artwork
from van_public_art.services import ArtistService, ArtworkService, NeighbourhoodArtworkService


class TestServiceHelper:

    def __init__(self, model, service):
        self.model = model
        self.service = service

    def test_get_all_items_count(self):
        self.model.query.count.return_value = 1
        result = self.service.get_all_items_count()
        assert result == 1

    def get_items_by_page(self, test_items):
        self.model.query.paginate.return_value.items = test_items
        return self.service.get_items_by_page(1,2)

    def test_get_items_by_page_when_empty_results(self):
        self.model.query.paginate.return_value.items = []
        results = self.service.get_items_by_page(1,1)
        expected = []
        assert results == expected
    
    def test_get_items_by_page_when_page_length_is_zero(self):
        self.model.query.paginate.return_value.items = []
        with pytest.raises(ZeroDivisionError) as ex:
            self.service.get_items_by_page(1, 0)

        assert "page_length cannot be 0" == str(ex.value)

    def test_get_filtered_items_by_page_when_page_length_zero(
        self, test_items):
        self.model.query.paginate.return_value.items = test_items

        with pytest.raises(ZeroDivisionError) as ex:
            self.service.get_filtered_items_by_page("test", 1, 0)
        assert "page_length cannot be 0" == str(ex.value)


class TestArtistService:

    @pytest.fixture(scope="session")
    def test_artists(self):
        return [
            Artist(0, "first", "last", "info"),
            Artist(1, "first1", "last1", "info1"),
            Artist(2, "first2", "last2", "info2"),
        ]

    @pytest.fixture(scope="function", autouse=True)
    def set_up_mocks_and_helper(self, mocker):
        mocker.patch.object(Artist, 'query')
        self.test_service = TestServiceHelper(Artist, ArtistService())

    def test_get_all_items_count(self):
        self.test_service.test_get_all_items_count()

    def test_get_items_by_page(self, test_artists):
        results = self.test_service.get_items_by_page(test_artists)
        expected = [
            {
                "name" : f"{test_artists[0].first_name} {test_artists[0].last_name}",
                "info": test_artists[0].biography
            },
            {
                "name" : f"{test_artists[1].first_name} {test_artists[1].last_name}",
                "info": test_artists[1].biography
            },
            {
                "name" : f"{test_artists[2].first_name} {test_artists[2].last_name}",
                "info": test_artists[2].biography
            }
        ]
        assert sorted(results, key=lambda r: r["name"]) == sorted(expected, key=lambda e: e["name"])

    def test_get_items_by_page_when_empty_results(self):
        self.test_service.test_get_items_by_page_when_empty_results()

    def test_get_items_by_page_when_page_length_is_zero(self):
        self.test_service.test_get_items_by_page_when_page_length_is_zero()

    def test_get_filtered_items_by_page(self, mocker, test_artists):
        Artist.query.paginate.return_value.items = test_artists
        mocker.patch.object(Artist, "first_name")
        mocker.patch.object(Artist, "last_name")

        search_term = 'search'
        results = ArtistService().get_filtered_items_by_page(search_term, 1, 1)
        
        Artist.first_name.ilike.assert_called_with(f"%{search_term}%")
        Artist.last_name.ilike.assert_called_with(f"%{search_term}%")

    def test_get_filtered_items_by_page_when_page_length_zero(
        self, test_artists):
        self.test_service.test_get_filtered_items_by_page_when_page_length_zero(test_artists)


class TestArtworkService:

    @pytest.fixture(scope="session")
    def test_artwork(self):
        return [
            Artwork(1, "title", "address", "neighbourhood", "info"),
            Artwork(2, "title2", "address2", "neighbourhood2", "info2"),
        ]

    @pytest.fixture(scope="function", autouse=True)
    def set_up_mocks_and_helper(self, mocker):
        mocker.patch.object(Artwork, 'query')
        self.test_service = TestServiceHelper(Artwork, ArtworkService())

    def test_get_all_items_count(self):
        self.test_service.test_get_all_items_count()
        
    def test_get_items_by_page(self, test_artwork):
        results = self.test_service.get_items_by_page(test_artwork)
        expected = [
            {
                "id": test_artwork[0].id,
                "title" : test_artwork[0].title,
                "address" : test_artwork[0].address,
                "neighbourhood": test_artwork[0].neighbourhood,
                "info": test_artwork[0].description
            },
            {
                "id": test_artwork[1].id,
                "title" : test_artwork[1].title,
                "address" : test_artwork[1].address,
                "neighbourhood": test_artwork[1].neighbourhood,
                "info": test_artwork[1].description
            }
        ]
        assert sorted(results, key=lambda r: r["id"]) == sorted(expected, key=lambda e: e["id"])

    def test_get_items_by_page_when_empty_results(self):
        self.test_service.test_get_items_by_page_when_empty_results()
        
    def test_get_items_by_page_when_page_length_is_zero(self):
        self.test_service.test_get_items_by_page_when_page_length_is_zero()
        
    def test_get_filtered_items_by_page(self, mocker, test_artwork):
        Artwork.query.paginate.return_value.items = test_artwork
        mocker.patch.object(Artwork, "title")
        mocker.patch.object(Artwork, "address")
        mocker.patch.object(Artwork, "neighbourhood")
        mocker.patch.object(Artwork, "description")

        search_term = 'search'
        results = ArtworkService().get_filtered_items_by_page(search_term, 1, 1)
        
        Artwork.title.ilike.assert_called_with(f"%{search_term}%")
        Artwork.address.ilike.assert_called_with(f"%{search_term}%")
        Artwork.neighbourhood.ilike.assert_called_with(f"%{search_term}%")
        Artwork.description.ilike.assert_called_with(f"%{search_term}%")

    def test_get_filtered_items_by_page_when_page_length_zero(
        self, test_artwork):
        self.test_service.test_get_filtered_items_by_page_when_page_length_zero(test_artwork)


class TestNeighbourhoodArtworkService():

    @pytest.fixture(scope="session")
    def test_artwork(self):
        return [
            Artwork(1, "title", "address", "neighbourhood", "info"),
            Artwork(2, "title2", "address2", "neighbourhood2", "info2"),
        ]

    @pytest.fixture(scope="function", autouse=True)
    def set_up_mocks_and_helper(self, mocker):
        mocker.patch.object(Artwork, 'query')
        Artwork.query.filter.return_value.count.return_value = 1
        Artwork.query.filter.return_value.paginate.return_value.items = []
        self.test_service = TestServiceHelper(
            Artwork, NeighbourhoodArtworkService('testNeighbourhood'))

    def test_get_neighbourhood(self, mocker):
        mocker.patch.object(Artwork, 'get_neighbourhoods')
        Artwork.get_neighbourhoods.return_value.all.return_value = ["n", "n2"]
        results = NeighbourhoodArtworkService.get_neighbourhoods()
        assert results

    def test_get_all_items_count(self):
        self.test_service.test_get_all_items_count()
        
    def test_get_items_by_page(self, test_artwork):
        Artwork.query.filter.return_value.paginate.return_value.items = test_artwork
        results = self.test_service.service.get_items_by_page(1, 2)
        expected = [
            {
                "id": test_artwork[0].id,
                "title" : test_artwork[0].title,
                "address" : test_artwork[0].address,
                "neighbourhood": test_artwork[0].neighbourhood,
                "info": test_artwork[0].description
            },
            {
                "id": test_artwork[1].id,
                "title" : test_artwork[1].title,
                "address" : test_artwork[1].address,
                "neighbourhood": test_artwork[1].neighbourhood,
                "info": test_artwork[1].description
            }
        ]
        assert sorted(
            results, key=lambda r: r["id"]
            ) == sorted(
            expected, key=lambda e: e["id"]
            )

    def test_get_items_by_page_when_empty_results(self):
        self.test_service.test_get_items_by_page_when_empty_results()
        
    def test_get_items_by_page_when_page_length_is_zero(self):
        self.test_service.test_get_items_by_page_when_page_length_is_zero()
        
    def test_get_filtered_items_by_page(self, mocker, test_artwork):
        Artwork.query.filter.return_value.paginate.return_value.items = test_artwork
        mocker.patch.object(Artwork, "title")
        mocker.patch.object(Artwork, "address")
        mocker.patch.object(Artwork, "neighbourhood")
        mocker.patch.object(Artwork, "description")

        search_term = 'search'
        results = ArtworkService().get_filtered_items_by_page(search_term, 1, 1)
        
        Artwork.title.ilike.assert_called_with(f"%{search_term}%")
        Artwork.address.ilike.assert_called_with(f"%{search_term}%")
        Artwork.neighbourhood.ilike.assert_called_with(f"%{search_term}%")
        Artwork.description.ilike.assert_called_with(f"%{search_term}%")

    def test_get_filtered_items_by_page_when_page_length_zero(
        self, test_artwork):
        Artwork.query.filter.return_value.paginate.return_value.items = test_artwork
        self.test_service.test_get_filtered_items_by_page_when_page_length_zero(
            test_artwork)