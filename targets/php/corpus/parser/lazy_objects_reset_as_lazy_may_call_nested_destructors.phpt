<?php

class Foo {
    public function __destruct() {
        printf("%s\n", __METHOD__);
    }
}

class Bar {
    public string $s;
    public ?Foo $foo;

    public function __destruct() {
        printf("%s\n", __METHOD__);
    }
}

$bar = new Bar();
$bar->foo = new Foo();

$reflector = new ReflectionClass(Bar::class);

print "Reset\n";

$reflector->resetAsLazyProxy($bar, function (Bar $bar) {
    $result = new Bar();
    $result->foo = null;
    $result->s = 'init';
    return $result;
});

print "Dump\n";

var_dump($bar->s);

print "Done\n";

?>