<?php

class C {
    public int $a;
    public int $b;
}

function test(string $name, object $obj) {
    printf("# %s\n", $name);

    $reflector = new ReflectionClass(C::class);
    $reflector->getProperty('a')->skipLazyInitialization($obj);
    try {
        $reflector->getProperty('a')->setRawValueWithoutLazyInitialization($obj, new stdClass);
    } catch (Error $e) {
        printf("%s: %s\n", $e::class, $e->getMessage());
    }

    // Prop is still non-lazy: This does not trigger initialization
    $obj->a = 1;
    var_dump($reflector->isUninitializedLazyObject($obj));
    var_dump($obj);
}

$reflector = new ReflectionClass(C::class);
$obj = $reflector->newLazyGhost(function ($obj) {
    throw new Exception('Unreachable');
});

test('Ghost', $obj);

$obj = $reflector->newLazyProxy(function () {
    throw new Exception('Unreachable');
});

test('Proxy', $obj);

?>