<?php

class B {
    public readonly int $a;
    public readonly int $b;
    public int $c;

    public function __construct($value, bool $setB = false) {
        try {
            $this->a = $value;
        } catch (\Error $e) {
            printf("%s: %s\n", $e::class, $e->getMessage());
        }
        if ($setB) {
            $this->b = $value;
        }
        try {
            $this->c = $value;
        } catch (\Error $e) {
            printf("%s: %s\n", $e::class, $e->getMessage());
        }
    }
}

final class C extends B {
}


function test(string $name, object $obj) {
    printf("# %s\n", $name);

    $reflector = new ReflectionClass($obj::class);

    $reflector->resetAsLazyGhost($obj, function ($obj) {
        $obj->__construct(2, setB: true);
    });

    $reflector->initializeLazyObject($obj);

    var_dump($obj);
}

$obj = new B(1);
test('B', $obj);

$obj = new C(1);
test('C', $obj);
