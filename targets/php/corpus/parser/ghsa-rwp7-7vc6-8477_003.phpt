<?php

class Foo {
    public int $prop;
}

function newFoo() {
    return new Foo();
}

try {
    newFoo()->prop ??= 'foo';
} catch (Error $e) {
    echo $e->getMessage();
}

?>