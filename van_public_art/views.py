from flask import render_template, request, jsonify

from van_public_art import app
from van_public_art.services import (
    ArtistService,
    ArtworkService,
    NeighbourhoodArtworkService,
)


@app.route("/")
def template():
    neighbourhoods = NeighbourhoodArtworkService.get_neighbourhoods()
    return render_template("main.html", neighbourhoods=neighbourhoods)


@app.route("/datatable/artwork", methods=["GET", "POST"])
def datatable_artwork():
    request_args = request.args
    return _form_datatable_response(request_args, ArtworkService())


@app.route("/datatable/artists", methods=["GET", "POST"])
def datatable_artists():
    request_args = request.args
    return _form_datatable_response(request_args, ArtistService())


@app.route("/datatable/<neighbourhood>", methods=["GET", "POST"])
def datatable_neighbourhood_artwork(neighbourhood):
    request_args = request.args
    return _form_datatable_response(
        request_args, NeighbourhoodArtworkService(neighbourhood)
    )


def _form_datatable_response(request_args, service):
    start_item = request_args.get("start", 0, type=int)
    page_length = request_args.get("length", 30, type=int)
    draw = request_args.get("draw", 0, type=int)
    search_value = request_args.get("search[value]", None, type=str)
    if search_value:
        count = service.get_filtered_items_count(search_value)
        data = service.get_filtered_items_by_page(search_value, start_item, page_length)
    else:
        count = service.get_all_items_count()
        data = service.get_items_by_page(start_item, page_length)
    result = {
        "draw": draw,
        "recordsTotal": count,
        "recordsFiltered": count,
        "data": data,
    }
    return jsonify(result)
