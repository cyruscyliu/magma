<?php

class A {
    public $prop {
        final get { return 42; }
    }
}

class B extends A {
    public $prop {
        get { return 24; }
    }
}

?>