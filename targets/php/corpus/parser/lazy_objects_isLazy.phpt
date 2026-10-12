<?php

#[AllowDynamicProperties]
class C {
    public static $staticProp;
    public int $typed;
    public $untyped;
    public $virtual {
        get {}
    }
}

function testProps(ReflectionClass $reflector, object $obj) {
    foreach (['staticProp', 'typed', 'untyped', 'virtual', 'dynamic'] as $name) {
        if ('dynamic' === $name) {
            $tmp = new C();
            $tmp->dynamic = 1;
            $pr = new ReflectionProperty($tmp, $name);
        } else {
            $pr = $reflector->getProperty($name);
        }
        printf("%s: %d\n", $name, $pr->isLazy($obj));
    }
}

$reflector = new ReflectionClass(C::class);

print "# Ghost\n";

$obj = $reflector->newLazyGhost(function () { });

testProps($reflector, $obj);

$pr = $reflector->getProperty('typed');
$pr->skipLazyInitialization($obj);
printf("typed (skipped): %d\n", $pr->isLazy($obj));

print "# Initialized Ghost\n";

$reflector->initializeLazyObject($obj);

testProps($reflector, $obj);

print "# Proxy\n";

$obj = $reflector->newLazyProxy(function () {
    return new C();
});

testProps($reflector, $obj);

$pr = $reflector->getProperty('typed');
$pr->skipLazyInitialization($obj);
printf("typed (skipped prop): %d\n", $pr->isLazy($obj));

print "# Initialized Proxy\n";

$reflector->initializeLazyObject($obj);

testProps($reflector, $obj);

print "# Nested Proxy\n";

$nested = new C();
$obj = $reflector->newLazyProxy(function () use ($nested) {
    return $nested;
});
$reflector->initializeLazyObject($obj);
$reflector->resetAsLazyProxy($nested, function () {
    return new C();
});

testProps($reflector, $obj);

print "# Nested Proxy (nested initialized)\n";

$nested = new C();
$obj = $reflector->newLazyProxy(function () use ($nested) {
    return $nested;
});
$reflector->initializeLazyObject($obj);
$reflector->resetAsLazyProxy($nested, function () {
    return new C();
});
$reflector->initializeLazyObject($nested);

testProps($reflector, $obj);

print "# Internal\n";

$obj = (new DateTime())->diff(new DateTime());
$reflector = new ReflectionClass(DateInterval::class);
$pr = new ReflectionProperty($obj, 'y');
printf("y: %d\n", $pr->isLazy($obj));

?>