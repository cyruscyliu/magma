<?php

// Still allowed via trait
trait TraitWithAbstract {
    abstract public function foo();
}
class TraitWorks {
    use TraitWithAbstract;
}

class NotAbstract {
    abstract public function bar();
}
?>