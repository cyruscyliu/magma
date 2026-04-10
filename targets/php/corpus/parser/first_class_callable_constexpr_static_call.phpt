<?php

class Foo {
    public static function myMethod(string $foo) {
        echo "Called ", __METHOD__, PHP_EOL;
        var_dump($foo);
    }
}

const Closure = Foo::myMethod(...);

var_dump(Closure);
(Closure)("abc");

?>