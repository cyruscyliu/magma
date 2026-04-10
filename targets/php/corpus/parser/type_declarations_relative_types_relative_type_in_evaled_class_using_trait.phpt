<?php

trait TraitCompiled {
    public function bar(): self { return new self; }
}

const EVAL_CODE = <<<'CODE'
class A {
    use TraitCompiled;
}
CODE;

eval(EVAL_CODE);

$a1 = new A();
$a2 = $a1->bar();
var_dump($a2);

?>
DONE