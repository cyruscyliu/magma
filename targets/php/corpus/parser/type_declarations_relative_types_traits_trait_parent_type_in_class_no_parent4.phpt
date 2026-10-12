<?php
trait TraitExample {
    public function bar(): (X&Y)|parent { return parent::class; }
}

class A {
    use TraitExample;
}
?>
DONE