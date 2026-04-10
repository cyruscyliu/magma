<?php

#[Attribute(Attribute::TARGET_FUNCTION)]
class MyFunctionAttribute {}

#[MyFunctionAttribute]
const EXAMPLE = 'Foo';

$ref = new ReflectionConstant('EXAMPLE');
$attribs = $ref->getAttributes();
var_dump($attribs);
$attribs[0]->newInstance();

?>