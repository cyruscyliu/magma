<?php

set_error_handler(function ($errno, $errstr) {
    global $nan;
    $nan = 45;
    echo $errstr, "\n";
});

$nan = fdiv(0, 0);
var_dump($nan);
settype($nan, 'null');
var_dump($nan);

?>