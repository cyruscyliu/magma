<?php

#[AllowDynamicProperties]
class B {
    private readonly string $b;

    public function __construct() {
        $this->b = 'b';
    }
}

#[AllowDynamicProperties]
class C extends B {
    public string $a;

    public function __construct() {
        parent::__construct();
        $this->a = 'a';
    }
}

function test(string $name, object $obj) {
    $reflector = new ReflectionClass(C::class);

    printf("# %s:\n", $name);

    var_dump(!$reflector->isUninitializedLazyObject($obj));

    $reflector->getProperty('a')->skipLazyInitialization($obj);
    var_dump(!$reflector->isUninitializedLazyObject($obj));

    // Should not count a second prop initialization
    $reflector->getProperty('a')->skipLazyInitialization($obj);
    var_dump(!$reflector->isUninitializedLazyObject($obj));

    try {
        // Should not count a prop initialization
        $reflector->getProperty('xxx')->skipLazyInitialization($obj);
    } catch (ReflectionException $e) {
        printf("%s: %s\n", $e::class, $e->getMessage());
    }

    try {
        // Should not count a prop initialization
        $reflector->getProperty('b')->skipLazyInitialization($obj);
    } catch (ReflectionException $e) {
        printf("%s: %s\n", $e::class, $e->getMessage());
    }

    (new ReflectionProperty(B::class, 'b'))->skipLazyInitialization($obj);
    var_dump(!$reflector->isUninitializedLazyObject($obj));

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
