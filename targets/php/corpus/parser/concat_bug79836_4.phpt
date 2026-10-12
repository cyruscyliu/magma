<?php
class Foo {
    public function __toString() {
        return str_repeat('a', 10);
    }
}

$i = str_repeat('a', 5 * 1024 * 1024);
$e = new Foo();
$e .= $i;
?>