let resultsTable = $("#result-table-dt").DataTable({
    dom: '<"row mb-2"<"col-12"l>>rBftip',
    ajax: {url: "/checkresultsapi"},
    cache:false,
    processing: true,
    language: {
        processing: 'Loading results...',
    },
    columnDefs: [{
        orderable: false,
        className: 'select-checkbox',
        targets: 0
    }],
    select: {
        style: 'multi+shift',
        selector: 'td:first-child',
        info: true,
    },
    columns: [
        {
            data: null,
            render: function render(data, type, row, meta) {
                return '';
            }
        },
        {
            data: 'name',
        },
        {
            data: 'subject',
        },
        {
            data: 'result',
        }
    ],
    buttons: [
        {
            extend: 'print',
            exportOptions: {
                columns: [1, 2, 3, 4, 5, 6, 7, 8],
            }
        },
        {
            extend: 'csv',
            exportOptions: {
                columns: [1, 2, 3, 4, 5, 6, 7, 8],
            }
        },
        {
            extend: 'pdf',
            exportOptions: {
                columns: [1, 2, 3, 4, 5, 6, 7, 8],
            }
        },
        {
            extend: 'selectNone',
            name: 'selectNone',
        }
        
    ],
});




