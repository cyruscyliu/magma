<?php

set_error_handler(function () {
    global $x;
    $x = 1;
});

$x = '';
$x++;
var_dump($x);

set_error_handler(function ($errno, $errstr) {
    var_dump($errstr);
    global $x;
    $x = new stdClass;
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