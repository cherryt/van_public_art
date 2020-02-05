var getData = async function(path){
    return await fetch(path)
    .then((response) => {
        if(!response.ok) {
            throw new Error(`not ok: error fetching ${path}`);
        }
        return response.json();
    }).catch((error) => {
        console.log(error);
    });
}

var getArtists = async function() {
    return await getData('/artists');
}

var updateTableHeader = function(headerList) {
    $('#mainTableHead').html(
        `<tr>
        </tr>`
    );
    headerList.forEach(header => {
        $('#mainTableHead tr').append(
            `<th>${header}</th>`
        )
    })
};

var setTableType = function(tableType){
    $('#mainTable').data('tableType', tableType);
}
    
var displayArtistsTable = async function() {
    var tableType = 'artists';
    if($('#mainTable').data('tableType') === tableType) return; 
    var artists = await getArtists();
    updateTableHeader(['Name', 'Info']);
    $('#mainTableBody').empty();
    if(!artists) return;
    $('#mainTableBody').html('');
    artists.forEach(artist => {
        $('#mainTableBody').append(
            `<tr> 
                <td>${artist.name}</td>
                <td>${artist.info}</td>
            </tr>`
        );
    });
    setTableType(tableType);
}

var getAllArtwork= async function() {
    return await getData('/artwork');
}

var displayArtworkTable = async function(artwork) {
    updateTableHeader(['Title', 'Address', 'Neighbourhood', 'Info']);
    $('#mainTableBody').empty();
    if(!artwork) return;
    artwork.forEach(artItem => {
        $('#mainTableBody').append(
            `<tr> 
                <td>${artItem.title}</td>
                <td>${artItem.address}</td>
                <td>${artItem.neighbourhood}</td>
                <td>${artItem.info}</td>
            </tr>`
        );
    });
}

var displayAllArtworkTable = async function() {
    var tableType = 'artwork';
    if($('#mainTable').data('tableType') === tableType) return;
    var artwork = await getAllArtwork();
    displayArtworkTable(artwork);
    setTableType(tableType);
}

var getArtworkByNeighbourhood = async function(neighbourhood) {
    return await getData(`/artwork/${neighbourhood}`);
}
    
var displayArtworkByNeighbourhood = async function(neighbourhood) {
    var tableType = `${neighbourhood}Artwork`;
    if($('#mainTable').data('tableType') === tableType) return;
    var artwork = await getArtworkByNeighbourhood(neighbourhood);
    displayArtworkTable(artwork);
    setTableType(tableType);
}