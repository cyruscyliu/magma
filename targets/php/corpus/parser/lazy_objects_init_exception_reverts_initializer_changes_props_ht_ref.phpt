<?php

class C {
    public $a = 1;
    public int $b = 2;
    public int $c;
}

function test(string $name, object $obj) {
    $reflector = new ReflectionClass(C::class);

    printf("# %s:\n", $name);

    (new ReflectionProperty(C::class, 'c'))->setRawValueWithoutLazyInitialization($obj, 0);

    // Builds properties hashtable
    var_dump(get_mangled_object_vars($obj));

    try {
        $reflector->initializeLazyObject($obj);
    } catch (Exception $e) {
        printf("%s\n", $e->getMessage());
    }

    var_dump($obj);
    printf("Is lazy: %d\n", $reflector->isUninitializedLazyObject($obj));

    var_dump($table);
}

$reflector = new ReflectionClass(C::class);

$obj = $reflector->newLazyGhost(function ($obj) {
    global $table;
    var_dump("initializer");
    $obj->a = 3;
    $obj->b = 4;
    $obj->c = 5;
    $table = (array) $obj;
    throw new Exception('initializer exception');
});

test('Ghost', $obj);

$obj = $reflector->newLazyProxy(function ($obj) {
    global $table;
    var_dump("initializer");
    $obj->a = 3;
    $obj->b = 4;
    $obj->c = 5;
    $table = (array) $obj;
    throw new Exception('initializer exception');
});

// Initializer effects on the proxy are not reverted
test('Proxy', $obj);
