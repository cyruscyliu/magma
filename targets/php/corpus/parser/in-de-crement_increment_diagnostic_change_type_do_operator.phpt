<?php

set_error_handler(function ($errno, $errstr) {
    var_dump($errstr);
    global $x;
    $x = gmp_init(10);
});

$x = 'foo!';
$x++;
var_dump($x);

/* Interned string */
$x = '!';
$x++;
var_dump($x);

?>
DONE