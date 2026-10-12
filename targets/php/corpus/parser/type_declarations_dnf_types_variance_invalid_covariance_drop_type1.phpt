<?php

interface A {}
interface B {}
interface X {}

class Test implements A, B {}

class Foo {
    public function foo(): (A&B)|X {
        return new Test();
    }
}

/* This fails because just A larger than A&B */
class FooChild extends Foo {
    public function foo(): A|X {
        return new Test();
    }
}

?>