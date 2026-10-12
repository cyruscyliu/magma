<?php
set_exception_handler(function (\Throwable $exception) {
    echo 'Caught: ' . $exception->getMessage() . "\n";
});
set_error_handler(function ($errno, $errstr) {
    throw new \Exception($errstr);
});
register_shutdown_function(function () {
    trigger_error('main', E_USER_WARNING);
});
?>