<?php

class Foo {
    public function bar(): void {
        return -1; // not permitted in a void function
    }
}

?>