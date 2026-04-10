<?php

namespace NS;

class Test {
    public function test() {
        return preg_match('foo', 'bar');
    }
}

$test = new Test();
$test->test();

?>