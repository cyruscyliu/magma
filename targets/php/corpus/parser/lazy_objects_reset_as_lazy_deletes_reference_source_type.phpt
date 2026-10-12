<?php

class C {
    public int $a;

    public function __construct() {
        $this->a = 1;
    }
}

$reflector = new ReflectionClass(C::class);

print "# Ghost:\n";

$obj = new C();
$ref = &$obj->a;
try {
    $ref = 'string';
} catch (\Error $e) {
    printf("%s: %s\n", $e::class, $e->getMessage());
}
$reflector->resetAsLazyGhost($obj, function ($obj) {
    var_dump("initializer");
    $obj->__construct();
});

$ref = 'string';
var_dump($obj);
var_dump($obj->a);
var_dump($obj);

print "# Proxy:\n";

$obj = new C();
$ref = &$obj->a;
try {
    $ref = 'string';
} catch (\Error $e) {
    printf("%s: %s\n", $e::class, $e->getMessage());
}
$reflector->resetAsLazyProxy($obj, function ($obj) {
    var_dump("initializer");
    return new C();
});

$ret = 'string';
var_dump($obj);
var_dump($obj->a);
var_dump($obj->a);
var_dump($obj);
