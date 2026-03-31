<?php

#[Attribute("foo")]
class A1 { }

#[A1]
class Foo {}

try {
    (new ReflectionClass(Foo::class))->getAttributes()[0]->newInstance();
} catch (Error $e) {
    echo $e->getMessage(), "\n";
}

?>