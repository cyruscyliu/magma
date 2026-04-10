<?php

class A {
    public $prop;
}

class B extends A {
    private $_prop;
    public $prop {
        &get => $this->_prop;
        set { $this->_prop = $value; }
    }
}

?>