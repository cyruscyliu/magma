<?php

#[AllowDynamicProperties]
class C {
    public int $a;
    private int $_b;
    public int $b {
        &get { $ref = &$this->_b; return $ref; }
    }
    public function __construct(bool $addDynamic = true) {
        var_dump(__METHOD__);
        $this->a = 1;
        $this->_b = 2;
        if ($addDynamic) {
            $this->c = 3;
            $this->d = 4;
            unset($this->c);
        }
    }
}

$reflector = new ReflectionClass(C::class);

function test(string $name, object $obj) {
    printf("# %s:\n", $name);
    foreach ($obj as $prop => $value) {
        var_dump($prop, $value);
    }
    foreach ($obj as $prop => &$value) {
        var_dump($prop, $value);
    }
}

$obj = $reflector->newLazyGhost(function ($obj) {
    var_dump("initializer");
    $obj->__construct();
});

test('Ghost', $obj);

$obj = $reflector->newLazyProxy(function ($obj) {
    var_dump("initializer");
    return new C();
});

test('Proxy', $obj);

$obj = $reflector->newLazyGhost(function ($obj) {
    var_dump("initializer");
    $obj->__construct(addDynamic: false);
});

test('Ghost (no dynamic)', $obj);

$obj = $reflector->newLazyProxy(function ($obj) {
    var_dump("initializer");
    return new C(addDynamic: false);
});

test('Proxy (no dynamic)', $obj);

print "# Proxy of proxy (initialization)\n";

$obj = $reflector->newLazyProxy(function ($obj) use (&$obj2, $reflector) {
    var_dump("initializer");
    return $obj2 = new C();
});
$reflector->initializeLazyObject($obj);
$reflector->resetAsLazyProxy($obj2, function () {
    return new C();
});

test('Proxy of proxy', $obj);

print "# Ghost (init exception):\n";

$obj = $reflector->newLazyGhost(function ($obj) {
    throw new \Exception("initializer");
});

try {
    var_dump(json_encode($obj));
} catch (\Exception $e) {
    printf("%s: %s\n", $e::class, $e->getMessage());
}

print "# Proxy (init exception):\n";

$obj = $reflector->newLazyProxy(function ($obj) {
    throw new \Exception("initializer");
});

try {
    var_dump(json_encode($obj));
} catch (\Exception $e) {
    printf("%s: %s\n", $e::class, $e->getMessage());
}
