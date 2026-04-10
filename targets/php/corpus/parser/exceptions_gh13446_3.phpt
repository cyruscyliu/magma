<?php
function exception_handler_1($ex) {
    echo "Handler 1\n";
    set_exception_handler('exception_handler_2');
}

function exception_handler_2($ex) {
    echo "Handler 2\n";
}

set_exception_handler('exception_handler_1');

register_shutdown_function(function () {
    echo set_exception_handler(null), "\n";
    restore_exception_handler();
});

throw new Exception();
?>