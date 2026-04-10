<?php

class A {
    public $prop {
        set {
            $this->prop = 42;
        }
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