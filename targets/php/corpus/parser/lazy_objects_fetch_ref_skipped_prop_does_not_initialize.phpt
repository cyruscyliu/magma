<?php

class C {
    public $a;
    public int $b = 1;
    public int $c;
    public function __construct() {
        var_dump(__METHOD__);
    }
}

function test(string $name, object $obj) {
    printf("# %s:\n", $name);

    var_dump($obj);
    $ref = &$obj->a;
    $ref = &$obj->b;
    try {
        $ref = &$obj->c;
    } catch (Error $e) {
        printf("%s\n", $e->getMessage());
    }
    var_dump($ref);
    var_dump($obj);
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
