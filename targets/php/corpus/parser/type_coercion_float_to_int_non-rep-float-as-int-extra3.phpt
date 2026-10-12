<?php

set_error_handler(function ($errno, $errstr) {
    global $ary;
    $ary = null;
    echo $errstr, "\n";
});

$ary = [rand()];
var_dump(isset($ary[1.0E+42]));

?>