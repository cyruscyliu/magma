<?php

trait T {
    public $prop;
}

readonly class C {
    use T;
}

?>