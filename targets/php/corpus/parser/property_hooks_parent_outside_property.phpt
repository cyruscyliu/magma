<?php

class A {
    public function test() {
        return parent::$prop::get();
    }
}

?>