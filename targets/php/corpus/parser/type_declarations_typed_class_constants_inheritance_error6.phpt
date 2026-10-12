<?php

interface A {
    public const string CONST1 = 'A';
}

class B implements A {
    public const CONST1 = 'B';
}

?>