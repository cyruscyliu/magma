<?php

set_error_handler(function ($errno, $errstr) {
    global $nan;
    $nan = bin2hex(random_bytes(4));
    echo $errstr, "\n";
});

$nan = fdiv(0, 0);
var_dump($nan);
settype($nan, 'int');
var_dump($nan);

?>