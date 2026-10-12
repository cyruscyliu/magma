<?php

$foo = [1, 2, 3];
static $x = new stdClass($foo);
var_dump($foo);

?>