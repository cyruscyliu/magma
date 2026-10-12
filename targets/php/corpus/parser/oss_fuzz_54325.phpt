<?php
set_error_handler(function ($errno, $errstr) {
    var_dump($errstr);
    global $x;
    $x = new stdClass;
});

// Needs to be non-interned string
$x = strrev('foo');
$$x++;
var_dump($x);
?>