<?php

#[Attribute]
class MyAttribute {
    public function __construct($first, $second) {
        echo "first: $first\n";
        echo "second: $second\n";
    }
}

#[MyAttribute(second: "bar", first: "foo")]
const EXAMPLE = 'ignored';

$ref = new ReflectionConstant('EXAMPLE');
$attribs = $ref->getAttributes();
var_dump($attribs);
var_dump($attribs[0]->getArguments());
$attribs[0]->newInstance();

?>