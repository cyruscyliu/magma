<?php
#[Attribute]
class MyAttrib{}
#[MyAttrib(notinterned:'')]
class Test1{}
$attr=(new ReflectionClass(Test1::class))->getAttributes()[0];
try {
    $attr->newInstance();
} catch (Error $e) {
    echo $e->getMessage(), "\n";
}
?>