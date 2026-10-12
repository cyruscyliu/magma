<?php

abstract class Foo {
    abstract public static function myMethod(string $foo);
}

const Closure = Foo::myMethod(...);

var_dump(Closure);
(Closure)("abc");

?>