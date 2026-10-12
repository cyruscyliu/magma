<?php

namespace Foo;

function strrev(string $value) {
    return 'not the global one';
}

const Closure = strrev(...);

var_dump(Closure);
var_dump((Closure)("abc"));

?>