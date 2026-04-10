<?php

class Canary {
    public function __destruct() {
        var_dump(__METHOD__);
    }
}

#[\AllowDynamicProperties]
class C {
    public $b;
    public function __construct() {
        $this->a = new Canary();
    }
}

$reflector = new ReflectionClass(C::class);

print "# Ghost:\n";

$obj = new C();
$reflector->resetAsLazyGhost($obj, function ($obj) {
    var_dump("initializer");
    $obj->__construct();
});

var_dump($obj);
var_dump($obj->a);
var_dump($obj);

print "# Proxy:\n";

$obj = new C();
$reflector->resetAsLazyProxy($obj, function ($obj) {
    var_dump("initializer");
    return new C();
});

var_dump($obj);
var_dump($obj->a);
var_dump($obj->a);
var_dump($obj);
