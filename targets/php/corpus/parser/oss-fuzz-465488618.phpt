<?php

class A {
    public function test(int $x) {}
}

class B extends A {
    public function test(string $x = Foo::{C}) {}
}

?>