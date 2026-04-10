<?php

class C {
    public int $a;
    public $b;

    public function __construct() {
        $this->a = 1;
        $this->b = 2;
    }
}

function test(string $name, object $obj) {
    printf("# %s\n", $name);

    $reflector = new ReflectionClass(C::class);
    $reflector->getProperty('a')->setRawValueWithoutLazyInitialization($obj, 3);

    $a = [];
    // Converts $obj to array internally
    array_splice($a, 0, 0, $obj);
    var_dump($a, $obj);

    $reflector->initializeLazyObject($obj);

    $a = [];
    array_splice($a, 0, 0, $obj);
    var_dump($a, $obj);
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

?>