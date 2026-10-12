<?php
trait TraitExample {
    public function bar(): ?parent { return parent::class; }
}

class A {
    use TraitExample;
}
?>
DONE