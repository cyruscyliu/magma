<?php

class A {
    private function test() {}
}

trait T {
    private function test() {}
}

class B extends A {
    use T;
}

?>