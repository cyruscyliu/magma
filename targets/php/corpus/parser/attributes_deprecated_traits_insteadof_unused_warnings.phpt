<?php

#[Deprecated]
trait DemoTraitA {
    public function lowerCase(): string {
        return 'a';
    }
    public function upperCase(): string {
        return 'A';
    }
}

#[Deprecated]
trait DemoTraitB {
    public function lowerCase(): string {
        return 'b';
    }
    public function upperCase(): string {
        return 'B';
    }
}

class DemoClass {
    use DemoTraita, DemoTraitB {
        DemoTraitA::lowerCase insteadof DemoTraitB;
        DemoTraitA::upperCase insteadof DemoTraitB;
    }
}

$d = new DemoClass();
var_dump($d->lowerCase());
var_dump($d->upperCase());

?>