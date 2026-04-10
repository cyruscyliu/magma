<?php

class C {
    public int $a;
    public int $b;
    public function __construct() {
        var_dump(__METHOD__);
        $this->a = 1;
        $this->b = 2;
    }
}

$reflector = new ReflectionClass(C::class);

print "# Ghost:\n";

$obj = $reflector->newLazyGhost(function ($obj) {
    var_dump("initializer");
    $obj->__construct();
});

foreach ($obj as $prop => $value) {
    var_dump($prop, $value);
}

print "# Ghost (by ref):\n";

$obj = $reflector->newLazyGhost(function ($obj) {
    var_dump("initializer");
    $obj->__construct();
});

foreach ($obj as $prop => &$value) {
    var_dump($prop, $value);
}

print "# Proxy:\n";

$obj = $reflector->newLazyProxy(function ($obj) {
    var_dump("initializer");
    return new C();
});

foreach ($obj as $prop => $value) {
    var_dump($prop, $value);
}

print "# Proxy (by ref):\n";

$obj = $reflector->newLazyProxy(function ($obj) {
    var_dump("initializer");
    return new C();
});

foreach ($obj as $prop => &$value) {
    var_dump($prop, $value);
}

print "# Ghost (init failure)\n";

$fail = true;
$obj = $reflector->newLazyGhost(function ($obj) use (&$fail) {
    if ($fail) {
        throw new Exception("initializer");
    } else {
        var_dump("initializer");
        $obj->__construct();
    }
});

try {
    foreach ($obj as $prop => $value) {
        var_dump($prop, $value);
    }
} catch (Exception $e) {
    printf("%s: %s\n", $e::class, $e->getMessage());
}

$fail = false;
foreach ($obj as $prop => $value) {
    var_dump($prop, $value);
}

print "# Ghost (init failure, by ref)\n";

$fail = true;
$obj = $reflector->newLazyGhost(function ($obj) use (&$fail) {
    if ($fail) {
        throw new Exception("initializer");
    } else {
        var_dump("initializer");
        $obj->__construct();
    }
});

try {
    foreach ($obj as $prop => &$value) {
        var_dump($prop, $value);
    }
} catch (Exception $e) {
    printf("%s: %s\n", $e::class, $e->getMessage());
}

$fail = false;
foreach ($obj as $prop => &$value) {
    var_dump($prop, $value);
}

?>