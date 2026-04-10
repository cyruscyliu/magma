<?php

#[DelayedTargetValidation]
#[AllowDynamicProperties]
class DemoClass {}

$obj = new DemoClass();
var_dump($obj);
// No warnings
$obj->dynamic = true;
var_dump($obj);

$ref = new ReflectionClass('DemoClass');
echo $ref . "\n";
$attributes = $ref->getAttributes();
var_dump($attributes);
var_dump($attributes[1]->newInstance());

?>