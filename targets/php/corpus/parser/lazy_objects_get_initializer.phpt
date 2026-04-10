<?php

class C {
    public $a;

    public static function initStatic() {}
    public function init() {}
}

function foo() {
}

$reflector = new ReflectionClass(C::class);

$initializers = [
    'foo',
    foo(...),
    function () {},
    [C::class, 'initStatic'],
    [new C(), 'init'],
    C::initStatic(...),
    (new C())->init(...),
];

foreach ($initializers as $i => $initializer) {
    $c = $reflector->newLazyGhost($initializer);
    if ($reflector->getLazyInitializer($c) !== $initializer) {
        printf("Initializer %d: failed\n", $i);
        continue;
    }

    $reflector->initializeLazyObject($c);
    if ($reflector->getLazyInitializer($c) !== null) {
        printf("Initializer %d: failed\n", $i);
        continue;
    }

    printf("Initializer %d: ok\n", $i);
}

?>