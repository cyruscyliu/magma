<?php

class C {
    public int $a = 1;
    public function __construct() {
        var_dump(__METHOD__);
        $this->a = 2;
    }
}

function test(string $name, object $obj) {
    printf("# %s:\n", $name);

    var_dump($obj);

    try {
        var_dump($obj->a++);
    } catch (Error $e) {
        printf("%s: %s\n", $e::class, $e->getMessage());
    }

    var_dump($obj);
}

$reflector = new ReflectionClass(C::class);

$obj = $reflector->newLazyGhost(function ($obj) {
    throw new Error("initializer");
});

test('Ghost', $obj);

$obj = $reflector->newLazyProxy(function ($obj) {
    throw new Error("initializer");
});

test('Proxy', $obj);
