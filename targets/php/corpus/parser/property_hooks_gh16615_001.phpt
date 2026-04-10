<?php

class Foo {
    public string $bar {
        set => $value;
    }
}

$reflector = new ReflectionClass(Foo::class);

// Adds IS_PROP_LAZY to prop flags
$foo = $reflector->newLazyGhost(function ($ghost) {
    $ghost->bar = 'bar';
});

echo $foo->bar;

?>