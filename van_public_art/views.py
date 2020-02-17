from flask import render_template, request, jsonify

from van_public_art import app
from van_public_art.services import (
    ArtistService, ArtworkService, NeighbourhoodArtworkService
    )

    
@app.route('/')
def template():
    neighbourhoods = NeighbourhoodArtworkService.get_neighbourhoods()
    return render_template('main.html', neighbourhoods=neighbourhoods)

@app.route('/datatable/artists', methods=['GET', 'POST'])
def datatable_artists():
    return _form_datatable_response(request.args, ArtistService())

@app.route('/datatable/artwork', methods=['GET', 'POST'])
def datatable_artwork():
    return _form_datatable_response(request.args, ArtworkService())

@app.route('/datatable/<neighbourhood>', methods=['GET', 'POST'])
def datatable_neighbourhood_artwork(neighbourhood):
    return _form_datatable_response(
        request.args, NeighbourhoodArtworkService(neighbourhood))

def _form_datatable_response(requestArgs, publicArtService):
    start_item = requestArgs.get('start', 0, type=int)
    page_length = requestArgs.get('length', 30, type=int)
    draw = requestArgs.get('draw', 0, type=int)
    search_value = requestArgs.get('search[value]', None, type=str)
    if(search_value):
        count = publicArtService.get_filtered_items_count(search_value)
        data = publicArtService.get_filtered_items_by_page(
            search_value, start_item, page_length)
    else:
        count = publicArtService.get_all_items_count()
        data = publicArtService.get_items_by_page(start_item, page_length)
    result = {
        "draw": draw,
        "recordsTotal": count,
        "recordsFiltered": count,
        "data": data
    }
    return jsonify(result)