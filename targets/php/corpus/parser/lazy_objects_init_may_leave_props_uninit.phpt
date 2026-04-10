<?php

class C {
    public $a;
    public int $b;

    public function __construct() {
        var_dump(__METHOD__);
    }
}

$reflector = new ReflectionClass(C::class);

$obj = $reflector->newLazyGhost(function ($obj) {
    var_dump("initializer");
    $obj->__construct();
});

var_dump($obj);
var_dump($obj->a);
try {
    var_dump($obj->b);
} catch (Error $e) {
    printf("%s\n", $e);
}
var_dump($obj);