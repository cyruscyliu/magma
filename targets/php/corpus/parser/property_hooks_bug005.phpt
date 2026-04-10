<?php

class B {
    protected mixed $x;
}

class C extends B {
    protected mixed $x {
        set {
            parent::$x::set(1);
        }
    }
}

?>
===DONE===