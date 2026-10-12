<?php
set_exception_handler(function (\Throwable $exception) {
    echo 'Caught: ' . $exception->getMessage() . "\n";
});

ob_start(function () {
    throw new \Exception('ob_start');
});
?>