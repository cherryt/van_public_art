from flask import render_template, jsonify
from van_public_art import app
from van_public_art.services import ArtistService, ArtworkService

@app.route('/')
def template():
    neighbourhoods = ['Downtown', 'West End', 'Mount Pleasant']
    return render_template('main.html', neighbourhoods=neighbourhoods)

@app.route('/artists', methods=['GET'])
def artists():
    return jsonify(ArtistService.get_all_artists())

@app.route('/artwork', methods=['GET'])
def artwork():
    return jsonify(ArtworkService.get_all_artwork())

@app.route('/artwork/<neighbourhood>', methods=['GET'])
def artworksByNeighbourhood(neighbourhood):
    return jsonify(ArtworkService.get_artwork_by_neighbourhood(neighbourhood))
