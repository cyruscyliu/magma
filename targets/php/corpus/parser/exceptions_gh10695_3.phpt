<?php
register_shutdown_function(function () {
    echo "shutdown\n";
    set_exception_handler(function (\Throwable $exception) {
        echo 'Caught: ' . $exception->getMessage() . "\n";
    });
});

throw new \Exception('main');
?>