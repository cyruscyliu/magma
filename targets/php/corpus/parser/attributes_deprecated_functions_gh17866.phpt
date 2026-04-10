<?php

class Foo {
    #[Deprecated("xyzzy")]
    public function __invoke() {
        echo "In __invoke\n";
    }
}

$foo = new Foo;
$closure = Closure::fromCallable($foo);
$test = $closure->__invoke(...);

$rc = new ReflectionMethod($test, '__invoke');
var_dump($rc->getAttributes());
var_dump($rc->isDeprecated());

$test();

?>