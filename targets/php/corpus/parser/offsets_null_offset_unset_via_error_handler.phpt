<?php
set_error_handler(function ($errno, $errstr) {
    var_dump($errstr);
    global $a;
    unset($a);
});

$a = new stdClass;
$b = [0, null => $a];

echo "\nSuccess\n";
?>