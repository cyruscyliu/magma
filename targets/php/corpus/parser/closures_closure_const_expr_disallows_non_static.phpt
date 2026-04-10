<?php

class C {
    public Closure $d = function () {
        var_dump($this);
    };
}

$foo = new C();
var_dump($foo->d);
($foo->d)();

?>