<?php

class Foo {
    public static function __callStatic(string $name, array $foo) {
        echo "Called ", __METHOD__, "({$name})", PHP_EOL;
        var_dump($foo);
    }
}

const Closure = Foo::myMethod(...);

var_dump(Closure);
(Closure)("abc");

?>