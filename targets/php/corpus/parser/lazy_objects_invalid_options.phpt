<?php

class C {
    public $a = 1;
}

$reflector = new ReflectionClass(C::class);

try {
    $obj = $reflector->newLazyGhost(function ($obj) { }, -1);
} catch (ReflectionException $e) {
    printf("%s: %s\n", $e::class, $e->getMessage());
}

try {
    $obj = $reflector->newLazyProxy(function ($obj) { }, -1);
} catch (ReflectionException $e) {
    printf("%s: %s\n", $e::class, $e->getMessage());
}

try {
    // SKIP_DESTRUCTOR is only allowed on resetAsLazyProxy()
    $obj = $reflector->newLazyGhost(function ($obj) { }, ReflectionClass::SKIP_DESTRUCTOR);
} catch (ReflectionException $e) {
    printf("%s: %s\n", $e::class, $e->getMessage());
}

$obj = new C();

try {
    $reflector->resetAsLazyGhost($obj, function ($obj) { }, -1);
} catch (ReflectionException $e) {
    printf("%s: %s\n", $e::class, $e->getMessage());
}

try {
    $reflector->resetAsLazyProxy($obj, function ($obj) { }, -1);
} catch (ReflectionException $e) {
    printf("%s: %s\n", $e::class, $e->getMessage());
}

?>