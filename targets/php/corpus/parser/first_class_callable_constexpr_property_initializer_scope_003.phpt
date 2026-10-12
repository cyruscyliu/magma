<?php

class P {
    protected static function myMethod(string $foo) {
        echo "Called ", __METHOD__, PHP_EOL;
        var_dump($foo);
    }
}


class C extends P {
    public Closure $d = self::myMethod(...);
}

$c = new C();
var_dump($c->d);
var_dump(($c->d)("abc"));

?>