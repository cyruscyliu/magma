<?php

interface X {}
interface Y {}

interface L {}

class TestOne implements X, Y {}
class TestTwo implements X {}

interface A
{
    public function foo(): (X&Y)|L;
}

interface B extends A
{
    public function foo(): TestOne|TestTwo;
}

?>