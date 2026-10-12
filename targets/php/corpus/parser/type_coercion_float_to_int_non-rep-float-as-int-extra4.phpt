<?php

set_error_handler(function ($errno, $errstr) {
    global $ary;
    $ary = null;
    echo $errstr, "\n";
});

$ary = [rand()];
var_dump(\array_key_exists(1.0E+42, $ary));

?>