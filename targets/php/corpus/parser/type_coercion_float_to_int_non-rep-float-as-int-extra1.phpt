<?php
set_error_handler(function ($errno, $errstr) {
    global $b;
    $b = null;
    echo $errstr, "\n";
});

$a = "1.0E+" . rand(40,42);
$b = &$a;
var_dump($b | 1);

?>