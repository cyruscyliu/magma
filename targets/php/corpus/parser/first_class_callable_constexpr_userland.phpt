<?php

function my_function(string $foo) {
    echo "Called ", __FUNCTION__, PHP_EOL;
    var_dump($foo);
}

const Closure = my_function(...);

var_dump(Closure);
(Closure)("abc");

?>