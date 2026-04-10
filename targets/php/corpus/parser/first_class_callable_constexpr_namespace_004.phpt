<?php

namespace Foo;

function foo(\Closure $c = strrev(...)) {
    $d = strrev(...);
    var_dump($c);
    var_dump($c("abc"));
    var_dump($d);
    var_dump($d("abc"));
}


foo();

if (random_int(1, 2) > 0) {
    function strrev(string $value) {
        return 'not the global one';
    }
}

foo();

?>