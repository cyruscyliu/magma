<?php

#[Attr(static function ($foo) {
    echo $foo;
})]
function foo() { }

$r = new ReflectionFunction('foo');
foreach ($r->getAttributes() as $attribute) {
    echo $attribute;
}

?>