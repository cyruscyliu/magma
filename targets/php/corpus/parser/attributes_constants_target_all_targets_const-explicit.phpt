<?php

#[Attribute(Attribute::TARGET_ALL)]
class MyAttribute {}

#[MyAttribute]
const EXAMPLE = 'Foo';

$ref = new ReflectionConstant('EXAMPLE');
$attribs = $ref->getAttributes();
var_dump($attribs);
$attribs[0]->newInstance();

?>