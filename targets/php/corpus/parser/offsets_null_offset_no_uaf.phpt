<?php
set_error_handler(function($errno, $errstr) {
    global $ary;
    $ary = null;
    echo $errstr;
});

$ary[null] = 1;

echo "\nSuccess\n";
?>