<?php
set_error_handler(function($_, $m) {
    echo "$m\n";
    unset($GLOBALS['x']);
});

$x=" ";
echo "POST DEC\n";
var_dump($x--);

$x=" ";
echo "PRE DEC\n";
var_dump(--$x);

$x=" ";
echo "POST INC\n";
var_dump($x++);

$x=" ";
echo "PRE INC\n";
var_dump(++$x);
?>