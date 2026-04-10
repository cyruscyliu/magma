<?php

function usage1(Closure $c) {
    $c(a: 1);
}

usage1(eval('return function($a) { var_dump($a); };'));
usage1(eval('return function($b) { var_dump($b); };'));

?>