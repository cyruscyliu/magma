<?php

interface A {}
interface B {}
interface C {}
interface X {}

class Test implements A, B, C {}

class Foo {
    public function foo(): (A&B&C)|X {
        return new Test();
    }
}

/* This fails because just (A&B) larger than ((A&B)&C) */
class FooChild extends Foo {
    public function foo(): (A&B)|X {
        return new Test();
    }
}

?>