<?php
set_exception_handler(function (\Throwable $exception) {
    echo 'Caught: ' . $exception->getMessage() . "\n";
    throw new \Exception('exception handler');
});

throw new \Exception('main');
?>