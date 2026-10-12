<?php

class C {
    public $a = 1;
    public int $b = 2;

    public function __construct() {
        var_dump(__METHOD__);
        $this->a = 3;
        $this->b = 4;
    }
}

$reflector = new ReflectionClass(C::class);

$obj = $reflector->newLazyGhost(function ($obj) {
    var_dump("initializer");
    var_dump($obj);
    $obj->__construct();
});

var_dump($obj);
var_dump($obj->a);
var_dump($obj);