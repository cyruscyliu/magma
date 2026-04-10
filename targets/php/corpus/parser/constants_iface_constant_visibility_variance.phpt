<?php
interface I {
    public const FOO = 'foo';
}

class C implements I {
    private const FOO = 'foo';
}
?>