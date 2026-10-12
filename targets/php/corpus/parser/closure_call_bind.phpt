<?php

class Foo {
    function __call($name, $args) {
        echo "__call($name)\n";
    }
}

$foo = new Foo;
$name = "foo";
Closure::fromCallable([$foo, $name . "bar"])->bindTo(new Foo)();
$foo->{$name . "bar"}(...)->bindTo(new Foo)();

?>