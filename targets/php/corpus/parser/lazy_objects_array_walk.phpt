<?php

class C {
    public int $a = 1;
}


$reflector = new ReflectionClass(C::class);
$obj = $reflector->newLazyProxy(function () {
    return new C();
});

array_walk($obj, function (&$value, $key) {
    try {
        $value = 'string';
    } catch (Error $e) {
        printf("%s: %s\n", $e::class, $e->getMessage());
    }
    $value = 2;
});

var_dump($obj);

?>