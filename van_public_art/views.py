from flask import render_template, request, jsonify

from van_public_art import app
from van_public_art.services import (
    ArtistService, ArtworkService, NeighbourhoodArtworkService
    )
@app.route('/')
def template():
    neighbourhoods = NeighbourhoodArtworkService.get_neighbourhoods()
    return render_template('main.html', neighbourhoods=neighbourhoods)

@app.route('/datatable/artwork', methods=['GET', 'POST'])
def datatable_artwork():
    requestArgs = request.args
    return _form_datatable_response(requestArgs, ArtworkService())

@app.route('/datatable/artists', methods=['GET', 'POST'])
def datatable_artists():
    requestArgs = request.args
    return _form_datatable_response(requestArgs, ArtistService())

@app.route('/datatable/<neighbourhood>', methods=['GET', 'POST'])
def datatable_neighbourhood_artwork(neighbourhood):
    requestArgs = request.args
    return _form_datatable_response(
        requestArgs, NeighbourhoodArtworkService(neighbourhood))

def _form_datatable_response(requestArgs, publicArtService):
    startItem = requestArgs.get('start', 0, type=int)
    pageLength = requestArgs.get('length', 30, type=int)
    draw = requestArgs.get('draw', 0, type=int)
    count = publicArtService.get_all_items_count()
    data = publicArtService.get_items_by_page(startItem, pageLength)
    result = {
        "draw": draw,
        "recordsTotal": count,
        "recordsFiltered": count,
        "data": data
    }
    return jsonify(result)