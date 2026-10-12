<?php

class A {
    public $prop = 42;
}

class Printer {
    public function __construct() {
        echo "Printer\n";
        return 'printer';
    }
}

const A_prop = (new A)->{new Printer ? 'printer' : null};

?>