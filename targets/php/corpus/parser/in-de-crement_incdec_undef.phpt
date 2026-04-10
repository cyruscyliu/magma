<?php
set_error_handler(function($_, $m) {
    echo "$m\n";
});
var_dump($x--);
unset($x);
var_dump($x++);
unset($x);
var_dump(--$x);
unset($x);
var_dump(++$x);
?>