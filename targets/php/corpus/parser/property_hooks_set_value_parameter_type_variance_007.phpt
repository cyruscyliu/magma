<?php

interface X {}
interface Y extends X {}

class A {
    public Y $prop {
        set(X $prop) {}
    }
}

class B extends A {
    public Y $prop {
        set(Y $prop) {}
    }
}

?>