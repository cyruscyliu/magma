<?php

#[\Foo]
#[\Bar]
const CONSTANT = 1;

$ref = new ReflectionConstant('CONSTANT');
var_dump($ref->getAttributes());

?>