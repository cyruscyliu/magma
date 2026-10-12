<?php

class Foo {
    public const Closure = self::myMethod(...);

    public static function myMethod(string $foo) {
        echo "Called ", __METHOD__, PHP_EOL;
        var_dump($foo);
    }
}

var_dump(Foo::Closure);
(Foo::Closure)("abc");

?>