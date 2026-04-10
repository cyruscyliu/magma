<?php

class C {
    public $x=x;
}

$reflector = new ReflectionClass(C::class);

try {
    $obj = $reflector->newLazyGhost(function() {});
    clone $obj;
} catch (Error $e) {
    printf("%s: %s\n", $e::class, $e->getMessage());
}


?>