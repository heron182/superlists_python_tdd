var initialize = function() {
    $('input[name="text"]').on('keypress', function() {
        $('.alert-danger').hide()
    })
}
