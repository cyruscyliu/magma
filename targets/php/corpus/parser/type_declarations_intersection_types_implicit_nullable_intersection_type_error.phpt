<?php

function foo(X&Y $foo = null) {
    var_dump($foo);
}

try {
    foo(5);
} catch (\TypeError $e) {
    echo $e->getMessage(), \PHP_EOL;
}

?>