<?php

class Foo {
    public function __toString() {
        static $i = 0;
        return (string) $i++;
    }
}

function test(string $foo = new Foo() . '') {
    var_dump($foo);
}

test();
test();
test();

?>