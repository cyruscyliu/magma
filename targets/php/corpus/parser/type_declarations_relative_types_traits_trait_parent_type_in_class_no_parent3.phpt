<?php
trait TraitExample {
    public function bar(): int|parent { return parent::class; }
}

class A {
    use TraitExample;
}
?>
DONE