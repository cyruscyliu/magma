<?php

function func() {
    static $i;
}

$x = func(...);

var_dump($x);

?>