<?php

set_error_handler(function ($errno, $errstr) {
    global $nan;
    unset($nan);
    echo $errstr, "\n";
});

$nan = fdiv(0, 0);
var_dump($nan);
settype($nan, 'object');
var_dump($nan);

?>