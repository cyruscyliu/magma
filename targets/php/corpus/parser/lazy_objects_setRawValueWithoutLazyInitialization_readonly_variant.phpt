<?php

class C {
    public function __construct() {
        try {
            $this->a = 1;
        } catch (Error $e) {
            printf("%s: %s\n", $e::class, $e->getMessage());
        }
    }
    public readonly int $a;
    public $b;
}

function test(string $name, object $obj) {
    printf("# %s\n", $name);

    $reflector = new ReflectionClass(C::class);
    $reflector->getProperty('a')->setRawValueWithoutLazyInitialization($obj, 2);

    var_dump($obj->a);
    var_dump(!$reflector->isUninitializedLazyObject($obj));
    var_dump($obj);

    $reflector->initializeLazyObject($obj);
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

?>