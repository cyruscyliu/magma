<?php

class S {
    public function __toString() {
        static $i = 0;
        $i++;
        if ($i === 1) {
            return 'S';
        } else {
            throw new \Exception('Thrown from S');
        }
    }
}

const S = new S();

class B {
    public $prop = A::C . S;
}

spl_autoload_register(function ($class) {
    class A { const C = "A"; }
    var_dump(new B());
});

var_dump(new B());

?>