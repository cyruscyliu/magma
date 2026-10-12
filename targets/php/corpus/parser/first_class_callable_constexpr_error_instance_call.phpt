<?php

class Foo {
    public function myMethod(string $foo) {
        echo "Called ", __METHOD__, PHP_EOL;
        var_dump($foo);
    }
}

const Closure = (new Foo())->myMethod(...);

var_dump(Closure);
(Closure)("abc");

?>