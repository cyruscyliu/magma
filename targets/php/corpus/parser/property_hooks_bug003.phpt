<?php

class B {
    public mixed $x;
}
class C extends B {
    public mixed $x {
        set {
            $f = parent::$x::set(...);
            $f($value);
        }
    }
}

$c = new C();
$c->x = 0;

?>