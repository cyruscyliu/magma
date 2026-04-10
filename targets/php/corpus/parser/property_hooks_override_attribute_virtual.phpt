<?php

class A {
    public $prop {
        get => 42;
    }
}

class B extends A {
    public $prop {
        #[Override]
        get => parent::$prop::get();
    }
}

?>
===DONE===