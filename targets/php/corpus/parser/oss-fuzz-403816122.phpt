<?php

const X = 'x';

class P {
    public $prop;
}

class C extends P {
    public $prop = X {
        get => 'y';
    }
}

var_dump((new C)->prop);

?>