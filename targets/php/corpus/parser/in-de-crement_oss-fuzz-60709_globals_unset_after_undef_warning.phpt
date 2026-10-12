<?php
set_error_handler(function($_, $m) {
    echo "$m\n";
    unset($GLOBALS['x']);
});

echo "POST DEC\n";
var_dump($x--);
unset($x);
echo "POST INC\n";
var_dump($x++);
unset($x);
echo "PRE DEC\n";
var_dump(--$x);
unset($x);
echo "PRE INC\n";
var_dump(++$x);
?>