<?php

class C {
    public $a = 1;

    public function __construct() {
    }
}

function test(string $name, object $obj) {
    printf("# %s:\n", $name);

    $reflector = new ReflectionClass($obj::class);
    $clone = clone($obj, [ 'a' => 2 ]);

    var_dump($reflector->isUninitializedLazyObject($obj));
    var_dump($obj);
    var_dump($reflector->isUninitializedLazyObject($clone));
    var_dump($clone);
}

$reflector = new ReflectionClass(C::class);

$obj = $reflector->newLazyGhost(function ($obj) {
    var_dump("initializer");
    $obj->__construct();
});

test('Ghost', $obj);

$obj = $reflector->newLazyProxy(function ($obj) {
    var_dump("initializer");
    return new C();
});

test('Proxy', $obj);

?>