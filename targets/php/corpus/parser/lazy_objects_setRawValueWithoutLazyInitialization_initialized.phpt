<?php

class C {
    public function __construct() {
    }
    public $a;
    public $b;
}

function test(string $name, object $obj) {
    printf("# %s\n", $name);

    $reflector = new ReflectionClass(C::class);
    $reflector->initializeLazyObject($obj);
    $reflector->getProperty('a')->setRawValueWithoutLazyInitialization($obj, 'test');

    var_dump($obj->a);
    var_dump($obj);
}

$reflector = new ReflectionClass(C::class);
$obj = $reflector->newLazyGhost(function ($obj) {
    $obj->__construct();
});

test('Ghost', $obj);

$obj = $reflector->newLazyProxy(function () {
    return new C();
});

test('Proxy', $obj);

$real = new C('foo');
$obj = $reflector->newLazyProxy(function () use ($real) {
    return $real;
});
$reflector->initializeLazyObject($obj);
$reflector->resetAsLazyProxy($real, function () {
    return new C('bar');
});
$reflector->initializeLazyObject($real);

test('Nested Proxy', $obj);

?>