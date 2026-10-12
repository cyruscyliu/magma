<?php

set_error_handler(function () {
    global $x;
    $x = 1;
});

$x = '';
$x--;
var_dump($x);

?>
DONE