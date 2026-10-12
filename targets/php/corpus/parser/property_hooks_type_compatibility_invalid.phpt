<?php

class A {
    public int $a { get {} }
}
class B extends A {
    public int|float $a { get {} }
}

?>