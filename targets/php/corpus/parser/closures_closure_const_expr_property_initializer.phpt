<?php

class C {
    public Closure $d = static function () {
        echo "called", PHP_EOL;
    };
}

$c = new C();
var_dump($c->d);
($c->d)();


?>