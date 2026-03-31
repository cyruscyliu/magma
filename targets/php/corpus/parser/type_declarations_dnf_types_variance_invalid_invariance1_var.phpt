<?php

interface X {}
interface Y {}

class A {
    public (X&Y&Z)|L $prop;
}
class B extends A {
    public (X&Y)|L $prop;
}

?>