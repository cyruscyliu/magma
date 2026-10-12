<?php
class Foo {
    public function &__call($method, $args) {
        return $method;
    }
}

$foo = new Foo;
$bar = $foo->bar(...);
echo $bar(),"\n";
?>