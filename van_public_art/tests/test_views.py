from contextlib import contextmanager
import flask
from flask import template_rendered
import os
import pytest

from van_public_art import app


class TestViews:

    def test_template(self, client):
        with self.get_template() as main_template:
            res = client.get('/')
            assert res.status_code == 200
            assert main_template[0][0].name == "main.html"
            assert len(main_template[0][1]["neighbourhoods"]) != 0
    
    @contextmanager
    def get_template(self):
        main_template = []
        def set_template(sender, template, context, **extra):
            main_template.append((template, context))
        template_rendered.connect(set_template, app)
        yield main_template
        template_rendered.disconnect(set_template, app)
    
    @pytest.fixture(scope='function')
    def client(self):
        app.config['TESTING'] = True
        with app.test_client() as client:
            yield client

    def test_datatable_artists_without_search(self, client):
        path = '/datatable/artists'
        self._test_datatable(client, path, self.request_params)

    @pytest.fixture(scope='function', autouse=True)
    def initialize_request_param(self):
        self.request_params = {
            'start': 1,
            'length': 20,
            'draw': 0
            }

    def test_datatable_artists_with_search(self, client):
        path = '/datatable/artists'
        self.request_params['search[value]'] = "test word"
        self._test_datatable(client, path, self.request_params)
    
    def test_datatable_artwork(self, client):
        path = '/datatable/artwork'
        self._test_datatable(client, path, self.request_params)

    def test_datatable_neighbourhood_artwork(self, client):
        path = '/datatable/kitsilano'
        self._test_datatable(client, path, self.request_params)

    def _test_datatable(self, client, path, request_params):
        res = client.post(path, json=request_params)
        data = res.get_json()
        assert data['recordsTotal'] != None
        assert data['recordsFiltered'] != None
        assert data['data'] != None