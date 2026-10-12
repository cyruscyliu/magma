<?php

interface X {}
interface Y {}
class A implements X, Y {}
class B {}

class Test {
    public (X&Y)|B $prop;
}
class Test2 extends Test {
    public A|B $prop;
}

?>
===DONE===