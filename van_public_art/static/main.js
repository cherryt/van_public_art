'use-strict';

var addTableHeader = function (tableId, headerList) {
    $(`#${tableId}`).append(
        $('<thead>').append(
            '<tr/>')
    );
    headerList.forEach(header => {
        $(`#${tableId} thead tr`).append(
            `<th>${header["data"].replace(/^\w/, c => c.toUpperCase())}</th>`
        )
    })
};

var getDataTableSettings = function (apiUrl, columns) {
    return {
        "processing": true,
        "serverSide": true,
        "ajax": apiUrl,
        "columns": columns,
        "paging": true,
        "pagingType": "simple_numbers",
        "retrieve": true
    };
}

var tableType;
var _displayTable = function (apiUrl, columns) {
    if ($(`#${tableType}Table`).data('tableType') === tableType) return;
    var table = $(`#${tableType}Table`).DataTable(getDataTableSettings(apiUrl, columns));
    table.page(0).draw('page');
}

var columns = {
    "artists": [
        { "data": "name" },
        { "data": "info" }
    ]
    ,
    "artwork": [
        { "data": "title" },
        { "data": "address" },
        { "data": "neighbourhood" },
        { "data": "info" }
    ]
};

var _displayNeighhourhoodTable = function (neighbourhood) {
    if (!$(`#${neighbourhood}Table`).length) {
        $('#neighbourhoodTables').append(
            $('<div/>')
                .attr("id", `${neighbourhood}TableAll`)
                .addClass("table-responsive")
                .append(
                    $('<table/>')
                        .attr("id", `${neighbourhood}Table`)
                        .addClass("table table-striped table-sm")
                )
        );
        addTableHeader(`${neighbourhood}Table`, columns["artwork"]);
    }
    _displayTable(`/datatable/${neighbourhood}`, columns["artwork"])
}
var displayArtworkByNeighbourhood = function (neighbourhood) {
    $(`#${tableType}TableAll`).hide();
    tableType = neighbourhood.replace(/ /g, '');
    _displayNeighhourhoodTable(tableType);
    $(`#${tableType}TableAll`).show();
}

$(function () {
    addTableHeader('artistsTable', columns["artists"]);
    addTableHeader('artworkTable', columns["artwork"]);

    $('#artistsTableAll').hide();
    $('#artworkTableAll').hide();

    $('#artistsLink').on('click', function () {
        $(`#${tableType}TableAll`).hide();
        tableType = "artists";
        _displayTable(`/datatable/${tableType}`, columns["artists"]);
        $(`#${tableType}TableAll`).show();
    })

    $('#artworkLink').on('click', function () {
        $(`#${tableType}TableAll`).hide();
        tableType = "artwork";
        _displayTable(`/datatable/${tableType}`, columns["artwork"]);
        $(`#${tableType}TableAll`).show();
    })

    $('.nav-link').on('click', function() {
        $('.nav-link').removeClass('active');
        $(this).addClass('active');
    })
});