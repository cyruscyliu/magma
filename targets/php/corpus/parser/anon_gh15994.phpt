<?php

abstract class ParentClass {
    abstract public function f();
}

$o = new class extends ParentClass {};
?>