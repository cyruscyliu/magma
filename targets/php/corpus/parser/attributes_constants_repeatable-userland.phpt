<?php

#[Attribute(Attribute::TARGET_ALL|Attribute::IS_REPEATABLE)]
class MyAttribute {}

#[MyAttribute]
#[MyAttribute]
const MY_CONST = true;

$attributes = new ReflectionConstant('MY_CONST')->getAttributes();
var_dump($attributes);
$attributes[0]->newInstance();

?>