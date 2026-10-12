<?php

class A
{
    public static function test(): void
    {
        echo 'called';
    }
}

new A::test();

?>