<?php

interface Foo {}

class P {
    public function test(Foo|callable $foo) {}
}

class C extends P {
    public function test(Foo|callable $foo) {}
}

?>
===DONE===