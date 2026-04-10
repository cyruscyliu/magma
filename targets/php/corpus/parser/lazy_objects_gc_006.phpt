<?php

class Foo {
    public $foo;
}

class Initializer {
    public function __invoke($obj) {
        $obj->foo = $this;
        var_dump(__METHOD__);
    }
    public function __destruct() {
        var_dump(__METHOD__);
    }
}

$reflector = new ReflectionClass(Foo::class);
$foo = $reflector->newLazyGhost(new Initializer());

print "Dump\n";

var_dump($foo->foo);

print "Done\n";

?>