<?php

class C extends DateTime {
}

$reflector = new ReflectionClass(C::class);

print "# Ghost:\n";

try {
    $obj = $reflector->newLazyGhost(function ($obj) {
        var_dump("initializer");
        $obj->__construct();
    });
} catch (Error $e) {
    printf("%s: %s\n", $e::class, $e->getMessage());
}

print "# Proxy:\n";

try {
    $obj = $reflector->newLazyProxy(function ($obj) {
        var_dump("initializer");
        $obj->__construct();
    });
} catch (Error $e) {
    printf("%s: %s\n", $e::class, $e->getMessage());
}
