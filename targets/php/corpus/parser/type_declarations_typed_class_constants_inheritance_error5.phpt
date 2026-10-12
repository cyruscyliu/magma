<?php

trait T {
    public const array CONST1 = [];
}

class C {
    use T;

    public const ?array CONST1 = [];
}

?>