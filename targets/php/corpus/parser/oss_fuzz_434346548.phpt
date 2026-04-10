<?php

class Foo {
    function __toString() {}
}

function test($y = new Foo() < "") {
    var_dump();
}

try {
    test();
} catch (Error $e) {
    echo $e->getMessage(), "\n";
}

?>