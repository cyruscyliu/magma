<?php

interface I {
    public $prop { &get; }
}

class A implements I {
    public $prop {
        get => $this->prop;
    }
}

?>