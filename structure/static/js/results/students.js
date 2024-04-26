let resultsTable = $("#results-table-dt").DataTable({
    dom: '<"row mb-2"<"col-12"l>>rBftip',
    ajax: {url: "/studentsapi"},
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
            data:"index_number"
            },
        {
            data: 'name',
        },
        {
        data:"completed_year",
        },
       
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
        },
        {
            extend: '',
            text: 'Refresh Table',
            action: function (e, table, button, config) {
                table.ajax.reload(null, false);
            }
        },
        {
            extend: 'selected',
            text: 'Edit result',
            action: function (e, table, button, config) {
                let selectedRows = table.rows({selected: true});
                if (selectedRows.count() !== 1) {
                    alert("Sorry, you can only edit one result. Kindly select only one result");
                    return;
                }
                let data = table.row(selectedRows.indexes()[0]).data();
                $("#edit-result-form").attr("action", `/result/${data.id}`);
                $("#edit-result-id").val(data.id);
                $("#edit-result-name").val(data.name);
                $("#edit-result-result").val(data.result);
                $('#editResultModal').modal('show');
            }
        },
        {
            extend: 'selected',
            text: 'View Student',
            action: function (e, table, button, config) {
                let selectedRows = table.rows({selected: true});
                if (selectedRows.count() !== 1) {
                    alert("Sorry, you can only edit one result. Kindly select only one result");
                    return;
                }
                let data = table.row(selectedRows.indexes()[0]).data();
                let id = data.id;
                window.location.href = `/student/${id}`;
            }
        },
        {
            extend: 'selected',
            text: 'Delete',
            attr: {
                class: 'ml-2 btn btn-sm btn-danger',
            },
            action: function (e, table, button, config) {
                let selectedRows = table.rows({selected: true}).indexes();
                let resultIds = [];
                Array.from(selectedRows).forEach((rowIndex) => {
                    let data = table.row(rowIndex).data();
                    resultIds.push(data.id);
                });

                if (confirm("Are you sure you want to delete?")) {
                    fetch(`/api/delete_results?results=${resultIds.join(',')}`)
                        .then(res => res.json())
                        .then(payload => {
                            Array.from(selectedRows).forEach((row) => {
                                table.row(row).remove().draw();
                                table.ajax.reload(null, false);
                            });
                        });
                }
            }
        },
    ],
});




