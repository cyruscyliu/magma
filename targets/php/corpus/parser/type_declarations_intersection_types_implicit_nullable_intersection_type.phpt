<?php

function foo(X&Y $foo = null) {
    var_dump($foo);
}

foo(null);

?>