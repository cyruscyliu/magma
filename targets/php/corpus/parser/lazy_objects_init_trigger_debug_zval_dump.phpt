<?php

class C {
    public int $a;
    public function __construct() {
        var_dump(__METHOD__);
        $this->a = 1;
    }
}

$reflector = new ReflectionClass(C::class);

print "# Ghost:\n";

$obj = $reflector->newLazyGhost(function ($obj) {
    var_dump("initializer");
    $obj->__construct();
});

debug_zval_dump($obj);
$reflector->initializeLazyObject($obj);
debug_zval_dump($obj);

print "# Proxy:\n";

$obj = $reflector->newLazyProxy(function ($obj) {
    var_dump("initializer");
    return new C();
});

debug_zval_dump($obj);
$reflector->initializeLazyObject($obj);
debug_zval_dump($obj);
