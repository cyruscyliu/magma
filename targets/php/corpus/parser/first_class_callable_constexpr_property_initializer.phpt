<?php

class C {
    public Closure $d = strrev(...);
}

$c = new C();
var_dump($c->d);
var_dump(($c->d)("abc"));


?>