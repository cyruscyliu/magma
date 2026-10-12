<?php

class A
{
    public function test(): void
    {
        echo 'called';
    }
}

new A->test();

?>