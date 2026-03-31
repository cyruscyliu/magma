<?php

class C {
    use _ZendTestTrait;
}

$o = new C();
var_dump($o);

$prop = new \ReflectionProperty(C::class, 'classUnionProp');
$union = $prop->getType();
$types = $union->getTypes();
var_dump($types, (string)$types[0], (string)$types[1]);

?>
===DONE===