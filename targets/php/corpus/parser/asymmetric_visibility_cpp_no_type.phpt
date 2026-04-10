<?php

class Foo {
    public function __construct(
        public private(set) $bar,
    ) {}
}

?>