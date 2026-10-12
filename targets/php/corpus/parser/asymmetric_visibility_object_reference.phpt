<?php

class Foo {
    public private(set) Bar $bar;

    public function __construct() {
        $this->bar = new Bar();
    }
}

class Bar {}

function test() {
    $foo = new Foo();
    $bar = &$foo->bar;
    var_dump($foo);
}

test();
// Test zend_fetch_property_address with warmed cache
test();

?>