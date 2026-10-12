<?php

class C {
    public function __construct() {
        $this->a = 2;
    }
    public $a = 1;
    public $b;
}

function test(string $name, object $obj) {
    printf("# %s\n", $name);

    $reflector = new ReflectionClass(C::class);
    $reflector->initializeLazyObject($obj);
    $reflector->getProperty('a')->skipLazyInitialization($obj);

    var_dump($obj->a);
    var_dump(!$reflector->isUninitializedLazyObject($obj));
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
    var_dump("initializer");
    return new C('bar');
});
$reflector->initializeLazyObject($real);

test('Nested Proxy', $obj);

?>