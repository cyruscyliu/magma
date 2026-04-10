<?php

#[Attribute(Attribute::TARGET_CONSTANT)]
class MyConstantAttribute {}

#[MyConstantAttribute]
class Example {}

$ref = new ReflectionClass(Example::class);
$attribs = $ref->getAttributes();
var_dump($attribs);
$attribs[0]->newInstance();

?>