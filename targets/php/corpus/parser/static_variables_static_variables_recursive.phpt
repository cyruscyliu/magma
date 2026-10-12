<?php

function foo($i) {
    static $a = $i <= 10 ? foo($i + 1) : "Done $i";
    var_dump($a);
    return $i;
}

foo(0);
foo(5);

?>