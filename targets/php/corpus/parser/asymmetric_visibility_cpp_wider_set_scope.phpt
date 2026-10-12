<?php

class Foo {
    public function __construct(
        private protected(set) string $bar
    ) {}
}

?>