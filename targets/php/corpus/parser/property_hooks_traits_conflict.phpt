<?php

trait T {
    public $prop {
        get { echo __METHOD__, "\n"; }
        set { echo __METHOD__, "\n"; }
    }
}

class C {
    use T;

    public $prop {
        get { echo __METHOD__, "\n"; }
        set { echo __METHOD__, "\n"; }
    }
}

?>