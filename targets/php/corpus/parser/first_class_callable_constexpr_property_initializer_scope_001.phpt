<?php

class C {
    public Closure $d = C::myMethod(...);

    private static function myMethod(string $foo) {
        echo "Called ", __METHOD__, PHP_EOL;
        var_dump($foo);
    }
}

$c = new C();
var_dump($c->d);
var_dump(($c->d)("abc"));

?>