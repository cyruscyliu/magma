<?php

interface A {}
interface B extends A {}
interface C {}
interface X {}

class Test implements B, C {}

class Foo {
    public function foo(): (B&C)|X {
        return new Test();
    }
}

/* This fails because A is a parent type for B */
class FooChild extends Foo {
    public function foo(): (A&C)|X {
        return new Test();
    }
}

?>