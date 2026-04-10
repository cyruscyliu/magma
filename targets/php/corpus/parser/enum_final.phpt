<?php

enum Foo {}

$final = new ReflectionClass(Foo::class)->isFinal();
var_dump($final);

?>