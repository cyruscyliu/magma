<?php

abstract class P {
    abstract protected $foo { get; }
}

class C1 extends P {
    protected $foo = 1;
}

class C2 extends P {
    protected $foo = 2;
    
    static function foo($c) { return $c->foo; }
}

var_dump(C2::foo(new C2));
var_dump(C2::foo(new C1));

?>