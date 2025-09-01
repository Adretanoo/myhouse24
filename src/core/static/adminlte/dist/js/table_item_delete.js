$(document).on('click', '.delete-button', function (e) {
    e.preventDefault();
    let url = $(this).data('url');
    if (confirm("Вы уверены, что хотите удалить?")) {
        let form = $('#deleteForm');
        form.attr('action', url);
        form.submit();
    }
});
