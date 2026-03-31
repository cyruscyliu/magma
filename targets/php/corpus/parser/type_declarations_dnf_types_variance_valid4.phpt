<?php

class A {}
class B extends A {}
interface X {}

class Test {
    public (A&B)|X $prop;
}
class Test2 extends Test {
    public B|X $prop;
}

?>
===DONE===