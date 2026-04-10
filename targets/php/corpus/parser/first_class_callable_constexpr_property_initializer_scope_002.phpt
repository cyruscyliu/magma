<?php

class E {
    private static function myMethod(string $foo) {
        echo "Called ", __METHOD__, PHP_EOL;
        var_dump($foo);
    }
}

class C {
  public Closure $d = E::myMethod(...);
}

$c = new C();
var_dump($c->d);
var_dump(($c->d)("abc"));

?>