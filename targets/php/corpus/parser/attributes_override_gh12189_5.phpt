<?php

abstract class A {
    abstract public function __construct();
}

trait T {
    #[\Override]
    public function __construct() {
        echo 'foo';
    }
}

class D extends A {
    use T;
}
echo "Done";

?>