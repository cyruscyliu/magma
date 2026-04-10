<?php

class A {
    public function create(): ?A {}
}

trait T {
    public function create(): self {}
}

class B extends A {
    use T;
}

?>
===DONE===